# pylint: disable=import-error
from flask import Flask, render_template, Blueprint
import os
from src.web.handlers import error
from src.web.controllers.issues import bp as issues_bp
from src.web.controllers.busqueda_avanzada import bp as busqueda_avanzada_bp
from src.web.config import config
from src.core import database
from src.core import seeds
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
        DB_HOST='nozomi.proxy.rlwy.net',
        DB_NAME='railway',
        DB_USER='postgres',
        DB_PASSWORD='KcooNtcHPuxNsQSXpQfMuUiVpmEFaeYm',
        DB_PORT='55215',
        DB_SCHEME='postgresql+psycopg2'
    )


    # Configuración
    app.config.from_object(config[env])

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
    app.register_blueprint(busqueda_avanzada_bp)

    # Comando CLI para reiniciar la base de datos
    @app.cli.command("reset-db")
    def reset_db_command():
        """Reinicia la base de datos de forma segura."""
        database.reset_db()

    return app