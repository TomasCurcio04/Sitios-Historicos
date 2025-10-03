"""Modelo de sitio histórico para la tabla 'site' en la base de datos."""

from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, Text, DECIMAL
from src.core.database import Base


class Site(Base):
    """Modelo de sitio histórico para la tabla 'site'."""

    __tablename__ = "site"
    id_site: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    short_description: Mapped[str] = mapped_column(String(255))
    full_description: Mapped[str] = mapped_column(Text)
    city: Mapped[int] = mapped_column(
        Integer, ForeignKey("state.id_state"), nullable=False
    )
    state: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(DECIMAL(9, 6))
    longitude: Mapped[float] = mapped_column(DECIMAL(9, 6))
    conservation_state: Mapped[str] = mapped_column(String(20), nullable=False)
    inauguration_year: Mapped[int] = mapped_column(Integer)
    category: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id_category"), nullable=False
    )
    date_registered: Mapped[datetime] = mapped_column(
        DateTime, default=lambda x: datetime.now(timezone.utc)
    )
    is_visible: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    created_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id_user"), nullable=False
    )

    def __repr__(self):
        return f"<Site(name='{self.name}', state='{self.state}', is_visible={self.is_visible})>"
