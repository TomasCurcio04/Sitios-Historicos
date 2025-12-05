"""Servicio para gestionar estados (provincias)."""

from src.core.database import db  # O desde donde importes tu sesión de DB
from src.core.entity.state import State


def get_state_by_id(id_state):
    """Obtiene una provincia por su ID.

    Args:
        id_state (int): ID de la provincia.

    Returns:
        State: Objeto State correspondiente al ID proporcionado.
    """
    state = db.session.get(State, id_state)
    return state
