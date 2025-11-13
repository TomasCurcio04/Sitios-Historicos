"""Controlador principal de la aplicación web."""

from flask import Blueprint, render_template
from src.web.handlers.auth import login_required

# Creamos el blueprint principal
web = Blueprint("web", __name__, template_folder="templates", static_folder="static")

# Rutas del blueprint
@web.route("/", endpoint="home")
@login_required
def home():
    """Página principal del panel administrativo."""
    print("Entré aca en es usuario autenticado")
    return render_template("home.html")




@web.route("/validacion_propuesta")
def validacion_propuesta():
    """Página de validación de propuestas de sitios."""
    return render_template("validacion_propuesta.html")




@web.route("/bajo_mantenimiento", endpoint="bajo_mantenimiento")
def bajo_mantenimiento():
    """Página mostrada durante el mantenimiento administrativo."""
    return render_template("web.bajo_mantenimiento.html")
