"""Modelo de permiso para la tabla 'permission' en la base de datos."""

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.entity.role import Role


class Permission(Base):
    """Modelo de permiso para la tabla 'permission'."""

    __tablename__ = "permission"

    id_permission: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    permission_name: Mapped[str] = mapped_column(String(50), nullable=False)
    permission_description: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return (
            f"<Permission(id_permission={self.id_permission}, "
            f"permission_name='{self.permission_name}')>"
        )
