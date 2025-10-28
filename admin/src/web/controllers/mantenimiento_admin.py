# pylint: disable=import-error
"""Controlador de página de mantenimiento administrativo."""

from flask import render_template, Blueprint

mantenimiento_admin_bp = Blueprint(
    "mantenimiento_admin", __name__, url_prefix="/mantenimiento_admin"
)


@mantenimiento_admin_bp.route("/", methods=["GET"])
def mantenimiento_admin():
    """Muestra la página de mantenimiento cuando está activo el modo mantenimiento.
    
    Returns:
        Página de mantenimiento o error 404 si no está activo
    """
    from src.core.services.auth.feature_flag_serv import get_feature_flag
    from flask import abort
    flag = get_feature_flag("admin_maintenance_mode")
    if not flag or not flag.enabled:
        abort(404)
    message = flag.maintenance_message if flag else None
    return render_template("mantenimiento_admin.html", message=message)
