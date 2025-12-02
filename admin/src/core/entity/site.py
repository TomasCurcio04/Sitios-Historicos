"""Modelo de sitio histórico para la tabla 'site' en la base de datos."""

from typing import TYPE_CHECKING
from datetime import datetime, timezone

# from src.core.entity.site_history import SiteHistory  # Evitar importación circular
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
    DECIMAL,
    Table,
    Column,
)
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.entity.users import Users
    from src.core.entity.category import Category
    from src.core.entity.state import State
    from src.core.entity.tag import Tag
    from src.core.entity.site_image import SiteImage
    from src.core.entity.site_history import SiteHistory
    from src.core.entity.site_tag import SiteTag
    from src.core.entity.review import Review
    from src.core.entity.site_visit import SiteVisit
    from src.core.entity.site_favorite import SiteFavorite


site_tag = Table(
    "site_tag",
    Base.metadata,
    Column("id_site", ForeignKey("site.id_site"), nullable=False),
    Column("id_tag", ForeignKey("tag.id_tag"), nullable=False),
    extend_existing=True,
)


class Site(Base):
    """Modelo de sitio histórico para la tabla 'site'."""

    __tablename__ = "site"
    id_site: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    short_description: Mapped[str] = mapped_column(String(120))
    full_description: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[int] = mapped_column(ForeignKey("state.id_state"), nullable=False)
    state_rel: Mapped["State"] = relationship(back_populates="sites")
    latitude: Mapped[float] = mapped_column(DECIMAL(9, 6))
    longitude: Mapped[float] = mapped_column(DECIMAL(9, 6))
    conservation_state: Mapped[str] = mapped_column(String(20), nullable=True)
    inauguration_year: Mapped[int] = mapped_column(Integer, nullable=True)
    category: Mapped[int] = mapped_column(
        ForeignKey("category.id_category"), nullable=False
    )
    category_rel: Mapped["Category"] = relationship(back_populates="sites")
    date_registered: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    is_visible: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    tag: Mapped[list["Tag"]] = relationship(secondary=site_tag)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id_user"), nullable=False)
    user: Mapped["Users"] = relationship(back_populates="sites")
    history: Mapped[list["SiteHistory"]] = relationship(back_populates="site_rel")
    images: Mapped[list["SiteImage"]] = relationship(back_populates="site_rel")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="site_rel")
    visits: Mapped["SiteVisit"] = relationship(
        "SiteVisit", back_populates="site_rel", uselist=False
    )
    favorites: Mapped[list["SiteFavorite"]] = relationship(
        "SiteFavorite", back_populates="site_rel"
    )

    def __repr__(self):
        return f"<Site(name='{self.name}', state='{self.state}', is_visible={self.is_visible})>"
