"""Módulo para la configuración y manejo de la base de datos SQLAlchemy en una aplicación Flask."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()
"""Inicializa la base de datos SQLAlchemy."""


def init_db(app):
    """Inicializa la base de datos SQLAlchemy con la aplicación Flask."""
    db.init_app(app)
    return db


def reset_db():
    """Reinicia la base de datos eliminando todas las tablas y volviéndolas a crear."""
    from auth.user import Users  # noqa: F401

    print("Reiniciando la base de datos...")
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("✔️Base de datos reiniciada.")


class Base(DeclarativeBase):
    """Clase base para los modelos de la base de datos."""
