"""Controlador del perfil del usuario actual."""

from flask import Blueprint, render_template, redirect, url_for, flash, session
from src.core.services.auth.user_serv import buscar_usuario
from src.web.handlers.auth import login_required

mi_perfil_bp = Blueprint("mi_perfil", __name__, url_prefix="/mi_perfil")


@mi_perfil_bp.route("/", methods=["GET"])
@login_required
def perfil():
    """Muestra el perfil del usuario actual."""

    user_data = session.get("user")

    if not user_data:
        flash("Debes iniciar sesión para ver tu perfil", "error")
        return redirect(url_for("auth.login"))
    
    email = user_data["email"]

    user = buscar_usuario(email)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("auth.login"))

    return render_template("user_profile.html", user=user)
