"""Modulo para gestionar usuarios"""

from src.core.database import db
from src.core.auth.users import Users


def list_users():
    """Función para listar todos los usuarios."""
    users = db.session.query(Users).all()
    return users


def create_user(**kwargs):
    """Función para crear un nuevo usuario."""
    new_user = Users(**kwargs)
    db.session.add(new_user)
    db.session.commit()
    return new_user
