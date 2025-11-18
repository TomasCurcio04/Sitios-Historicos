"""Punto de entrada principal de la aplicación Flask."""

import sys
import os

# Agregar la carpeta padre al path para poder importar desde api y portal
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.web import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
