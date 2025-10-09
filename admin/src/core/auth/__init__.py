"""Modulo para gestionar usuarios"""

# pylint: disable=import-error
from src.core.database import db
from src.core.auth.users import Users
from src.core.auth.role import Role
from src.core.auth.permission import Permission
from src.core.auth.feature_flag import FeatureFlag


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


# ####Fin de funciones de roles###


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

####Funciones de feature flags###


def list_feature_flags():
    """Función para listar todas las feature flags."""

    flags = db.session.query(FeatureFlag).all()
    return flags


# flag = FeatureFlag.get_flag("admin_maintenance_mode")
# print(flag.enabled)


def get_feature_flag(name):
    """Función para obtener una feature flag por su nombre."""

    flag = FeatureFlag.get_flag(name)
    return flag


def modify_feature_flag(name, enabled, updated_by, maintenance_message=None):
    """Función para modificar una feature flag."""

    flag = FeatureFlag.get_flag(name)
    if flag:
        flag.enabled = enabled
        flag.updated_by = updated_by
        if maintenance_message is not None:
            flag.maintenance_message = maintenance_message
        db.session.commit()
    return flag


# Placeholder para current_user, en una aplicación real esto vendría de Flask-Login u otro sistema de autenticación
def current_user():
    return Users(id_user=1, user_name="admin", s_user=False)


# ####Fin de funciones de feature flags###
