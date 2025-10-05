"""Modelo de rol para la tabla 'role' en la base de datos."""

# pylint: disable=import-error
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.core.database import Base

if TYPE_CHECKING:
    from src.core.board.users import Users


class Role(Base):
    """Modelo de rol para la tabla 'role'."""

    __tablename__ = "role"

    id_role: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    users: Mapped[list["Users"]] = relationship(back_populates="categroy")

    def __repr__(self):
        return f"<Role(id_role={self.id_role}, name='{self.name}', description='{self.description}')>"
