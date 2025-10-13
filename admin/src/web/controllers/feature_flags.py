# pylint: disable=import-error
"""Módulo controlador de feature flags"""

from flask import request, render_template, redirect, url_for, flash, Blueprint, session
from src.web.utils import admin_maintenance_required
from src.core import auth

feature_flags_bp = Blueprint("feature_flags", __name__, url_prefix="/featureflags")


@feature_flags_bp.route("/", methods=["GET", "POST"], endpoint="feature_flags")
@admin_maintenance_required
def feature_flags():
    """Vista del menu de feature flags."""
    flags = auth.list_feature_flags()
    usuario = auth.buscar_usuario(session.get("user"))
    usuario_id = usuario.id_user if usuario else 1
    print(f"usuario_id: {usuario_id}")
    if request.method == "POST":
        flags_data = {}
        for flag in flags:
            flags_data[str(flag.id)] = {
                "enabled": f"enabled_{flag.id}" in request.form,
                "maintenance_message": request.form.get(f"mensaje_{flag.id}", ""),
            }
        has_changes = auth.update_feature_flags(flags_data, usuario_id)
        if has_changes:
            flash("Feature flags actualizados correctamente", "success")
        else:
            flash("No se detectaron cambios", "info")
        return redirect(url_for("feature_flags.feature_flags"))

    return render_template("feature_flags.html", flags=flags)
