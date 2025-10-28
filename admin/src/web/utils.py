# pylint: disable=import-error
"""Utilidades para la aplicación web."""

from flask import flash, session as current_user, abort, redirect, url_for
from src.core.services.auth.user_serv import buscar_usuario, obtener_usuario_por_id
from src.core.services.auth.feature_flag_serv import get_feature_flag


# Middleware para modo mantenimiento de administración
def admin_maintenance_required(view):
    """Decorator que verifica el estado de mantenimiento administrativo.
    
    Args:
        view: Función de vista a decorar
    
    Returns:
        Función decorada que verifica mantenimiento
    """

    def wrapped_view(*args, **kwargs):
        flag = get_feature_flag("admin_maintenance_mode")
        usuario = buscar_usuario(current_user.get("user"))
        # SI no es usuario, no puede entrar.
        if not usuario:
            return redirect(url_for("auth.login"))
        if not usuario.s_user:
            abort(403)
        if flag and flag.enabled:
            flash(flag.maintenance_message, "warning")
        return view(*args, **kwargs)

    return wrapped_view


def usuario_actual():
    """Obtiene el usuario actual desde la sesión.
    
    Returns:
        Usuario actual o None si no hay sesión
    """
    if not current_user.get("usuario_id"):
        return None
    usuario_id = current_user.get("usuario_id")
    if usuario_id:
        return obtener_usuario_por_id(usuario_id)
    return None
