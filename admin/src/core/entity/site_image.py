# pylint: disable=import-error
"""Modelo de imagen de sitio para la tabla site_image en la base de datos"""
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.entity.site import Site


class SiteImage(Base):
    """Modelo de imagen de sitio para la tabla site_image en la base de datos"""

    __tablename__ = "site_image"
    id_site_image: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_site: Mapped[int] = mapped_column(ForeignKey("site.id_site"), nullable=False)
    site_rel: Mapped["Site"] = relationship(back_populates="images")
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    file_path: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(120), nullable=False)
    is_thumbnail: Mapped[bool] = mapped_column(default=False)
    display_order: Mapped[int] = mapped_column(default=0)
    date_registered: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<SiteImage(title='{self.title}', file_path='{self.file_path}', is_thumbnail={self.is_thumbnail})>"
