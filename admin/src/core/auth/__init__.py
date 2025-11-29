# pylint: disable=import-error
"""Módulo de autenticación y autorización."""

import math
from datetime import datetime, timezone
from sqlalchemy import desc
from src.core.entity.users import Users
from src.core.entity.feature_flag import FeatureFlag
from src.core.database import db
from src.core.entity.role import Role
from src.core.entity.permission import Permission
from src.core.services.auth.bcrypt import bcrypt


def list_roles():
    """Lista todos los roles disponibles.

    Returns:
        list[Role]: Lista con los roles del sistema.
    """
    session = db.session
    return session.query(Role).all()


def create_role(**kwargs):
    """Crea un nuevo rol.

    Args:
        **kwargs: Campos del rol.

    Returns:
        Role: Rol creado.
    """
    session = db.session
    new_role = Role(**kwargs)
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role


def assign_role(user_id, role_id):
    """Asigna un rol a un usuario.

    Args:
        user_id (int): ID del usuario.
        role_id (int): ID del rol.

    Returns:
        Users: Usuario actualizado.
    """
    session = db.session
    user = session.query(Users).get(user_id)
    role = session.query(Role).get(role_id)
    user.role = role
    session.commit()
    return user


####Fin de funciones de roles###


####Funciones de permisos###
def list_permissions():
    """Lista todos los permisos disponibles.

    Returns:
        list[Permission]: Permisos del sistema.
    """
    session = db.session
    return session.query(Permission).all()


def create_permission(**kwargs):
    """Crea un nuevo permiso.

    Args:
        **kwargs: Campos del permiso.

    Returns:
        Permission: Permiso creado.
    """
    session = db.session
    perm = Permission(**kwargs)
    session.add(perm)
    session.commit()
    session.refresh(perm)
    return perm


def assign_permission(role_id, permission_id):
    """Asigna un permiso a un rol.

    Args:
        role_id (int): ID del rol.
        permission_id (int): ID del permiso.

    Returns:
        Role: Rol con el permiso asignado.
    """
    session = db.session
    role = session.query(Role).get(role_id)
    perm = session.query(Permission).get(permission_id)
    role.permission.append(perm)
    session.commit()
    return role


####Fin de funciones de permisos###


####Funciones de feature flags###
def list_feature_flags():
    """Lista todas las feature flags ordenadas por id.

    Returns:
        list[FeatureFlag]: Lista de flags.
    """

    flags = db.session.query(FeatureFlag).order_by(FeatureFlag.id).all()
    return flags


def get_feature_flag(name):
    """Obtiene una feature flag por nombre.

    Args:
        name (str): Nombre de la flag.

    Returns:
        FeatureFlag | None: Flag encontrada o None.
    """

    flag = db.session.query(FeatureFlag).filter_by(name=name).first()
    return flag


def modify_feature_flag(name, enabled, updated_by, maintenance_message=None):
    """Modifica una feature flag existente.

    Args:
        name (str): Nombre de la flag a modificar.
        enabled (bool): Nuevo estado.
        updated_by (int): ID del usuario que realiza la modificación.
        maintenance_message (str | None): Mensaje de mantenimiento (opcional).

    Returns:
        FeatureFlag | None: Flag modificada o None si no existe.
    """

    flag = FeatureFlag.get_flag(name)
    if flag:
        flag.enabled = enabled
        flag.updated_by = updated_by
        if maintenance_message is not None:
            flag.maintenance_message = maintenance_message
        db.session.commit()
    return flag


def get_feature_flag_fresh(name):
    """Función para obtener una feature flag fresca desde la base de datos."""
    db.session.expire_all()
    flag = db.session.query(FeatureFlag).filter_by(name=name).first()
    return flag


def update_feature_flags(flags_data, updated_by):
    """Actualiza múltiples feature flags según un diccionario de datos.

    Args:
        flags_data (dict): Mapeo de id -> {enabled, maintenance_message}.
        updated_by (int): ID del usuario que realiza la actualización.

    Returns:
        bool: True si hubo cambios y se guardaron, False si no hubo cambios.
    """
    flags = list_feature_flags()
    has_changes = False
    for flag in flags:
        flag_id = str(flag.id)
        if flag_id in flags_data:
            new_enabled = flags_data[flag_id].get("enabled", False)
            new_message = flags_data[flag_id].get("maintenance_message", "")

            if flag.enabled != new_enabled or flag.maintenance_message != new_message:
                flag.enabled = new_enabled
                flag.maintenance_message = new_message
                flag.updated_by = updated_by
                has_changes = True

    if has_changes:
        db.session.commit()
        db.session.expire_all()
    return has_changes


####Fin de funciones de feature flags###
