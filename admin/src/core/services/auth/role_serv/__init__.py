# pylint: disable=import-error
"""Servicio de roles."""

from src.core.database import db
from src.core.entity.role import Role
from src.core.entity.users import Users


def list_roles():
    """Función para listar todos los roles."""
    session = db.session
    return session.query(Role).all()


def create_role(**kwargs):
    """Crea un nuevo rol."""
    session = db.session
    new_role = Role(**kwargs)
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role


def assign_role(user_id, role_id):
    """Asigna un rol a un usuario."""
    session = db.session
    user = session.query(Users).get(user_id)
    role = session.query(Role).get(role_id)
    user.role = role
    session.commit()
    return user