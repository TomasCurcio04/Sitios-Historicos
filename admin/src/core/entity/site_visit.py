"""Modelo de visitas de sitio para la tabla 'site_visit' en la base de datos."""

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.entity.site import Site


class SiteVisit(Base):
    """Modelo de contador de visitas para la tabla 'site_visit'."""

    __tablename__ = "site_visit"

    id_site: Mapped[int] = mapped_column(ForeignKey("site.id_site"), primary_key=True)
    visit_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relación con sitio
    site_rel: Mapped["Site"] = relationship("Site", back_populates="visits")

    def __repr__(self):
        return f"<SiteVisit(site={self.id_site}, visits={self.visit_count})>"
