# pylint: disable=import-error
"""Modulo para gestionar usuarios"""

from src.core.database import db
from src.core.board.site import Site
from src.core.board.category import Category
from src.core.board.state import State
from src.core.board.site_history import SiteHistory
from src.core.board.tag import Tag

import os
import json
from datetime import datetime

###Funciones de sitios###
def list_sites():
    """Función para listar todos los sitios."""
    sites = db.session.query(Site).all()
    return sites


def create_site(**kwargs):
    """Función para crear un nuevo sitio."""
    new_site = Site(**kwargs)
    db.session.add(new_site)
    db.session.commit()
    return new_site


def assign_user(site, user):
    """Función para asignar un usuario a un sitio."""
    site.users = user
    db.session.commit()
    return site


###Fin de funciones de sitios###

###Funciones de categorías###


def list_categories():
    """Función para listar todas las categorías."""
    categories = db.session.query(Category).all()
    return categories


###Fin de funciones de categorías###

###Funciones de provincias###


def list_states():
    """Función para listar todas las provincias."""
    states = db.session.query(State).all()
    return states


def create_state(**kwargs):
    """Función para crear una nueva provincia."""
    new_state = State(**kwargs)
    db.session.add(new_state)
    db.session.commit()
    return new_state


###Fin de funciones de provincias###


###Funciones de sitios históricos###
def list_site_history():
    """Función para listar todo el historial de sitios."""

    site_history = db.session.query(SiteHistory).all()
    return site_history


def create_site_history(**kwargs):
    """Función para crear un nuevo registro en el historial de sitios."""

    new_site_history = SiteHistory(**kwargs)
    db.session.add(new_site_history)
    db.session.commit()
    return new_site_history


def assign_site_to_history(site_history, site):
    """Función para asignar un sitio a un registro del historial de sitios."""
    site_history.site = site
    db.session.commit()
    return site_history


def assign_user_to_hisotry(site_history, user):
    """Función para asignar un usuario a un registro del historial de sitios."""
    site_history.user = user
    db.session.commit()
    return site_history


###Fin de funciones de sitios históricos###


###Funciones de etiquetas###
def list_tags():
    """Función para listar todas las etiquetas."""
    tags = db.session.query(Tag).all()
    return tags


def create_tag(**kwargs):
    """Función para crear una nueva etiqueta."""
    new_tag = Tag(**kwargs)
    db.session.add(new_tag)
    db.session.commit()
    return new_tag


def assign_tag_to_site(tag, site):
    """Función para asignar una etiqueta a un sitio."""
    site.tag.append(tag)
    db.session.commit()
    return site


"""Módulo para gestionar sitios históricos usando JSON (modo prueba)."""

import os
import json
from datetime import datetime

# Flag para usar JSON o base de datos
USE_JSON = True

# Archivo JSON donde se guardan los sitios (solo para desarrollo)
DATA_FILE = os.path.join(os.path.dirname(__file__), "sites.json")

# -------------------------
# Funciones para JSON
# -------------------------
def load_sites():
    """Carga los sitios desde el archivo JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_sites(sites):
    """Guarda la lista de sitios en JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sites, f, ensure_ascii=False, indent=4)

def get_all_sites_json():
    """Devuelve todos los sitios desde JSON."""
    return load_sites()

def get_site_json(site_id):
    """Devuelve un sitio por su ID desde JSON."""
    sites = load_sites()
    for site in sites:
        if site["id"] == site_id:
            return site
    return None

def create_site_json(data):
    """Crea un nuevo sitio en JSON."""
    sites = load_sites()
    new_id = max([s["id"] for s in sites], default=0) + 1
    data["id"] = new_id
    data["fecha_registro"] = datetime.now().isoformat()
    sites.append(data)
    save_sites(sites)
    return data

def update_site_json(site_id, updated_data):
    """Actualiza un sitio en JSON."""
    sites = load_sites()
    for i, site in enumerate(sites):
        if site["id"] == site_id:
            sites[i].update(updated_data)
            save_sites(sites)
            return sites[i]
    return None

def delete_site_json(site_id):
    """Elimina un sitio en JSON."""
    sites = load_sites()
    for i, site in enumerate(sites):
        if site["id"] == site_id:
            del sites[i]
            save_sites(sites)
            return True
    return False

# -------------------------
# Interfaz pública
# -------------------------
def list_sites():
    """Lista todos los sitios según la fuente de datos."""
    if USE_JSON:
        return get_all_sites_json()
    # Aquí iría db.session.query(Site).all() si se usa base de datos
    return []

def get_site(site_id):
    """Devuelve un sitio por ID según la fuente de datos."""
    if USE_JSON:
        return get_site_json(site_id)
    return None

def create_site(data):
    """Crea un sitio según la fuente de datos."""
    if USE_JSON:
        return create_site_json(data)
    return None

def update_site(site_id, data):
    """Actualiza un sitio según la fuente de datos."""
    if USE_JSON:
        return update_site_json(site_id, data)
    return None

def delete_site(site_id):
    """Elimina un sitio según la fuente de datos."""
    if USE_JSON:
        return delete_site_json(site_id)
    return False