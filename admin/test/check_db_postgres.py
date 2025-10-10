from src.core.database import db
from app import create_app  # o la ruta correcta a tu app.py
from sqlalchemy import inspect

def main():
    app = create_app("development")

    with app.app_context():
        inspector = inspect(db.engine)
        print("=== TABLAS EN LA BASE DE DATOS ===")
        for table_name in inspector.get_table_names():
            print(table_name)

if __name__ == "__main__":
    main()