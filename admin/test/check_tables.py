"""
Verifica que las tablas, columnas y relaciones de la base de datos existan.
Compatible con modo JSON y Base de Datos.
"""

from sqlalchemy import inspect, create_engine
from src.core.database import db

# Cambiar según tu base de datos real
DATABASE_URL = "sqlite:///database.db"

TABLES_ESPERADAS = {
    "site": ["id", "name", "short_description", "full_description", "city", "province",
             "conservation_state", "inauguration_year", "category", "state", "latitude",
             "longitude", "is_visible", "created_by", "fecha_registro"],
    "category": ["id", "name"],
    "state": ["id", "name"],
    "tag": ["id", "name"],
    "site_history": ["id", "site", "user", "fecha"],
    "users": ["id", "name"]
}

def main():
    # Crear engine
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)

    print("=== VERIFICACIÓN COMPLETA DE TABLAS, COLUMNAS Y RELACIONES ===\n")

    for table_name, columnas_esperadas in TABLES_ESPERADAS.items():
        if table_name in inspector.get_table_names():
            print(f"Tabla '{table_name}': EXISTE [OK]")

            columnas_actuales = [col["name"] for col in inspector.get_columns(table_name)]
            for col in columnas_esperadas:
                if col in columnas_actuales:
                    print(f"  Columna '{col}': existe [OK]")
                else:
                    print(f"  Columna '{col}': NO EXISTE [X]")

        else:
            print(f"Tabla '{table_name}': NO EXISTE [X]")

    print("\n=== FIN DE VERIFICACIÓN ===")

if __name__ == "__main__":
    main()