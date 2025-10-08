from dataclasses import dataclass
from flask import Flask
from flask import render_template


@dataclass
class Error:
    code: int
    message: str
    description: str


def not_found(error):
    err = Error(
        code=404,
        message="Página no encontrada",
        description="No se encontró la página solicitada.",
    )
    return render_template("error.html", error=err), 404


def not_authorized(error):
    err = Error(
        code=401,
        message="No autorizado",
        description="No tienes permiso para acceder a esta página.",
    )
    return render_template("error.html", error=err), 401


def internal_server_error(error):
    err = Error(
        code=500,
        message="Error interno del servidor",
        description="Ocurrió un error inesperado en el servidor.",
    )
    return render_template("error.html", error=err), 500
