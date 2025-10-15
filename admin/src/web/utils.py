# pylint: disable=import-error
"""Utilidades para la aplicación web."""

from flask import flash, session as current_user, abort, redirect, url_for
from src.core import auth


# Middleware para modo mantenimiento de administración
def admin_maintenance_required(view):
    """Decorator para verificar el estado de mantenimiento de la administración."""

    def wrapped_view(*args, **kwargs):
        flag = auth.get_feature_flag("admin_maintenance_mode")
        usuario = auth.buscar_usuario(current_user.get("user"))
        # SI no es usuario, no puede entrar.
        if not usuario:
            return redirect(url_for("auth.login"))

        # Si el flag está activado, solo s_user puede entrar
        if flag and flag.enabled:
            if not usuario.s_user:
                abort(403)
        flash(flag.maintenance_message or "Mantenimiento", "warning")
        return view(*args, **kwargs)

    return wrapped_view


def usuario_actual():
    """Obtiene el usuario actual."""
    if not current_user.get("usuario_id"):
        return None
    usuario_id = current_user.get("usuario_id")
    if usuario_id:
        return auth.obtener_usuario_por_id(usuario_id)
    return None
