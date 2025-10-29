"""Manejadores de errores HTTP para la aplicación."""

from dataclasses import dataclass
from flask import Flask
from flask import render_template


@dataclass
class Error:
    """Clase para representar errores HTTP."""

    code: int
    message: str
    description: str


def not_found(error):
    """Manejador para errores 404 - Página no encontrada."""
    err = Error(
        code=404,
        message="Página no encontrada",
        description="No se encontró la página solicitada.",
    )
    return render_template("error.html", error=err), 404


def not_authorized(error):
    """Manejador para errores 401 - No autorizado."""
    err = Error(
        code=401,
        message="No autorizado",
        description="No tienes permiso para acceder a esta página.",
    )
    return render_template("error.html", error=err), 401


def internal_server_error(error):
    """Manejador para errores 500 - Error interno del servidor."""
    err = Error(
        code=500,
        message="Error interno del servidor",
        description="Ocurrió un error inesperado en el servidor.",
    )
    return render_template("error.html", error=err), 500


def forbidden(error):
    """Manejador para errores 403 - Prohibido."""
    err = Error(
        code=403,
        message="Prohibido",
        description="No tienes permiso para acceder a esta página.",
    )
    return render_template("error.html", error=err), 403
