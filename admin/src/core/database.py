"""Módulo para la configuración y manejo de la base de datos SQLAlchemy en una aplicación Flask."""

from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()
"""Inicializa la base de datos SQLAlchemy."""


def init_db(app):
    """Inicializa la extensión SQLAlchemy con la aplicación Flask.

    Args:
        app (Flask): Instancia de la aplicación Flask.

    Returns:
        SQLAlchemy: Objeto db inicializado.
    """
    db.init_app(app)
    return db


def reset_db():
    """Reinicia la base de datos eliminando y recreando todas las tablas.

    Returns:
        Mensaje de confirmación.
    """

    # from src.core.entity.users import Users
    # from src.core.entity.site import Site
    # from src.core.entity.category import Category
    # from src.core.entity.state import State
    # from src.core.entity.site_image import SiteImage
    # from src.core.entity.site_history import SiteHistory
    # from src.core.entity.tag import Tag
    # from src.core.entity.role import Role
    # from src.core.entity.permission import Permission
    # from src.core.entity.feature_flag import FeatureFlag

    print("Reiniciando la base de datos...")
    Base.metadata.drop_all(bind=db.engine)
    # with db.engine.begin() as conn:
    #     conn.execute(text("DROP SCHEMA public CASCADE"))
    #     conn.execute(text("CREATE SCHEMA public"))

    Base.metadata.create_all(bind=db.engine)
    print("✔️  Base de datos reiniciada.")


class Base(DeclarativeBase):
    """Clase base para los modelos de la base de datos.

    Provee la base declarativa para los modelos SQLAlchemy.
    """
