# test/sync_db_windows.py
import logging
from src.core.database import engine, Base

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def reset_db():
    """Elimina todas las tablas y las vuelve a crear."""
    print("=== SINCRONIZACIÓN DE TABLAS Y COLUMNAS ===")
    print("Eliminando tablas existentes...")

    # Drop todas las tablas con CASCADE para evitar errores de FK
    Base.metadata.drop_all(bind=engine, checkfirst=True)
    logging.info("Tablas eliminadas correctamente.")

    # Crear todas las tablas de nuevo
    Base.metadata.create_all(bind=engine)
    logging.info("Tablas creadas correctamente.")

    # Mensaje simple en lugar de Unicode
    print("Base de datos reiniciada correctamente.")

def main():
    reset_db()

if __name__ == "__main__":
    main()