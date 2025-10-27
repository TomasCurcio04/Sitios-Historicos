# pylint: disable=import-error
"""Modelo de usuario para la tabla 'users' en la base de datos."""


from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from src.core.database import Base
import re

if TYPE_CHECKING:
    from src.core.entity.site import Site
    from src.core.entity.site_history import SiteHistory
    from src.core.entity.role import Role
    from src.core.entity.feature_flag import FeatureFlag

# Expresion regular para validar emails



class Users(Base):
    """Modelo de usuario para la tabla 'users'."""

    __tablename__ = "users"
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

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

    @validates("email")
    def validate_email(self, key, email):
        if not re.match(self.EMAIL_REGEX, email):
            raise ValueError("El email no tiene un formato válido.")
        return email.strip().lower()

    @validates("user_name")
    def validate_user_name(self, key, user_name):
        if not user_name or len(user_name.strip()) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres.")
        return user_name.strip()

    @validates("password")
    def validate_password(self, key, password):
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        return password

    def __repr__(self):
        return f"<Users(user_name='{self.user_name}', email='{self.email}', role={self.role})>"
