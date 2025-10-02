"""Configuration classes for different environments."""
from os import environ

class Config:
    """Base configuration class."""
    TESTING = False
    DEBUG = False
    SECRET_KEY = "your_secret_key"
    SESSION_TYPE = "filesystem"

class ProductionConfig(Config):
    """Production configuration class."""
    SQLALCHEMY_ENGINES = {
        "default": environ.get("DATABASE_URL") 
    }

class DevelopmentConfig(Config):
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
        "default": f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    }
config = {
    "development": DevelopmentConfig,           
    "production": ProductionConfig,
    "default": DevelopmentConfig    
}