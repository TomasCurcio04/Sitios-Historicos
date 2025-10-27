# pylint: disable=import-error
"""Modelo de categoría para la tabla 'category' en la base de datos."""
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.core.database import Base


if TYPE_CHECKING:
    from src.core.entity.site import Site


class Category(Base):
    """Modelo de categoría para la tabla 'category'."""

    __tablename__ = "category"

    id_category: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    sites: Mapped[list["Site"]] = relationship(back_populates="category_rel")

    def __repr__(self):
        return f"<Category(id_category={self.id_category}, name='{self.name}', description='{self.description}')>"
