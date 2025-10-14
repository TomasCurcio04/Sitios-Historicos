"""Configuration classes for different environments."""

from os import environ


class BaseConfig:
    """Base configuration class."""

    TESTING = False
    DEBUG = False
    SECRET_KEY = "your_secret_key"
    SESSION_TYPE = "filesystem"


class ProductionConfig(BaseConfig):
    """Production configuration class."""

    SQLALCHEMY_ENGINES = {
        "default": "postgresql+psycopg2://grupo10:GtGouFR0ONveaoqQKi31@127.0.0.1:5432/grupo10?options=-c%20search_path=postgres"
    }
    # {"default": environ.get("DATABASE_URL")}


class DevelopmentConfig(BaseConfig):
    """Development configuration class."""

    SECRET_KEY = "your_dev_secret_key"
    DB_USER = "postgres"
    DB_PASSWORD = "KcooNtcHPuxNsQSXpQfMuUiVpmEFaeYm"
    DB_NAME = "railway"
    DB_HOST = "nozomi.proxy.rlwy.net"
    DB_PORT = "55215"
    DB_SCHEME = "postgresql+psycopg2"
    DEBUG = True
    SQLALCHEMY_ENGINES = {
        #  "default": "postgresql+psycopg2://grupo10:GtGouFR0ONveaoqQKi31@172.19.0.3:5432/grupo10?sslmode=require&channel_binding"
        # "default": f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        "default": "postgresql+psycopg2://neondb_owner:npg_RAUO1X2TMZad@ep-red-river-a828fhqc-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"
    }


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
