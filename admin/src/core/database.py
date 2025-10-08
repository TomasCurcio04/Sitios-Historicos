from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:KcooNtcHPuxNsQSXpQfMuUiVpmEFaeYm@nozomi.proxy.rlwy.net:55215/railway"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# Funciones
def init_db(*args, **kwargs):
    """Inicializa la base de datos creando todas las tablas."""
    Base.metadata.create_all(bind=engine)


def reset_db():
    """Reinicia la base de datos: elimina todas las tablas y las vuelve a crear."""
    print("Eliminando todas las tablas existentes...")

    with engine.connect() as conn:
        # Borra todo el esquema público con CASCADE (elimina tablas y dependencias)
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()

    print("Creando todas las tablas nuevamente...")
    Base.metadata.create_all(bind=engine)
    print("Base de datos reiniciada correctamente.")

