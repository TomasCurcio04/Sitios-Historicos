"""Módulo para la configuración y manejo de la base de datos SQLAlchemy en una aplicación Flask."""
from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()
"""Inicializa la base de datos SQLAlchemy."""
def init_db(app):
    """Inicializa la base de datos SQLAlchemy con la aplicación Flask."""
    db.init_app(app)
    return db

class Base(DeclarativeBase):
    """Clase base para los modelos de la base de datos."""
