# pylint: disable=import-error
"""Módulo controlador de feature flags"""

from flask import request, render_template, redirect, url_for, flash, Blueprint, session

from src.core.database import db
from src.web.utils import admin_maintenance_required
from src.core import auth

bp = Blueprint("feature_flags", __name__, url_prefix="/featureflags")


@bp.route("/feature_flags", methods=["GET", "POST"])
@admin_maintenance_required
def feature_flags():
    """Vista del menu de feature flags."""
    flags = auth.list_feature_flags()
    usuario_id = session.get("user_id")

    if request.method == "POST":
        for flag in flags:
            flag.enabled = f"enabled_{flag.id}" in request.form
            flag.maintenance_message = request.form.get(f"mensaje_{flag.id}", "")
            flag.updated_by = usuario_id
        db.session.commit()
        flash("Feature flags actualizados correctamente", "success")
        return redirect(url_for("feature_flags.feature_flags"))

    return render_template("feature_flags.html", flags=flags)
