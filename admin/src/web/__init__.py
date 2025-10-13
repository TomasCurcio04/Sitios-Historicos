# pylint: disable=import-error
"""Inicialización del módulo web de la aplicación Flask."""
from flask import (
    Flask,
    render_template,
    Blueprint,
    session as current_user,
    request,
    redirect,
    url_for,
    flash,
)
from flask_session import Session
import os
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp
from src.web.controllers.tags import bp as tags_bp
from src.web.controllers.busqueda_avanzada import bp as busqueda_avanzada_bp
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.users import user_bp
from src.web.controllers.feature_flags import bp as feature_flags_bp

from src.core.auth.bcrypt import bcrypt
from src.web.handlers.auth import is_authenticated
from src.web.config import config
from src.core import database
from src.core import seeds
from src.web.utils import admin_maintenance_required
from src.core import auth

# Creamos el blueprint principal
web = Blueprint("web", __name__, template_folder="templates", static_folder="static")

session = Session()


# Rutas del blueprint
@web.route("/", endpoint="home")
def home():
    if not is_authenticated(current_user):
        print("Entré aca en no es usuario autenticado")
        return render_template("login.html")
    print("Entré aca en es usuario autenticado")
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


# @web.route("/feature_flags", methods=["GET", "POST"], endpoint="feature_flags")
# @admin_maintenance_required
# def feature_flags():
#     """Vista del menu de feature flags."""
#     # flags = auth.list_feature_flags()
#     # usuario_id = current_user.get("user_id")

#     # if request.method == "POST":
#     #     for flag in flags:
#     #         flag.enabled = f"enabled_{flag.id}" in request.form
#     #         flag.maintenance_message = request.form.get(f"mensaje_{flag.id}", "")
#     #         flag.updated_by = usuario_id
#     #     database.db.session.commit()
#     #     flash("Feature flags actualizados correctamente", "success")
#     #     return redirect(url_for("web.feature_flags"))

#     return render_template("feature_flags.html")  # , flags=flags


@web.route("/feature_flags", methods=["GET", "POST"], endpoint="feature_flags")
@admin_maintenance_required
def feature_flags():
    """Vista del menu de feature flags."""
    flags = auth.list_feature_flags()
    usuario_id = current_user.get("user_id") or current_user.get("id") or 1

    if request.method == "POST":
        for flag in flags:
            flag.enabled = f"enabled_{flag.id}" in request.form
            flag.maintenance_message = request.form.get(f"mensaje_{flag.id}", "")
            flag.updated_by = usuario_id or 1
        database.db.session.commit()
        flash("Feature flags actualizados correctamente", "success")
        return redirect(url_for("web.feature_flags"))

    return render_template("feature_flags.html", flags=flags)


@web.route("/mantenimiento_admin", endpoint="mantenimiento_admin")
def mantenimiento_admin():
    """Vista de mantenimiento administrativo."""
    return render_template("feature_flags.html")


@web.route("/test_flash")
def test_flash():
    flash("Mensaje de prueba", "success")
    return redirect(url_for("web.bajo_mantenimiento"))


# @admin_maintenance_required
@web.route("/bajo_mantenimiento", endpoint="bajo_mantenimiento")
def bajo_mantenimiento():
    """Vista de mantenimiento administrativo."""
    return render_template("web.bajo_mantenimiento.html")


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
    # app.config.from_mapping(
    #     DEBUG=True,
    #     TESTING=False,
    #     DB_HOST="nozomi.proxy.rlwy.net",
    #     DB_NAME="railway",
    #     DB_USER="postgres",
    #     DB_PASSWORD="KcooNtcHPuxNsQSXpQfMuUiVpmEFaeYm",
    #     DB_PORT="55215",
    #     DB_SCHEME="postgresql+psycopg2",
    # )

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
    app.register_blueprint(feature_flags_bp)

    app.jinja_env.globals["is_authenticated"] = is_authenticated

    @app.before_request
    def check_admin_maintenance():

        flag = auth.get_feature_flag("admin_maintenance_mode")
        if not flag or not flag.enabled:
            return

        exempt_endpoints = [
            "auth.login",
            "auth.logout",
            "auth.authenticate",
            "static",
            "web.feature_flags",
        ]

        if request.endpoint in exempt_endpoints:
            return
        usuario = auth.buscar_usuario(current_user.get("user"))
        print("busque el usuario")
        if not usuario:
            print("no es usuario")
            return render_template("login.html", message=flag.maintenance_message)
        if not getattr(usuario, "s_user", True):
            print(f"{usuario} No es sysadmin")
            return render_template(
                "bajo_mantenimiento.html", message=flag.maintenance_message
            )
        if getattr(usuario, "s_user", True):
            destino = url_for("web.feature_flags")
            if request.path != destino:
                return redirect(destino)

        return render_template("feature_flags.html", message=flag.maintenance_message)

    return app
