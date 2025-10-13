# pylint: disable=import-error
"""Módulo controlador de feature flags"""

from flask import request, render_template, redirect, url_for, flash, Blueprint, session
import logging
from src.core.database import db
from src.web.utils import admin_maintenance_required
from src.core import auth

feature_flags_bp = Blueprint("feature_flags", __name__, url_prefix="/featureflags")


@feature_flags_bp.route("/", methods=["GET", "POST"], endpoint="feature_flags")
@admin_maintenance_required
def feature_flags():
    """Vista del menu de feature flags."""
    flags = auth.list_feature_flags()
    try:
        usuario = auth.buscar_usuario(session.get("user"))
        print(f"usuario: {usuario}")
    except Exception as e:
        print(f"Error al buscar usuario: {e}")

    usuario_id = usuario.id_user if usuario else 1
    print(f"usuario_id: {usuario_id}")
    if request.method == "POST":
        for flag in flags:
            flag.enabled = f"enabled_{flag.id}" in request.form
            flag.maintenance_message = request.form.get(f"mensaje_{flag.id}", "")
            flag.updated_by = usuario_id
        db.session.commit()
        flash("Feature flags actualizados correctamente", "success")
        return redirect(url_for("feature_flags.feature_flags"))

    return render_template("feature_flags.html", flags=flags)
