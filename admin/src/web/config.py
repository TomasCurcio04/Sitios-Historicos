"""Configuration classes for different environments."""

# from os import environ
from datetime import timedelta
from os import environ
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env

class BaseConfig:
    """Base configuration class."""

    TESTING = False
    DEBUG = False
    SECRET_KEY = "your_secret_key"
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = "./flask_session_data"
    SESSION_PERMANENT = True
    SESSION_PERMANENT_LIFETIME = timedelta(minutes=20)
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'


class ProductionConfig(BaseConfig):
    """Production configuration class."""
    MINIO_SERVER = environ.get("MINIO_SERVER", "minio:9000")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY", "VutZt4djr4TvVvU6e9ai")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY", "uCNf8TFkB6kAxMEBGPIJI9GoOXNLU2D7pFvigvM0")
    MINIO_SECURE = True
    MINIO_BUCKET = "grupo10"

    SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
    # {"default": "postgresql+psycopg2://grupo10:GtGouFR0ONveaoqQKi31@127.0.0.1:5432/grupo10?options=-c%20search_path=postgres" }
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")

class DevelopmentConfig(BaseConfig):
    """Development configuration class."""
    MINIO_SERVER = "minio.proyecto2025.linti.unlp.edu.ar" # <-- CAMBIADO
    MINIO_ACCESS_KEY = "VutZt4djr4TvVvU6e9ai"
    MINIO_SECRET_KEY = "uCNf8TFkB6kAxMEBGPIJI9GoOXNLU2D7pFvigvM0"
    MINIO_SECURE = True # <-- CAMBIADO
    MINIO_BUCKET = "grupo10"
    # SECRET_KEY = "your_dev_secret_key"
    # DB_USER = "postgres"
    # DB_PASSWORD = "KcooNtcHPuxNsQSXpQfMuUiVpmEFaeYm"
    # DB_NAME = "railway"
    # DB_HOST = "nozomi.proxy.rlwy.net"
    # DB_PORT = "55215"
    # DB_SCHEME = "postgresql+psycopg2"
    # DEBUG = True
    SECRET_KEY = "your_dev_secret_key"
    DB_USER = "neondb_owner"
    DB_PASSWORD = "npg_RAUO1X2TMZad"
    DB_NAME = "neondb"
    DB_HOST = "ep-red-river-a828fhqc-pooler.eastus2.azure.neon.tech"
    DB_PORT = "5432"
    DB_SCHEME = "postgresql+psycopg2"
    DEBUG = True
    DB_SSL_PARAMS = "sslmode=require&channel_binding=require"
    SQLALCHEMY_ENGINES = {
        "default": f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}{f'?{DB_SSL_PARAMS}' if DB_SSL_PARAMS else ''}"
        # "default": "postgresql+psycopg2://neondb_owner:npg_RAUO1X2TMZad@ep-red-river-a828fhqc-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
    }
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")



config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
