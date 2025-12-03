"""Modelo de usuario para la tabla 'users' en la base de datos."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Boolean, DateTime, ForeignKey

if TYPE_CHECKING:
    from src.core.entity.site import Site
    from src.core.entity.site_history import SiteHistory
    from src.core.entity.role import Role
    from src.core.entity.feature_flag import FeatureFlag
    from src.core.entity.review import Review


class Users(Base):
    """Modelo de usuario para la tabla 'users'."""

    __tablename__ = "users"

    # Campos principales
    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    # Rol del usuario
    role: Mapped[int] = mapped_column(ForeignKey("role.id_role"), nullable=False)
    rol_rel: Mapped["Role"] = relationship("Role", back_populates="users")

    # Estado activo / superusuario
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    s_user: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relaciones con otros modelos
    sites: Mapped[list["Site"]] = relationship("Site", back_populates="user")
    user_history: Mapped[list["SiteHistory"]] = relationship(
        "SiteHistory", back_populates="user_rel"
    )
    flags: Mapped[list["FeatureFlag"]] = relationship(
        "FeatureFlag", back_populates="user"
    )
    moderated_reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="moderator_rel"
    )

    # Fechas de creación y modificación
    date_create: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    modify: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<Users(user_name='{self.user_name}', email='{self.email}', role={self.role})>"
