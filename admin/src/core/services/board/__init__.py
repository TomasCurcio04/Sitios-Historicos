"""
Módulo para gestionar sitios históricos, categorías, estados, usuarios y tags.
Se integra con base de datos usando SQLAlchemy y mantiene soporte JSON para pruebas.
"""

import os
import json
from datetime import datetime
from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.category import Category
from src.core.entity.state import State
from src.core.entity.site_history import SiteHistory
from src.core.entity.tag import Tag
from src.core.entity.review import Review


# -------------------------
# Funciones de sitios
# -------------------------
def list_sites():
    """Lista todos los sitios históricos.

    Returns:
        Lista de sitios desde DB o JSON según configuración
    """
    session = db.session
    return session.query(Site).all()
