"""Servicios relacionados con Sitios históricos"""

from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.state import State
from src.core.entity.category import Category
from src.core.entity.tag import Tag
from src.core.services.board.site_history_serv import register_modify


# Consultas y operaciones con Sitios


def list_sites():
    """Lista todos los sitios históricos.

    Returns:
        Lista de sitios desde DB o JSON según configuración
    """
    session = db.session
    return session.query(Site).all()


def obtener_todos_las_provincias():
    """Obtiene todas las provincias
    Args:
        None
    Returns:
        Lista de todas las provincias en la base de datos
    """

    session = db.session
    all_states = session.query(State).all()
    return all_states


def obtener_todas_las_categorias():
    """Obtiene todas las categorias
    Args:
        None
    Returns:
        Lista de todas las categorias en la base de Datos
    """

    session = db.session
    all_categorys = session.query(Category).all()
    return all_categorys


def obtener_sitio_id(site_id):
    """Obtiene un sitio histórico por su ID
    Args:
        site_id (int): ID del sitio histórico
    Returns:
        Sitio histórico correspondiente al ID proporcionado
    """
    sitio = db.session.get(Site, site_id)
    return sitio


def actualizar_sitio(sitio, data, nuevas_etiquetas):
    """Actualiza un sitio histórico
    Args:
        sitio (Site): Instancia del sitio histórico a actualizar
        data (dict): Diccionario con los datos actualizados del sitio histórico
        nuevas_etiquetas (list): Lista de nuevas etiquetas asociadas al sitio histórico
    Returns:
        None
    """
    for key, value in data.items():
        setattr(sitio, key, value)
    sitio.tag = nuevas_etiquetas
    db.session.commit()
    return


def eliminar_sitio(sitio):
    """Elimina un sitio histórico
    Args:
        sitio (Site): Instancia del sitio histórico a eliminar
    Returns:
        Sitio histórico eliminado
    """
    sitio.deleted = True
    db.session.commit()
    return sitio


def crear_sitio(data, tags_ids, user_id):
    """Crea un sitio con sus etiquetas.
    Args:
        data (dict): Diccionario con los datos del sitio a crear
        tags_ids (list): Lista de IDs de las etiquetas a asociar al sitio
        user_id (int): ID del usuario que crea el sitio
    Returns:
        Sitio creado
    """

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
    """ "Obtiene las etiquetas correspondientes a los IDs proporcionados.
    Args:
        tags_ids (list): Lista de IDs de las etiquetas
    Returns:
        Lista de etiquetas correspondientes a los IDs proporcionados
    """
    return db.session.query(Tag).filter(Tag.id_tag.in_(tags_ids)).all()
