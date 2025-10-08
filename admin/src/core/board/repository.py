"""
Capa de persistencia para manejar sitios históricos.

Permite conmutar entre:
- Modo JSON (para desarrollo sin base de datos)
- Modo SQLAlchemy (base de datos real)

Solo cambiando la variable USE_JSON se decide el modo de trabajo.
"""

import os
import json
from datetime import datetime
from src.core.database import db
from src.core.board.site import Site
from src.core.board.sitio_historico import SitioHistorico
from src.core.board.category import Category
from src.core.board.state import State
from src.core.board.tag import Tag
from src.core.board.site_history import SiteHistory

# --------------------------
# CONFIGURACIÓN
# --------------------------

# Si está en True -> usa archivo JSON
# Si está en False -> usa base de datos real
USE_JSON = False

# Ruta del archivo JSON (solo si USE_JSON es True)
DATA_FILE = os.path.join(os.path.dirname(__file__), "sites.json")


# --------------------------
# FUNCIONES AUXILIARES JSON
# --------------------------

def load_sites():
    """Carga todos los sitios desde el archivo JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_sites(sites):
    """Guarda todos los sitios en el archivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sites, f, ensure_ascii=False, indent=4)


# --------------------------
# FUNCIONES CRUD
# --------------------------

def list_sites():
    """Lista todos los sitios históricos."""
    if USE_JSON:
        return load_sites()
    return db.session.query(Site).all()

def get_site(site_id):
    """
    Devuelve un sitio histórico por su ID.
    """
    if USE_JSON:
        for site in load_sites():
            if site["id"] == site_id:
                return site
        return None
    return db.session.get(Site, site_id)

def create_site(data):
    """
    Crea un nuevo sitio histórico.
    Valida los datos antes de guardar.
    Genera ID y fecha automática.
    """
    SitioHistorico(data)  # Validación de todos los campos

    if USE_JSON:
        sites = load_sites()
        new_id = max([s["id"] for s in sites], default=0) + 1
        data["id"] = new_id
        data["fecha_registro"] = datetime.now().isoformat()
        sites.append(data)
        save_sites(sites)
        return data
    else:
        site = Site(**data)
        db.session.add(site)
        db.session.commit()
        return site

def update_site(site_id, updated_data):
    """
    Actualiza un sitio histórico existente (soporta actualización parcial).
    Devuelve el sitio actualizado o None si no existe.
    """
    if USE_JSON:
        sites = load_sites()
        for i, site in enumerate(sites):
            if site["id"] == site_id:
                # Combinar datos existentes con los nuevos para validar
                combined_data = {**site, **updated_data}
                SitioHistorico(combined_data)
                sites[i].update(updated_data)
                save_sites(sites)
                return sites[i]
        return None
    else:
        site = db.session.get(Site, site_id)
        if not site:
            return None
        # Combinar atributos existentes con los nuevos para validar
        existing_data = {
            "name": site.name,
            "short_description": site.short_description,
            "full_description": site.full_description,
            "city": site.city,
            "province": site.province,
            "conservation_state": site.conservation_state,
            "inauguration_year": site.inauguration_year,
            "category": site.category,
            "state": site.state,
            "latitude": site.latitude,
            "longitude": site.longitude,
            "is_visible": site.is_visible,
            "created_by": site.created_by
        }
        combined_data = {**existing_data, **updated_data}
        SitioHistorico(combined_data)

        for key, value in updated_data.items():
            setattr(site, key, value)
        db.session.commit()
        return site

def delete_site(site_id):
    """
    Elimina un sitio histórico por su ID.
    Devuelve True si se eliminó correctamente.
    """
    if USE_JSON:
        sites = load_sites()
        for i, site in enumerate(sites):
            if site["id"] == site_id:
                del sites[i]
                save_sites(sites)
                return True
        return False
    else:
        site = db.session.get(Site, site_id)
        if not site:
            return False
        db.session.delete(site)
        db.session.commit()
        return True


# --------------------------
# FUNCIONES DE ASIGNACIÓN
# --------------------------

def assign_category_to_site(category, site):
    """Asigna una categoría a un sitio."""
    if USE_JSON:
        site["category"] = category
        return site
    site.category_rel = category
    db.session.commit()
    return site

def assign_state_to_site(state, site):
    """Asigna un estado/provincia a un sitio."""
    if USE_JSON:
        site["state"] = state
        return site
    site.state_rel = state
    db.session.commit()
    return site

def assign_tag_to_site(tag, site):
    """Asigna una etiqueta a un sitio."""
    if USE_JSON:
        if "tags" not in site:
            site["tags"] = []
        if tag not in site["tags"]:
            site["tags"].append(tag)
        return site
    if tag not in site.tag:
        site.tag.append(tag)
    db.session.commit()
    return site

def assign_user(site, user):
    """Asigna un usuario a un sitio."""
    if USE_JSON:
        site["user"] = user
        return site
    site.user = user
    db.session.commit()
    return site

def assign_site_to_history(site_history, site):
    """Asigna un sitio a un registro del historial."""
    if USE_JSON:
        site_history["site"] = site
        return site_history
    site_history.site_rel = site
    db.session.commit()
    return site_history

def assign_user_to_history(site_history, user):
    """Asigna un usuario a un registro del historial."""
    if USE_JSON:
        site_history["user"] = user
        return site_history
    site_history.user = user
    db.session.commit()
    return site_history


# --------------------------
# FUNCIONES AUXILIARES: Categorías, Estados y Tags
# --------------------------

def list_categories():
    """Lista todas las categorías."""
    if USE_JSON:
        return []
    return db.session.query(Category).all()

def create_category(**kwargs):
    """Crea una nueva categoría."""
    if USE_JSON:
        return kwargs
    cat = Category(**kwargs)
    db.session.add(cat)
    db.session.commit()
    return cat

def list_states():
    """Lista todas las provincias/estados."""
    if USE_JSON:
        return []
    return db.session.query(State).all()

def create_state(**kwargs):
    """Crea una nueva provincia/estado."""
    if USE_JSON:
        return kwargs
    state = State(**kwargs)
    db.session.add(state)
    db.session.commit()
    return state

def list_tags():
    """Lista todas las etiquetas."""
    if USE_JSON:
        return []
    return db.session.query(Tag).all()

def create_tag(**kwargs):
    """Crea una nueva etiqueta."""
    if USE_JSON:
        return kwargs
    tag = Tag(**kwargs)
    db.session.add(tag)
    db.session.commit()
    return tag

def list_site_history():
    """Lista todos los registros de historial de sitios."""
    if USE_JSON:
        return []
    return db.session.query(SiteHistory).all()

def create_site_history(**kwargs):
    """Crea un nuevo registro en el historial de sitios."""
    if USE_JSON:
        return kwargs
    sh = SiteHistory(**kwargs)
    db.session.add(sh)
    db.session.commit()
    return sh