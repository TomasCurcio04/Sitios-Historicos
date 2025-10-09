# pylint: disable=import-error
"""Utilidades para la aplicación web."""

from flask import render_template, flash
from src.core import auth


# Middleware para modo mantenimiento de administración
def admin_maintenance_required(view):
    """Decorator para verificar el estado de mantenimiento de la administración."""

    def wrapped_view(*args, **kwargs):
        flag = auth.get_feature_flag("admin_maintenance_mode")
        print(flag)
        if flag and flag.enabled:
            # if not getattr(current_user, "is_sysadmin", False):
            flash(flag.maintenance_message or "Mantenimiento", "warning")
            return render_template(
                "mantenimiento_admin.html", message=flag.maintenance_message
            )
        return view(*args, **kwargs)

    return wrapped_view
