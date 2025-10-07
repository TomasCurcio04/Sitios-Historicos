from flask import Blueprint, flash, redirect, render_template, request, session
from src.core.auth import servicios
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/")
def login():
    return render_template("login.html")

@bp.get("/logout") 
def logout():
    pass

@bp.post("/authenticate")
def authenticate():
    params = request.form

    user = servicios.buscar_usuario(params.get("email"), params.get("password"))
    if not user:
        flash("Email o contraseñas incorrecto", "error")
        return redirect("login.html", error="Credenciales inválidas")
    
    session["user"] = user.email
    flash("Inicio de sesión exitoso", "success")
    return redirect("home.html")