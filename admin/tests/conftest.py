import pytest
import os
from src.web import create_app

@pytest.fixture
def app():
    """Crear app Flask para tests."""
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    app = create_app('testing')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Cliente de test."""
    return app.test_client()