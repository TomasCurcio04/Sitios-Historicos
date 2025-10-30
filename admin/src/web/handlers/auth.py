"""Manejadores de autenticación y autorización para la aplicación."""

from functools import wraps
from flask import session, redirect, url_for, flash
from src.core.services.auth.user_serv import buscar_usuario

def login_required(f):
    """Decorator que requiere autenticación para acceder a una ruta.
    
    Args:
        f: Función de vista a decorar
    
    Returns:
        Función decorada que verifica autenticación
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            flash("Por favor, inicia sesión para acceder a esta página.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

def is_authenticated(session):
    """Verifica si el usuario está autenticado.
    
    Args:
        session: Sesión de Flask
    
    Returns:
        True si el usuario está autenticado, False en caso contrario
    """
    return session.get("user") is not None

def is_admin(session):
    """Verifica si el usuario tiene rol de administrador.
    
    Args:
        session: Sesión de Flask
    
    Returns:
        True si el usuario es administrador, False en caso contrario
    """
    return int(session.get("role", 0)) == 1

def admin_required(f):
    """Decorator que requiere rol de administrador para acceder a una ruta.
    
    Args:
        f: Función de vista a decorar
    
    Returns:
        Función decorada que verifica rol de administrador
    """
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
