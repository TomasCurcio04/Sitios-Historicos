from flask import Flask
from src.core import database

def create_app():
    app = Flask(__name__)
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

    # Otros blueprints y configuraciones
    from src.web.controllers.issues import bp as issues_bp
    app.register_blueprint(issues_bp)

    # Comando CLI para reiniciar la base de datos
    @app.cli.command("reset-db")
    def reset_db_command():
        """Reinicia la base de datos de forma segura."""
        database.reset_db()

    return app