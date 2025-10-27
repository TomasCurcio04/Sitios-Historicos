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
from src.web.controllers.web import web
from src.web.controllers.sites import bp as sites_bp
from src.web.controllers.tags import bp as tags_bp
from src.web.controllers.busqueda_avanzada import bp as busqueda_avanzada_bp
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.users import user_bp
from src.web.controllers.feature_flags import feature_flags_bp
from src.web.controllers.mantenimiento_admin import mantenimiento_admin_bp

from src.core.services.auth.bcrypt import bcrypt
from src.web.handlers.auth import is_authenticated
from src.web.config import config
from src.core import database
from src.core import seeds
from src.web.handlers.utils import admin_maintenance_required
from src.core.services import auth
from src.web.handlers.auth import login_required
from src.web.handlers.utils import permissions_required

session = Session()


def create_app(env="development", static_folder=None):
    """Crea y devuelve la aplicación Flask según el entorno."""

    # Determinar entorno por variable de entorno FLASK_ENV (por defecto 'development')
    env = os.environ.get("FLASK_ENV", "development")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    if static_folder is None:
        static_folder = os.path.abspath(os.path.join(base_dir, "..", "..", "static"))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=static_folder,
    )

    app.secret_key = "supersecreto123"  # 🔒 Necesario para usar sesiones y flash()

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
    app.register_blueprint(sites_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(busqueda_avanzada_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(feature_flags_bp)
    app.register_blueprint(mantenimiento_admin_bp)

    app.jinja_env.globals["is_authenticated"] = is_authenticated

    @app.before_request
    def check_admin_maintenance():
        """Verifica si el usuario está en modo de mantenimiento administrativo."""
        current_user.setdefault("user", None)
        """Verifica si el usuario está en modo de mantenimiento administrativo."""
        current_user.setdefault("user", None)
        # Agregar user_name a sesiones existentes que no lo tengan
        if "user" in current_user and "user_name" not in current_user:
            usuario = auth.buscar_usuario(current_user.get("user"))
            if usuario:
                current_user["user_name"] = usuario.user_name
                current_user["user_name"] = usuario.user_name
        usuario = auth.buscar_usuario(current_user.get("user"))
        print(f"current_user: {current_user.get('user')}")
        flag = auth.get_feature_flag("admin_maintenance_mode")
        exempt_endpoints = [
            "auth.login",
            "auth.logout",
            "auth.authenticate",
            "static",
            "feature_flags.feature_flags",
            "mantenimiento_admin.mantenimiento_admin",
        ]
        if request.endpoint in exempt_endpoints:
            print("request")
            return
        if not flag or not flag.enabled:
            if not usuario:
                print("no usuario")
                return redirect(url_for("auth.login"))
            return
        if not usuario:
            return redirect(url_for("auth.login"))
        print(f"Usuario s_user: {usuario.s_user}")
        if not usuario.s_user:
            return redirect(url_for("mantenimiento_admin.mantenimiento_admin"))
        print(f"{usuario} Es sysadmin")
        destino = url_for("feature_flags.feature_flags")
        if request.path != destino:
            return redirect(destino)
        return render_template("feature_flags.html", message=flag.maintenance_message)

    return app
