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
    SECRET_KEY = environ.get("SECRET_KEY")
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = "./flask_session_data"
    SESSION_PERMANENT = True
    SESSION_PERMANENT_LIFETIME = timedelta(minutes=20)
    CORS_ORIGINS = (
        environ.get("CORS_ORIGINS").split(",") if environ.get("CORS_ORIGINS") else []
    )
    CORS_RESOURCES = [r"/api/*"]
    CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"


class ProductionConfig(BaseConfig):
    """Production configuration class."""

    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    MINIO_BUCKET = environ.get("MINIO_BUCKET")

    SQLALCHEMY_ENGINES = {"default": environ.get("DATABASE_URL")}
    CORS_ORIGINS = (
        environ.get("CORS_ORIGINS").split(",") if environ.get("CORS_ORIGINS") else []
    )

    GOOGLE_CLIENT_ID = {"google-oauth": environ.get("GOOGLE_CLIENT_ID")}
    GOOGLE_CLIENT_SECRET = {"google-oauth": environ.get("GOOGLE_CLIENT_SECRET")}
    API_SERVER = environ.get("API_SERVER")


class TestingConfig(BaseConfig):
    """Testing configuration class."""

    TESTING = True
    SQLALCHEMY_ENGINES = {"default": "sqlite:///:memory:"}
    SECRET_KEY = "test_secret_key"
    JWT_SECRET_KEY = "test_jwt_secret"


class DevelopmentConfig(BaseConfig):
    """Development configuration class."""

    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    MINIO_BUCKET = environ.get("MINIO_BUCKET")
    SECRET_KEY = environ.get("SECRET_KEY")
    DB_USER = environ.get("DB_USER")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_NAME = environ.get("DB_NAME")
    DB_HOST = environ.get("DB_HOST")
    DB_PORT = environ.get("DB_PORT", "5432")
    DB_SCHEME = environ.get("DB_SCHEME", "postgresql+psycopg2")
    DEBUG = True
    DB_SSL_PARAMS = "sslmode=require&channel_binding=require"
    SQLALCHEMY_ENGINES = {
        "default": f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}{f'?{DB_SSL_PARAMS}' if DB_SSL_PARAMS else ''}"
    }
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")
    API_SERVER = environ.get("API_SERVER")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
