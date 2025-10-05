from sqlalchemy import create_engine, text
from src.web.config import DevelopmentConfig  

def test_connection_to_default_engine():
    """Test connection to the default database engine."""
    db_url = DevelopmentConfig.SQLALCHEMY_ENGINES["default"]
    engine = create_engine(db_url)

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1