# pylint: disable=import-error
"""Modelo de Provincias para la tabla 'state' en la base de datos."""
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.core.database import Base


if TYPE_CHECKING:
    from src.core.entity.site import Site


class State(Base):
    """Modelo de provincias para la tabla 'state'."""

    __tablename__ = "state"
    id_state: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    sites: Mapped[list["Site"]] = relationship(back_populates="state_rel")