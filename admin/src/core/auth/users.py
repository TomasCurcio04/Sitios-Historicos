# pylint: disable=import-error
"""Modelo de usuario para la tabla 'users' en la base de datos."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.board.site import Site


class Users(Base):
    """Modelo de usuario para la tabla 'users'."""

    __tablename__ = "users"
    id_user: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    pass_: Mapped[str] = mapped_column(String(100), nullable=False)
    # role: Mapped[int] = mapped_column(
    #     Integer, ForeignKey("role.id_role"), nullable=False
    # )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    super: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    site: Mapped[list["Site"]] = relationship(back_populates="users")
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
        return f"<Users(user_name='{self.user_name}', email='{self.email}')>"
        # , role={self.role})>"
