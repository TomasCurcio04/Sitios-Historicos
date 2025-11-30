"""Modelo de reseña para la tabla 'review' en la base de datos."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Enum
from src.core.database import Base
import enum

if TYPE_CHECKING:
    from src.core.entity.site import Site
    from src.core.entity.users import Users
    from src.core.entity.public_user import PublicUser


class ReviewStatus(enum.Enum):
    """Estados posibles de una reseña."""

    PENDIENTE = "Pendiente"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"


class Review(Base):
    """Modelo de reseña para la tabla 'review'."""

    __tablename__ = "review"

    id_review: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Relación con sitio
    id_site: Mapped[int] = mapped_column(ForeignKey("site.id_site"), nullable=False)
    site_rel: Mapped["Site"] = relationship("Site", back_populates="reviews")

    # Relación con usuario público
    id_public_user: Mapped[int] = mapped_column(
        ForeignKey("public_user.id_public_user"), nullable=False
    )
    public_user_rel: Mapped["PublicUser"] = relationship(
        "PublicUser", back_populates="reviews"
    )

    # Contenido de la reseña
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Estado y moderación
    status: Mapped[ReviewStatus] = mapped_column(
        Enum(ReviewStatus), nullable=False, default=ReviewStatus.PENDIENTE
    )
    rejection_reason: Mapped[str] = mapped_column(String(200), nullable=True)

    # Fechas
    date_created: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
    )
    date_moderated: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Usuario que moderó
    moderated_by: Mapped[int] = mapped_column(
        ForeignKey("users.id_user"), nullable=True
    )
    moderator_rel: Mapped["Users"] = relationship(
        "Users", back_populates="moderated_reviews"
    )

    def __repr__(self):
        return f"<Review(site={self.id_site}, user={self.id_public_user}, rating={self.rating}, status={self.status.value})>"
