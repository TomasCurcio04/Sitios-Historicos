# pylint: disable=import-error
"""Módulo controlador de feature flags"""

from flask import render_template, Blueprint

mantenimiento_admin_bp = Blueprint(
    "mantenimiento_admin", __name__, url_prefix="/mantenimiento_admin"
)


@mantenimiento_admin_bp.route("/", methods=["GET"])
def mantenimiento_admin():
    """Vista de mantenimiento administrativo."""
    from src.core import auth
    flag = auth.get_feature_flag("admin_maintenance_mode")
    message = flag.maintenance_message if flag else None
    return render_template("mantenimiento_admin.html", message=message)
