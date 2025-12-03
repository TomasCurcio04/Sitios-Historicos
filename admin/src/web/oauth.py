"""Módulo para la configuración de OAuth en la aplicación Flask."""

from authlib.integrations.flask_client import OAuth
import os


oauth = OAuth()


def init_oauth(app):
    """Inicializa la configuración de OAuth para la aplicación Flask."""

    oauth.init_app(app)

    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url=app.config.get(
            "CONF_URL", "https://accounts.google.com/.well-known/openid-configuration"
        ),
        client_kwargs={"scope": "openid email profile"},
    )
