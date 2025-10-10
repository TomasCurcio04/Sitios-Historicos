from app import create_app  # Tu función que crea la app Flask
from src.core.database import db
from sqlalchemy import inspect

def main():
    # Crear la app Flask con configuración de desarrollo
    app = create_app("development")

    # No inicializamos db de nuevo, solo usamos la que ya está ligada a la app
    # db.init_app(app)  <-- omitido para evitar error de "ya inicializado"

    # Tablas que queremos revisar
    expected_tables = ["site", "category", "state", "tag", "site_history", "users", "permission_list", "site_tag"]

    with app.app_context():
        # Obtenemos el engine desde la app
        engine = db.engines["default"]
        inspector = inspect(engine)

        print("=== VERIFICACIÓN DE TABLAS EN LA BASE DE DATOS ===\n")
        for table_name in expected_tables:
            if table_name in inspector.get_table_names():
                print(f"Tabla '{table_name}': Existe")
            else:
                print(f"Tabla '{table_name}': NO EXISTE")
        print("\n=== FIN DE VERIFICACIÓN ===")

if __name__ == "__main__":
    main()