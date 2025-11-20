"""Configuración específica para tests."""

class TestConfig:
    """Configuración para el entorno de testing."""
    TESTING = True
    JWT_SECRET_KEY = "test-secret-key"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = None
    SECRET_KEY = "test-secret"