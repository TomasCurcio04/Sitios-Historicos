"""Utilidades de autenticación y autorización."""

from flask import flash, abort, redirect, url_for
from src.core import auth
from src.core.services.auth.user_serv import buscar_usuario, usuario_actual


# Middleware para modo mantenimiento de administración
def admin_maintenance_required(view):
    """Decorator que verifica el estado de mantenimiento administrativo.

    Args:
        view: Función de vista a decorar

    Returns:
        Función decorada que verifica mantenimiento
    """

    def wrapped_view(*args, **kwargs):
        flag = auth.get_feature_flag("admin_maintenance_mode")
        usuario = buscar_usuario(usuario_actual())
        # SI no es usuario, no puede entrar.
        if not usuario:
            return redirect(url_for("auth.login"))
        if not usuario.s_user:
            abort(403)
        if flag and flag.enabled:
            flash(flag.maintenance_message, "warning")
        return view(*args, **kwargs)

    return wrapped_view
