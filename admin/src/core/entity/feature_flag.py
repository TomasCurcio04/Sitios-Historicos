"""Modelo de Feature Flags para la tabla 'feature_flag' en la base de datos."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.entity.users import Users


class FeatureFlag(Base):
    """Modelo de Feature Flags para la tabla 'feature_flag'."""

    __tablename__ = "feature_flag"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    maintenance_message: Mapped[str] = mapped_column(String(100), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    updated_by: Mapped[int] = mapped_column(ForeignKey("users.id_user"), nullable=False)
    user: Mapped["Users"] = relationship(back_populates="flags")

    def __repr__(self):
        return f"<FeatureFlag(name={self.name}, enabled={self.enabled})>"
