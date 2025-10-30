"""Punto de entrada alternativo para desarrollo."""

from src.web import create_app

if __name__ == "__main__":
    app = create_app(env="development")
    app.run(debug=True)
