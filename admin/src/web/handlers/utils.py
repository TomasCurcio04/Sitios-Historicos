# pylint: disable=import-error
"""Utilidades de autenticación y autorización."""

from flask import flash, session as current_user, abort, redirect, url_for
from src.core.services import auth

# Obtener permisos del usuario
from src.core.services.auth.permission_serv import get_permissions


# Middleware para modo mantenimiento de administración
def admin_maintenance_required(view):
    """Decorator para verificar el estado de mantenimiento de la administración."""

    def wrapped_view(*args, **kwargs):
        flag = auth.get_feature_flag("admin_maintenance_mode")
        usuario = auth.buscar_usuario(current_user.get("user"))
        # SI no es usuario, no puede entrar.
        if not usuario:
            return redirect(url_for("auth.login"))
        if not usuario.s_user:
            abort(403)
        if flag and flag.enabled:
            flash(flag.maintenance_message, "warning")
        return view(*args, **kwargs)

    return wrapped_view


def check_permissions(section, permissions):
    """Verifica si el usuario actual tiene permisos para una sección.

    kwArgs:
        section (str): Nombre de la sección (ej: 'users', 'sites')
        permissions (list): Lista de permisos requeridos (ej: ['create', 'write'])

    Returns:
        bool: True si tiene permisos o es superusuario, False caso contrario
    """
    usuario = auth.usuario_actual()
    if not usuario:
        return False

    # Si es superusuario, permitir acceso
    if usuario.s_user:
        return True

    permissions_user = get_permissions(usuario.role)

    # Verificar si tiene todos los permisos requeridos para la sección
    required_perms = [f"{section}_{perm}" for perm in permissions]
    return all(perm in permissions_user for perm in required_perms)


def permissions_required(section, permissions):
    """Decorador para verificar permisos en rutas."""

    def decorator(view):
        def wrapped_view(*args, **kwargs):
            if not check_permissions(section, permissions):
                abort(403)
            return view(*args, **kwargs)

        return wrapped_view

    return decorator
