# pylint: disable=import-error
"""Modelo de sitio histórico para la tabla 'site_history' en la base de datos."""
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Text
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.entity.users import Users
    from src.core.entity.site import Site


class SiteHistory(Base):
    """Modelo de sitio histórico para la tabla 'site_history'."""

    __tablename__ = "site_history"
    id_site_history: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_site: Mapped[int] = mapped_column(ForeignKey("site.id_site"), nullable=False)
    site_rel: Mapped["Site"] = relationship(back_populates="history")
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id_user"), nullable=False) 
    user_rel: Mapped["Users"] = relationship(back_populates="user_history")
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    action_detail: Mapped[str] = mapped_column(Text)
    date_action: Mapped[datetime] = mapped_column(
        DateTime, default=lambda x: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<SiteHistory(id_site_history={self.id_site_history}, id_site={self.id_site}, id_user={self.id_user}, action_type='{self.action_type}', date_action='{self.date_action}')>"