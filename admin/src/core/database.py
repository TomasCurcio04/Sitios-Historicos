"""Módulo para la configuración y manejo de la base de datos SQLAlchemy en una aplicación Flask."""

# pylint: disable=import-error
# pylint: disable=import-outside-toplevel
# pylint: disable=unused-import

from flask_sqlalchemy_lite import SQLAlchemy  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import DeclarativeBase  # pyright: ignore[reportMissingImports]
from sqlalchemy import text  # pyright: ignore[reportMissingImports]

db = SQLAlchemy()
"""Inicializa la base de datos SQLAlchemy."""


def init_db(app):
    """Inicializa la base de datos SQLAlchemy con la aplicación Flask."""
    db.init_app(app)
    return db


def reset_db():
    """Reinicia la base de datos eliminando todas las tablas y volviéndolas a crear."""

    # from src.core.services.auth.users import Users  # noqa: F401
    # from src.core.services.board.site import Site  # noqa: F401
    # from src.core.services.board.category import Category  # noqa: F401
    # from src.core.services.board.state import State  # noqa: F401

    print("Reiniciando la base de datos...")
    Base.metadata.drop_all(bind=db.engine)
    # with db.engine.begin() as conn:
    #     conn.execute(text("DROP SCHEMA public CASCADE"))
    #     conn.execute(text("CREATE SCHEMA public"))

    Base.metadata.create_all(bind=db.engine)
    print("✔️  Base de datos reiniciada.")


class Base(DeclarativeBase):
    """Clase base para los modelos de la base de datos."""
