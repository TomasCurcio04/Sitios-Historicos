# pylint: disable=import-error
"""Inicialización del módulo web de la aplicación Flask."""
import os
from flask import Flask, render_template, Blueprint
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp
from src.web.config import config
from src.core import database
from src.core import seeds
from src.web.utils import admin_maintenance_required

# from flask import redirect, url_for, flash, session

# Creamos el blueprint principal
web = Blueprint("web", __name__, template_folder="templates", static_folder="static")


# Rutas del blueprint
@web.route("/")
def home():
    return render_template("home.html")


@web.route("/gestionsitioshistoricos")
def gestionsitioshistoricos():
    return render_template("gestionsitioshistoricos.html")


@web.route("/validacion_propuesta")
def validacion_propuesta():
    return render_template("validacion_propuesta.html")


@web.route("/moderacion_resenias")
def moderacion_resenias():
    return render_template("moderacion_resenias.html")


@web.route("/gestion_usuarios")
def gestion_usuarios():
    return render_template("gestion_usuarios.html")


@web.route("/feature_flags", endpoint="feature_flags")
@admin_maintenance_required
def feature_flags():
    """Vista del menu de feature flags."""
    return render_template("feature_flags.html")


@web.route("/mantenimiento_admin", endpoint="mantenimiento_admin")
def mantenimiento_admin():
    """Vista de mantenimiento administrativo."""
    return render_template("mantenimiento_admin.html")


@web.before_request
def check_admin_maintenance():
    from src.core import auth
    from flask import request, redirect, url_for

    flag = auth.get_feature_flag("admin_maintenance_mode")
    if not flag or not flag.enabled:
        return

    exempt_endpoints = ["login", "static", "web.feature_flags"]
    if request.endpoint in exempt_endpoints:
        return
    usuario = auth.current_user()
    if not usuario.is_authenticated():
        return render_template(
            "mantenimiento_admin.html", message=flag.maintenance_message
        )

    if getattr(auth.current_user(), "s_user", False):
        # Si ya está en feature_flags, no redirigir
        if request.endpoint != "web.feature_flags":
            return redirect(url_for("web.feature_flags"))

    return render_template("mantenimiento_admin.html", message=flag.maintenance_message)


def create_app(env="development"):
    """Crea y devuelve la aplicación Flask según el entorno."""

    # Determinar entorno por variable de entorno FLASK_ENV (por defecto 'development')
    env = os.environ.get("FLASK_ENV", "development")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.abspath(os.path.join(base_dir, "..", "..", "static"))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=static_folder,
    )

    # Configuración
    app.config.from_object(config[env])
    print(app.config)

    # Inicialización de la base de datos
    database.init_db(app)

    # Register commands
    @app.cli.command("reset-db")
    def reset_db_command():
        """Reinicia la base de datos."""
        database.reset_db()

    @app.cli.command("seed-db")
    def seed_db_command():
        """Llena la base de datos con datos iniciales."""
        seeds.run()

    # Registrar blueprints
    app.register_blueprint(web)
    app.register_blueprint(issues_bp)

    # Manejo de errores
    app.register_error_handler(404, error.not_found)
    app.register_error_handler(401, error.not_authorized)
    app.register_error_handler(500, error.internal_server_error)

    return app
