"""Test module for database connection."""

from sqlalchemy import create_engine, text
import sys
import os

# Agregar la ruta del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar directamente desde el archivo config
from src.web.config import DevelopmentConfig


def test_connection_to_default_engine():
    """Test connection to the default database engine."""
    db_url = DevelopmentConfig.SQLALCHEMY_ENGINES["default"]
    engine = create_engine(db_url)
    print(f"Testing connection to database at {db_url}")

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1
