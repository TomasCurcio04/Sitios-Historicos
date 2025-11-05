"""Punto de entrada principal de la aplicación Flask."""

from src.web import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
