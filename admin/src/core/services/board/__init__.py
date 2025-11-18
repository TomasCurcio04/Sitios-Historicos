"""
Módulo para gestionar sitios históricos, categorías, estados, usuarios y tags.
Se integra con base de datos usando SQLAlchemy y mantiene soporte JSON para pruebas.
"""

import os
import json
from datetime import datetime
from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.category import Category
from src.core.entity.state import State
from src.core.entity.site_history import SiteHistory
from src.core.entity.tag import Tag
from src.core.entity.review import Review

# -------------------------
# Configuración de fuente de datos
# -------------------------
USE_JSON = False  # Cambiar a True solo si querés usar JSON en lugar de DB
DATA_FILE = os.path.join(os.path.dirname(__file__), "sites.json")

# -------------------------
# Funciones de JSON
# -------------------------
def load_sites():
    """Carga sitios desde archivo JSON.
    
    Returns:
        Lista de sitios o lista vacía si no existe el archivo
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_sites(sites):
    """Guarda sitios en archivo JSON.
    
    Args:
        sites: Lista de sitios a guardar
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sites, f, ensure_ascii=False, indent=4)

def get_all_sites_json():
    """Obtiene todos los sitios desde JSON.
    
    Returns:
        Lista de todos los sitios
    """
    return load_sites()

def get_site_json(site_id):
    """Obtiene un sitio específico desde JSON.
    
    Args:
        site_id: ID del sitio a buscar
    
    Returns:
        Sitio encontrado o None
    """
    for site in load_sites():
        if site["id"] == site_id:
            return site
    return None

def create_site_json(data):
    """Crea un nuevo sitio en JSON.
    
    Args:
        data: Datos del sitio a crear
    
    Returns:
        Sitio creado con ID asignado
    """
    sites = load_sites()
    new_id = max([s["id"] for s in sites], default=0) + 1
    data["id"] = new_id
    data["fecha_registro"] = datetime.now().isoformat()
    sites.append(data)
    save_sites(sites)
    return data

def update_site_json(site_id, updated_data):
    sites = load_sites()
    for i, site in enumerate(sites):
        if site["id"] == site_id:
            sites[i].update(updated_data)
            save_sites(sites)
            return sites[i]
    return None

def delete_site_json(site_id):
    sites = load_sites()
    for i, site in enumerate(sites):
        if site["id"] == site_id:
            del sites[i]
            save_sites(sites)
            return True
    return False

# -------------------------
# Funciones de sitios usando DB
# -------------------------
def list_sites():
    """Lista todos los sitios históricos.
    
    Returns:
        Lista de sitios desde DB o JSON según configuración
    """
    if USE_JSON:
        return get_all_sites_json()
    session = db.session
    return session.query(Site).all()

def get_site(site_id):
    """Obtiene un sitio por su ID.
    
    Args:
        site_id: ID del sitio a buscar
    
    Returns:
        Sitio encontrado o None
    """
    if USE_JSON:
        return get_site_json(site_id)
    session = db.session
    return session.get(Site, site_id)

def create_site(**kwargs):
    """Crea un nuevo sitio histórico.
    
    Args:
        **kwargs: Datos del sitio a crear
    
    Returns:
        Sitio creado
    """
    if USE_JSON:
        return create_site_json(kwargs)
    site = Site(**kwargs)
    session = db.session
    session.add(site)
    session.commit()
    session.refresh(site)
    return site

def update_site(site_id, **kwargs):
    if USE_JSON:
        return update_site_json(site_id, kwargs)
    session = db.session
    site = session.get(Site, site_id)
    for key, value in kwargs.items():
        setattr(site, key, value)
    session.commit()
    session.refresh(site)
    return site

def delete_site(site_id):
    if USE_JSON:
        return delete_site_json(site_id)
    session = db.session
    site = session.get(Site, site_id)
    session.delete(site)
    session.commit()
    return True

# -------------------------
# Funciones de reseñas usando DB
# -------------------------

def create_review(**kwargs):
    review = Review(**kwargs)
    session = db.session
    session.add(review)
    session.commit()
    session.refresh(review)
    return review
# -------------------------
# Funciones de asignación
# -------------------------
def assign_user(site, user):
    session = db.session
    site = session.merge(site)
    site.user = user
    session.commit()
    session.refresh(site)
    return site

def assign_category_to_site(category, site):
    session = db.session
    site = session.merge(site)
    site.category_rel = category
    session.commit()
    session.refresh(site)
    return site

def assign_state_to_site(state, site):
    session = db.session
    site = session.merge(site)
    site.state_rel = state
    session.commit()
    session.refresh(site)
    return site

def assign_tag_to_site(tag, site):
    session = db.session
    site = session.merge(site)
    if tag not in site.tag:
        site.tag.append(tag)
    session.commit()
    session.refresh(site)
    return site

# -------------------------
# Funciones de categorías
# -------------------------
def list_categories():
    """Lista todas las categorías disponibles.
    
    Returns:
        Lista de categorías
    """
    session = db.session
    return session.query(Category).all()

def create_category(**kwargs):
    """Crea una nueva categoría.
    
    Args:
        **kwargs: Datos de la categoría
    
    Returns:
        Categoría creada
    """
    category = Category(**kwargs)
    session = db.session
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

# -------------------------
# Funciones de estados/provincias
# -------------------------
def list_states():
    """Lista todos los estados/provincias.
    
    Returns:
        Lista de estados
    """
    session = db.session
    return session.query(State).all()

def create_state(**kwargs):
    """Crea un nuevo estado/provincia.
    
    Args:
        **kwargs: Datos del estado
    
    Returns:
        Estado creado
    """
    state = State(**kwargs)
    session = db.session
    session.add(state)
    session.commit()
    session.refresh(state)
    return state

# -------------------------
# Funciones de historial de sitios
# -------------------------
def list_site_history():
    session = db.session
    return session.query(SiteHistory).all()

def create_site_history(**kwargs):
    site_history = SiteHistory(**kwargs)
    session = db.session
    session.add(site_history)
    session.commit()
    session.refresh(site_history)
    return site_history

def assign_site_to_history(site_history, site):
    session = db.session
    site_history = session.merge(site_history)
    site_history.site_rel = site
    session.commit()
    session.refresh(site_history)
    return site_history

def assign_user_to_history(site_history, user):
    session = db.session
    site_history = session.merge(site_history)
    site_history.user = user
    session.commit()
    session.refresh(site_history)
    return site_history

# -------------------------
# Funciones de tags
# -------------------------
def list_tags():
    session = db.session
    return session.query(Tag).all()

def create_tag(**kwargs):
    """Crea una nueva etiqueta.
    
    Args:
        **kwargs: Datos de la etiqueta
    
    Returns:
        Etiqueta creada
    """
    tag = Tag(**kwargs)
    session = db.session
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag
