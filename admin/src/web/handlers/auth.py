"""Manejadores de autenticación y autorización para la aplicación."""

from functools import wraps
from flask import session, redirect, url_for, flash
from src.core.services.auth.user_serv import buscar_usuario


def login_required(f):
    """Decorator que requiere autenticación para acceder a una ruta."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            flash("Por favor, inicia sesión para acceder a esta página.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def is_authenticated(session):
    """Verifica si el usuario está autenticado."""
    return session.get("user") is not None


def template_is_authenticated():
    """Función wrapper para usar is_authenticated en templates sin parámetros."""
    from flask import session

    return is_authenticated(session)


def is_admin(session):
    """Verifica si el usuario tiene rol de administrador."""
    return int(session.get("role", 0)) == 1


def admin_required(f):
    """Decorator que requiere rol de administrador para acceder a una ruta."""

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


def has_permission(permission_name):
    """Verifica si el usuario actual tiene un permiso específico guardado en la sesión.

    Args:
        permission_name (str): Nombre del permiso a verificar.

    Returns:
        bool: True si el permiso está presente en la sesión, False en caso contrario.
    """
    # Lee la lista de permisos que guardamos en la sesión durante el login
    permissions = session.get("permissions", [])
    return permission_name in permissions


# --- ¡ESTO ES LO NUEVO QUE NECESITAMOS! ---
def permission_required(permission_name):
    """Decorator para restringir acceso a usuarios que tengan un permiso específico.

    Args:
        permission_name (str): El nombre del permiso requerido (ej: "site_edit").

    Returns:
        function: Decorador que envuelve la función original y realiza las comprobaciones
        de autenticación y permiso, devolviendo la respuesta o redirección correspondiente.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. Verificamos si está logueado
            if not is_authenticated(session):
                flash("Por favor, inicia sesión para acceder a esta página.", "warning")
                return redirect(url_for("auth.login"))

            # 2. Verificamos el permiso usando nuestra función helper
            if not has_permission(permission_name):
                flash(
                    f"No tenés permisos para acceder a esta sección ({permission_name}).",
                    "danger",
                )
                return redirect(url_for("web.home"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
