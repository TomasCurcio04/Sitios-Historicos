from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.state import State
from src.core.entity.category import Category
from src.core.entity.tag import Tag
from src.core.services.board.site_history_serv import register_modify


# Consultas y operaciones con Sitios

def obtener_todos_las_provincias():
    """Obtiene todas las provincias
    Returns:
        Lista de todas las provincias en la base de datos"""
    

    session = db.session
    all_states = session.query(State).all()
    return all_states


def obtener_todas_las_categorias():
    """Obtiene todas las categorias
    Returns:
        Lista de todas las categorias en la base de Datos"""
    
    session = db.session
    all_categorys = session.query(Category).all()
    return all_categorys



def obtener_sitio_id(site_id):
      sitio = db.session.get(Site, site_id)
      return sitio

def actualizar_sitio(sitio,data,nuevas_etiquetas):
    for key, value in data.items():
        setattr(sitio, key, value)
    sitio.tag=nuevas_etiquetas
    db.session.commit()
    return 

def eliminar_sitio(sitio):
    """Elimina un sitio histórico"""

    db.session.delete(sitio)
    db.session.commit()
    return

def crear_sitio(data, tags_ids, user_id):
        """Crea un sitio con sus etiquetas."""

        nuevo_sitio = Site(**data, created_by=user_id)

        # Asociar etiquetas
        tags = db.session.query(Tag).filter(Tag.id_tag.in_(tags_ids)).all()
        nuevo_sitio.tag = tags

        try:
            db.session.add(nuevo_sitio)
            db.session.commit()
            return nuevo_sitio

        except Exception:
            db.session.rollback()
            raise


def obtener_nuevas_etiquetas(tags_ids):
     return db.session.query(Tag).filter(Tag.id_tag.in_(tags_ids)).all()