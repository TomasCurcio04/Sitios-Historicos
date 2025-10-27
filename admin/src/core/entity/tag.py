# pylint: disable=import-error
"""Modelo de etiqueta para la tabla 'tag' en la base de datos."""
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from src.core.database import Base
# from src.core.entity.site import site_tag  # Se define en site.py
import unicodedata

if TYPE_CHECKING:
    from src.core.entity.site import Site


class Tag(Base):
    """Modelo de etiqueta para la tabla 'tag'."""

    __tablename__ = "tag"
    id_tag: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    date_created: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    sites: Mapped[list["Site"]] = relationship(
    "Site",
    secondary="site_tag",
    back_populates="tag"
)

    def __init__(self, name: str):
        self.name = name
        self.slug = self.generate_slug(name)

    @staticmethod
    def generate_slug(name: str) -> str:
        # Quita acentos

        slug = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
        # Convierte a minúsculas y reemplaza espacios por guiones
        slug = slug.lower().replace(" ", "-")
        return slug
    
    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("El nombre es obligatorio")
        value = value.strip()
        if len(value) < 3 or len(value) > 50:
            raise ValueError("El nombre debe tener entre 3 y 50 caracteres")
        return value

    

    def __repr__(self):
        return f"<Tag(id_tag={self.id_tag}, name='{self.name}')>"
