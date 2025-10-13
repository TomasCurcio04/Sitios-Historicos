from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorator para rutas que requieren autenticación."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            flash("Por favor, inicia sesión para acceder a esta página.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def is_authenticated(session):
    """Verifica que el usuario este autenticado."""
    return session.get("user") is not None

def is_admin(session):
    """Devuelve True si el usuario logueado tiene rol de administrador."""
    return int(session.get("role", 0)) == 1

def admin_required(f):
    """Decorator para rutas que requieren rol administrador."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            flash("Por favor, inicia sesión para acceder a esta página.", "warning")
            return redirect(url_for("auth.login"))
        if not is_admin(session):
            flash("No tenés permisos para acceder a esta sección.", "danger")
            return redirect(url_for("web.home"))
        return f(*args, **kwargs)
    return decorated_function