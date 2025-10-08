# pylint: disable=import-error
"""Modulo para gestionar usuarios"""

from src.core.database import db
from src.core.board.site import Site
from src.core.board.category import Category
from src.core.board.state import State
from src.core.board.site_history import SiteHistory
from src.core.board.tag import Tag


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


def assign_category_to_site(category, site):
    """Función para asignar una categoría a un sitio."""
    site.category = category
    db.session.commit()
    return site


###Fin de funciones de sitios###

###Funciones de categorías###


def list_categories():
    """Función para listar todas las categorías."""
    categories = db.session.query(Category).all()
    return categories


def create_category(**kwargs):
    """Función para crear una nueva categoría."""
    new_category = Category(**kwargs)
    db.session.add(new_category)
    db.session.commit()
    return new_category


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


def assign_state_to_site(state, site):
    """Función para asignar una provincia a un sitio."""
    site.state = state
    db.session.commit()
    return site


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


###Fin de funciones de etiquetas###
