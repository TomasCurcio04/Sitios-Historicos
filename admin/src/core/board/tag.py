# pylint: disable=import-error
"""Modelo de etiqueta para la tabla 'tag' en la base de datos."""
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.board.site import Site


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

    def __repr__(self):
        return f"<Tag(id_tag={self.id_tag}, name='{self.name}')>"
