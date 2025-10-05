# pylint: disable=import-error
"""Modelo de categoría para la tabla 'category' en la base de datos."""
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from src.core.database import Base


if TYPE_CHECKING:
    from src.core.board.site import Site


class Category(Base):
    """Modelo de categoría para la tabla 'category'."""

    __tablename__ = "category"

    id_category = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    site: Mapped[list["Site"]] = relationship(back_populates="category")
