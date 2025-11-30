"""Modelo de usuario público para la tabla 'public_user' en la base de datos."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Text
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.entity.review import Review
    from src.core.entity.site_favorite import SiteFavorite


class PublicUser(Base):
    """Modelo de usuario público para la tabla 'public_user'."""

    __tablename__ = "public_user"

    id_public_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Información de Google
    google_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    picture: Mapped[str] = mapped_column(Text, nullable=True)

    # Fechas
    date_created: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relaciones
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="public_user_rel"
    )
    favorites: Mapped[list["SiteFavorite"]] = relationship(
        "SiteFavorite", back_populates="public_user_rel"
    )

    def __repr__(self):
        return f"<PublicUser(name='{self.name}', email='{self.email}')>"
