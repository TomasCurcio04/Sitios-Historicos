# pylint: disable=import-error
"""Modulo para gestionar usuarios"""

from src.core.database import db
from src.core.board.site import Site
from src.core.board.category import Category
from src.core.board.state import State


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
