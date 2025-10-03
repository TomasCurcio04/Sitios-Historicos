"""Modelo de usuario para la tabla 'users' en la base de datos."""

from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime
from src.core.database import Base


class Users(Base):
    """Modelo de usuario para la tabla 'users'."""

    __tablename__ = "users"
    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    pass_: Mapped[str] = mapped_column(String(255), nullable=False)
    # role: Mapped[int] = mapped_column(
    #     Integer, ForeignKey("role.id_role"), nullable=False
    # )
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    super: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    date_create: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
    modify: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Users(user_name='{self.user_name}', email='{self.email}', role={self.role})>"
