"""Modulo para gestionar usuarios"""

from src.core.database import db
from src.core.board import Site


def list_sites():
    """Función para listar todos los usuarios."""
    sites = db.session.query(Site).all()
    return sites


def create_site(**kwargs):
    """Función para crear un nuevo usuario."""
    new_site = Site(**kwargs)
    db.session.add(new_site)
    db.session.commit()
    return new_site
