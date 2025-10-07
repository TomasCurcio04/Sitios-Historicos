from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from src.core.auth.__init__ import verificar_usuario

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

    user = verificar_usuario(params["email"], params["password"])
    if not user:
        flash("Email o contraseñas incorrecto", "error")    
        return redirect(url_for('auth.login'))
    
    session["user"] = user.email
    flash("Inicio de sesión exitoso", "success")
    return redirect(url_for('users.user_index'))