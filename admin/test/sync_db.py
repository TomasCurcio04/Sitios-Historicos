from sqlalchemy import inspect
from src.core.database import db
from app import create_app  # Ajustá si tu app.py está en otra ruta

def main():
    # Crear la app Flask con configuración de desarrollo
    app = create_app("development")

    # No inicializamos db de nuevo si ya se hace dentro de create_app
    # db.init_app(app)

    # Lista de tablas que queremos revisar
    expected_tables = ["site", "category", "state", "tag", "site_history", "users"]

    with app.app_context():
        inspector = inspect(db.engines["default"])  # usamos engine de db
        print("=== VERIFICACIÓN DE TABLAS EN LA BASE DE DATOS ===\n")
        for table_name in expected_tables:
            if table_name in inspector.get_table_names():
                print(f"Tabla '{table_name}': Existe")
            else:
                print(f"Tabla '{table_name}': NO EXISTE")
        print("\n=== FIN DE VERIFICACIÓN ===")

if __name__ == "__main__":
    main()