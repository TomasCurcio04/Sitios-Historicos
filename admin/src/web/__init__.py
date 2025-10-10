# pylint: disable=import-error
"""Inicialización del módulo web de la aplicación Flask."""
from flask import Flask, render_template, Blueprint
from flask_session import Session
import os
from flask import Flask, render_template, Blueprint
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp
from src.web.controllers.tags import bp as tags_bp
from src.web.controllers.busqueda_avanzada import bp as busqueda_avanzada_bp
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.users import user_bp
from src.core.auth.bcrypt import bcrypt
from src.web.handlers.auth import is_authenticated
from src.web.config import config
from src.core import database
from src.core import seeds
from src.web.utils import admin_maintenance_required

# Creamos el blueprint principal
web = Blueprint("web", __name__, template_folder="templates", static_folder="static")

session = Session()


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

    app.secret_key = "supersecreto123"  # 🔒 Necesario para usar sesiones y flash()
    # Configuración de la app
    app.config.from_mapping(
        DEBUG=True,
        TESTING=False,
        DB_HOST="nozomi.proxy.rlwy.net",
        DB_NAME="railway",
        DB_USER="postgres",
        DB_PASSWORD="KcooNtcHPuxNsQSXpQfMuUiVpmEFaeYm",
        DB_PORT="55215",
        DB_SCHEME="postgresql+psycopg2",
    )

    # Configuración
    app.config.from_object(config[env])

    # Inicialización de la base de datos
    database.init_db(app)
    # Inicializando Session
    session.init_app(app)
    # Inicializando Bcrypt
    bcrypt.init_app(app)

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
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(busqueda_avanzada_bp)
    app.register_blueprint(tags_bp)

    # Comando CLI para reiniciar la base de datos
    @app.cli.command("reset-db")
    def reset_db_command():
        """Reinicia la base de datos de forma segura."""
        database.reset_db()

    app.jinja_env.globals["is_authenticated"] = is_authenticated

    return app
