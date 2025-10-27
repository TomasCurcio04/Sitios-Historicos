from flask import Blueprint, render_template
from src.web.handlers.auth import login_required

# Creamos el blueprint principal
web = Blueprint("web", __name__, template_folder="templates", static_folder="static")

# Rutas del blueprint
@web.route("/", endpoint="home")
@login_required
def home():
    print("Entré aca en es usuario autenticado")
    return render_template("home.html")


@web.route("/gestionsitioshistoricos")
@login_required
def gestionsitioshistoricos():
    return render_template("gestionsitioshistoricos.html")


@web.route("/validacion_propuesta")
def validacion_propuesta():
    return render_template("validacion_propuesta.html")


@web.route("/moderacion_resenias")
def moderacion_resenias():
    return render_template("moderacion_resenias.html")


@web.route("/bajo_mantenimiento", endpoint="bajo_mantenimiento")
def bajo_mantenimiento():
    """Vista de mantenimiento administrativo."""
    return render_template("web.bajo_mantenimiento.html")