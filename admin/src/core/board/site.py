# pylint: disable=import-error
"""Modelo de sitio histórico para la tabla 'site' en la base de datos."""
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, Text, DECIMAL
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.auth.users import Users
    from src.core.board.category import Category
    from src.core.board.state import State


class Site(Base):
    """Modelo de sitio histórico para la tabla 'site'."""

    __tablename__ = "site"
    id_site: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    short_description: Mapped[str] = mapped_column(String(120))
    full_description: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[int] = mapped_column(ForeignKey("state.id_state"), nullable=False)
    state_rel: Mapped["State"] = relationship(back_populates="site")
    latitude: Mapped[float] = mapped_column(DECIMAL(9, 6))
    longitude: Mapped[float] = mapped_column(DECIMAL(9, 6))
    conservation_state: Mapped[str] = mapped_column(String(20), nullable=False)
    inauguration_year: Mapped[int] = mapped_column(Integer)
    category: Mapped[int] = mapped_column(
        ForeignKey("category.id_category"), nullable=False
    )
    category_rel: Mapped["Category"] = relationship(back_populates="site")
    date_registered: Mapped[datetime] = mapped_column(
        DateTime, default=lambda x: datetime.now(timezone.utc)
    )
    is_visible: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id_user"), nullable=False)
    user: Mapped["Users"] = relationship(back_populates="site")

    def __repr__(self):
        return f"<Site(name='{self.name}', state='{self.state}', is_visible={self.is_visible})>"
