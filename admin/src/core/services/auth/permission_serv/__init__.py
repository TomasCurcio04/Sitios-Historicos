# pylint: disable=import-error

"""Modulo de servicios de Permisos"""

from src.core.database import db
from src.core.entity.permission import Permission
from src.core.entity.role import Role


####Funciones de permisos###
def list_permissions():
    """Lista todos los permisos del sistema.

    Returns:
        Lista de permisos
    """
    session = db.session
    return session.query(Permission).all()


def create_permission(**kwargs):
    """Crea un nuevo permiso.

    Args:
        **kwargs: Datos del permiso

    Returns:
        Permiso creado
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
        Role: Objeto Role con el permiso agregado.
    """
    session = db.session
    role = session.query(Role).get(role_id)
    perm = session.query(Permission).get(permission_id)
    role.permission.append(perm)
    session.commit()
    return role


def get_permissions(role_id):
    """Obtiene los nombres de permisos de un rol.

    Args:
        role_id (int): ID del rol.

    Returns:
        list[str]: Lista con los nombres de permisos asignados al rol.
    """
    session = db.session
    role = session.query(Role).get(role_id)
    if not role or not role.permission:
        return []
    return [perm.permission_name for perm in role.permission]


####Fin de funciones de permisos###
