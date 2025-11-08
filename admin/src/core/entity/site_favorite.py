# pylint: disable=import-error
"""Modelo de sitios favoritos para la tabla 'site_favorite' en la base de datos."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.entity.site import Site
    from src.core.entity.public_user import PublicUser


class SiteFavorite(Base):
    """Modelo de sitios favoritos para la tabla 'site_favorite'."""

    __tablename__ = "site_favorite"

    id_site: Mapped[int] = mapped_column(ForeignKey("site.id_site"), primary_key=True)
    id_public_user: Mapped[int] = mapped_column(ForeignKey("public_user.id_public_user"), primary_key=True)
    
    # Fecha cuando se marcó como favorito
    date_added: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    # Relaciones
    site_rel: Mapped["Site"] = relationship("Site", back_populates="favorites")
    public_user_rel: Mapped["PublicUser"] = relationship("PublicUser", back_populates="favorites")

    def __repr__(self):
        return f"<SiteFavorite(site={self.id_site}, user={self.id_public_user})>"