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
        return json.load(f)


def save_sites(sites):
    """Guarda todos los sitios en el archivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sites, f, ensure_ascii=False, indent=4)


# --------------------------
# CRUD PRINCIPAL
# --------------------------

def list_sites():
    """
    Devuelve la lista de sitios históricos.
    Si USE_JSON=True -> lee del archivo JSON
    Si USE_JSON=False -> consulta la base de datos
    """
    if USE_JSON:
        return load_sites()
    else:
        return db.session.query(Site).all()


def get_site(site_id):
    """
    Devuelve un sitio histórico por su ID.
    """
    if USE_JSON:
        sites = load_sites()
        for site in sites:
            if site["id"] == site_id:
                return site
        return None
    else:
        return db.session.get(Site, site_id)


def create_site(data):
    """
    Crea un nuevo sitio histórico.
    Valida los datos antes de guardar.
    Genera ID y fecha automática.
    """
    # Validación con el modelo
    SitioHistorico(data)

    if USE_JSON:
        sites = load_sites()
        new_id = max([s["id"] for s in sites], default=0) + 1
        data["id"] = new_id
        data["fecha_registro"] = datetime.now().isoformat()
        sites.append(data)
        save_sites(sites)
        return data
    else:
        new_site = Site(**data)
        db.session.add(new_site)
        db.session.commit()
        return new_site


def update_site(site_id, updated_data):
    """
    Actualiza un sitio histórico existente.
    Valida los datos antes de guardar.
    Devuelve el sitio actualizado o None si no existe.
    """
    # Validación
    SitioHistorico(updated_data)

    if USE_JSON:
        sites = load_sites()
        for i, site in enumerate(sites):
            if site["id"] == site_id:
                sites[i].update(updated_data)
                save_sites(sites)
                return sites[i]
        return None
    else:
        site = db.session.get(Site, site_id)
        if not site:
            return None
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