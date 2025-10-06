"""Modulo para gestionar usuarios"""

# pylint: disable=import-error
from src.core.database import db
from src.core.auth.users import Users
from src.core.auth.role import Role
from src.core.auth.permission import Permission


####Funciones de usuarios###
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


####Fin de funciones de usuarios###

####Funciones de roles###


def list_roles():
    """Función para listar todos los roles."""
    roles = db.session.query(Role).all()
    return roles


def create_role(**kwargs):
    """Función para crear un nuevo rol."""
    new_role = Role(**kwargs)
    db.session.add(new_role)
    db.session.commit()
    return new_role


def assign_role(user, role):
    """Función para asignar un rol a un usuario."""
    user.role = role
    db.session.commit()
    return user


####Fin de funciones de roles###


####Funciones de permisos###
def list_permissions():
    """Función para listar todos los permisos."""
    permissions = db.session.query(Permission).all()
    return permissions


def assign_permission(role, permission):
    """Función para asignar un permiso a un rol."""
    role.permission.append(permission)
    db.session.commit()
    return role


def create_permission(**kwargs):
    """Función para crear un nuevo permiso."""
    new_permission = Permission(**kwargs)
    db.session.add(new_permission)
    db.session.commit()
    return new_permission


# ####Fin de funciones de permisos###
