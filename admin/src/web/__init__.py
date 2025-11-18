# pylint: disable=import-error
"""Inicialización del módulo web de la aplicación Flask."""
import signal
import sys
import shutil
import os
from flask import (
    Flask,
    render_template,
    Blueprint,
    session as flask_session,
    request,
    redirect,
    url_for,
    flash,
)
from flask_session import Session
from sqlalchemy.exc import OperationalError
from admin.src.web.oauth import init_oauth
from src.web.handlers import error
from src.web.handlers.auth import (
    is_authenticated,
    template_is_authenticated,
    login_required,
    has_permission,
)
from src.web.handlers.utils import admin_maintenance_required, permissions_required
from src.web.controllers.web import web
from src.web.controllers.sites import bp as sites_bp
from src.web.controllers.tags import bp as tags_bp
from src.web.controllers.auth import bp as auth_bp
from src.web.controllers.users import user_bp
from src.web.controllers.feature_flags import feature_flags_bp
from src.web.controllers.mantenimiento_admin import mantenimiento_admin_bp
from src.web.controllers.mi_perfil import mi_perfil_bp
from src.web.controllers.resenias import bp as gestion_resenas_bp
from src.web.config import config
from src.web.storage import storage
from src.core.services.auth.bcrypt import bcrypt
from src.core import database
from src.core import seeds
from src.core.services.auth.user_serv import buscar_usuario, buscar_usuario_public
from src.core.services.auth.feature_flag_serv import get_feature_flag
from api.controllers.sites import bp as api_sites_bp
from api.controllers.reviews import bp as api_reviews_bp
from api.controllers.favorites import bp as api_favorites_bp
from api.controllers.me import bp as api_me_bp
from api.controllers.search import bp as api_search_bp
from api.controllers.auth import bp as api_auth_bp
from flask_cors import CORS
from src.web.controllers.auth_google import bp as google_auth_bp


server_session = Session()


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

    CORS(app, supports_credentials=True)

    app.secret_key = "supersecreto123"  # 🔒 Necesario para usar sesiones y flash()

    # Configuración
    app.config.from_object(config[env])

    print("GOOGLE_CLIENT_ID:", app.config.get("GOOGLE_CLIENT_ID"))
    print("GOOGLE_CLIENT_SECRET:", app.config.get("GOOGLE_CLIENT_SECRET"))

    # Inicialización de la base de datos
    database.init_db(app)
    # Inicializando Session
    server_session.init_app(app)
    # Inicializando Bcrypt
    bcrypt.init_app(app)
    # inicializo storage
    storage.init_app(app)
    # inicializo cors
    CORS(app)

    init_oauth(app)

    # --- 2. REGISTRA EL HELPER EN JINJA ---
    @app.context_processor
    def inject_permissions():
        """Hace que la función has_permission() esté disponible en todos los templates."""
        return dict(has_permission=has_permission)

    # --- FIN DEL REGISTRO ---
    # Register
    @app.cli.command("reset-db")
    def reset_db_command():
        """Comando CLI para reiniciar la base de datos.

        Elimina todas las tablas y las vuelve a crear.
        """
        database.reset_db()

    @app.cli.command("seed-db")
    def seed_db_command():
        """Comando CLI para llenar la base de datos con datos iniciales.

        Ejecuta el script de semillas para crear usuarios, roles,
        sitios y otros datos de prueba.
        """
        seeds.run()

    # Registrar blueprints
    app.register_blueprint(web)
    app.register_blueprint(sites_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(feature_flags_bp)
    app.register_blueprint(mantenimiento_admin_bp)
    app.register_blueprint(mi_perfil_bp)
    app.register_blueprint(api_sites_bp)
    app.register_blueprint(api_reviews_bp)
    app.register_blueprint(api_favorites_bp)
    app.register_blueprint(api_me_bp)
    app.register_blueprint(api_search_bp)
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(gestion_resenas_bp)
    app.register_blueprint(google_auth_bp)

    # Registrar manejadores de errores
    app.register_error_handler(404, error.not_found)
    app.register_error_handler(401, error.not_authorized)
    app.register_error_handler(500, error.internal_server_error)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(OperationalError, error.database_connection_error)

    app.jinja_env.globals["is_authenticated"] = template_is_authenticated

    @app.before_request
    def check_admin_maintenance():
        """Verifica si el panel administrativo está en modo de mantenimiento.

        Redirige a los usuarios no autenticados al login y a los usuarios
        no superusuarios a la página de mantenimiento cuando está activo.
        """
        user_dict = flask_session.get("user")
        usuario = None

        user_type = user_dict.get("type") if user_dict else None

        if user_type == "back":
            usuario = buscar_usuario(user_dict["email"])

        elif user_type == "google":
            usuario = buscar_usuario_public(user_dict["email"])

        flag = get_feature_flag("admin_maintenance_mode")
        exempt_endpoints = [
            "auth.login",
            "auth.logout",
            "auth.authenticate",
            "static",
            "feature_flags.feature_flags",
            "mantenimiento_admin.mantenimiento_admin",
            "api_sites.all_sites",
            "api_sites.get_site",
            "api_sites.create_site_endpoint",
            "api_reviews.get_site_reviews",
            "api_reviews.create_site_review",
            "api_reviews.get_site_review",
            "api_reviews.delete_site_review",
            "api_favorites.toggle_site_favorite_endpoint",
            "api_me.get_my_favorites",
            "api_search.search_nearby",
            "api_search.search_by_filters",
            "api_search.autocomplete_cities",
            "api_auth.get_token",
            "google_auth.google_login",
            "google_auth.login",
            "google_auth.auth",
            "google_auth.login",
            "google_auth.auth",
            "google_auth.logout",
            "google_auth.status",
        ]
        if request.endpoint in exempt_endpoints:
            return
        if not flag or not flag.enabled:
            if not usuario:
                return redirect(url_for("auth.login"))
            return
        if not usuario:
            return redirect(url_for("auth.login"))
        if not usuario.s_user:
            return redirect(url_for("mantenimiento_admin.mantenimiento_admin"))
        destino = url_for("feature_flags.feature_flags")
        if request.path != destino:
            return redirect(destino)
        return render_template("feature_flags.html", message=flag.maintenance_message)

    def cleanup_sessions(*args):
        """Borra todas las sesiones activas cuando se detiene la app."""
        session_dir = app.config.get("SESSION_FILE_DIR")
        if session_dir:
            if not os.path.isabs(session_dir):
                session_dir = os.path.join(os.getcwd(), session_dir)
            if os.path.exists(session_dir):
                try:
                    shutil.rmtree(session_dir)
                    os.makedirs(session_dir, exist_ok=True)
                    print("\n🧹 Se eliminaron todas las sesiones activas.")
                except Exception as e:
                    print(f"\n⚠️ Error al limpiar sesiones: {e}")
        else:
            print("\n⚠️ No se encontró SESSION_FILE_DIR en la configuración.")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup_sessions)

    return app
