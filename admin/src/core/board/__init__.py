"""
Módulo para gestionar sitios históricos, categorías, estados, usuarios y tags.
Se integra con base de datos usando SQLAlchemy y mantiene soporte JSON para pruebas.
"""

import os
import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.core.database import Base, engine
from src.core.board.site import Site
from src.core.board.category import Category
from src.core.board.state import State
from src.core.board.site_history import SiteHistory
from src.core.board.tag import Tag

# -------------------------
# Configuración de fuente de datos
# -------------------------
USE_JSON = False  # Cambiar a True solo si querés usar JSON en lugar de DB
DATA_FILE = os.path.join(os.path.dirname(__file__), "sites.json")

# -------------------------
# Funciones de JSON
# -------------------------
def load_sites():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_sites(sites):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(sites, f, ensure_ascii=False, indent=4)

def get_all_sites_json():
    return load_sites()

def get_site_json(site_id):
    for site in load_sites():
        if site["id"] == site_id:
            return site
    return None

def create_site_json(data):
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
    if USE_JSON:
        return get_all_sites_json()
    with Session(engine) as session:
        return session.scalars(select(Site)).all()

def get_site(site_id):
    if USE_JSON:
        return get_site_json(site_id)
    with Session(engine) as session:
        return session.get(Site, site_id)

def create_site(**kwargs):
    if USE_JSON:
        return create_site_json(kwargs)
    site = Site(**kwargs)
    with Session(engine) as session:
        session.add(site)
        session.commit()
        session.refresh(site)
        return site

def update_site(site_id, **kwargs):
    if USE_JSON:
        return update_site_json(site_id, kwargs)
    with Session(engine) as session:
        site = session.get(Site, site_id)
        for key, value in kwargs.items():
            setattr(site, key, value)
        session.commit()
        session.refresh(site)
        return site

def delete_site(site_id):
    if USE_JSON:
        return delete_site_json(site_id)
    with Session(engine) as session:
        site = session.get(Site, site_id)
        session.delete(site)
        session.commit()
        return True

# -------------------------
# Funciones de asignación
# -------------------------
def assign_user(site, user):
    with Session(engine) as session:
        site = session.merge(site)
        site.user = user
        session.commit()
        session.refresh(site)
        return site

def assign_category_to_site(category, site):
    with Session(engine) as session:
        site = session.merge(site)
        site.category_rel = category
        session.commit()
        session.refresh(site)
        return site

def assign_state_to_site(state, site):
    with Session(engine) as session:
        site = session.merge(site)
        site.state_rel = state
        session.commit()
        session.refresh(site)
        return site

def assign_tag_to_site(tag, site):
    with Session(engine) as session:
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
    with Session(engine) as session:
        return session.scalars(select(Category)).all()

def create_category(**kwargs):
    category = Category(**kwargs)
    with Session(engine) as session:
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

# -------------------------
# Funciones de estados/provincias
# -------------------------
def list_states():
    with Session(engine) as session:
        return session.scalars(select(State)).all()

def create_state(**kwargs):
    state = State(**kwargs)
    with Session(engine) as session:
        session.add(state)
        session.commit()
        session.refresh(state)
        return state

# -------------------------
# Funciones de historial de sitios
# -------------------------
def list_site_history():
    with Session(engine) as session:
        return session.scalars(select(SiteHistory)).all()

def create_site_history(**kwargs):
    site_history = SiteHistory(**kwargs)
    with Session(engine) as session:
        session.add(site_history)
        session.commit()
        session.refresh(site_history)
        return site_history

def assign_site_to_history(site_history, site):
    with Session(engine) as session:
        site_history = session.merge(site_history)
        site_history.site_rel = site
        session.commit()
        session.refresh(site_history)
        return site_history

def assign_user_to_history(site_history, user):
    with Session(engine) as session:
        site_history = session.merge(site_history)
        site_history.user = user
        session.commit()
        session.refresh(site_history)
        return site_history

# -------------------------
# Funciones de tags
# -------------------------
def list_tags():
    with Session(engine) as session:
        return session.scalars(select(Tag)).all()

def create_tag(**kwargs):
    tag = Tag(**kwargs)
    with Session(engine) as session:
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag
