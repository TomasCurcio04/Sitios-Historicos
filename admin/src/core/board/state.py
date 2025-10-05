# pylint: disable=import-error
"""Modelo de Provincias para la tabla 'state' en la base de datos."""
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from src.core.database import Base


if TYPE_CHECKING:
    from src.core.board.site import Site


class State(Base):
    """Modelo de provincias para la tabla 'state'."""

    __tablename__ = "state"

    id_state = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    site: Mapped[list["Site"]] = relationship(back_populates="state")
