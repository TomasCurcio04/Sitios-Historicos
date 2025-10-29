"""Controlador de autenticación para login y logout de usuarios."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from src.core.services.auth.user_serv import verificar_usuario

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/")
def login():
    """Muestra la página de login."""
    return render_template("login.html")

@bp.get("/logout") 
def logout():
    """Cierra la sesión del usuario actual."""
    if session.get("user"):
        session.pop("user")
        session.clear()
        flash("Cierre de sesión exitoso", "success")
    else:
        flash("No hay una sesión activa", "error")
    return redirect(url_for('auth.login'))        

@bp.post("/authenticate")
def authenticate():
    """Autentica las credenciales del usuario e inicia sesión."""
    params = request.form

    user,error = verificar_usuario(params["email"], params["password"])
    if not user:
        flash(error, "error")    
        return redirect(url_for('auth.login'))
    
    session["user"] = user.email
    session["user_name"] = user.user_name
    session["role"] = int(user.role)
    flash("Inicio de sesión exitoso", "success")
    return redirect(url_for('users.user_profile'))
