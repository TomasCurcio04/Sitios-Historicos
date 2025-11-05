"""Servicio para la gestión de etiquetas de sitios históricos."""

from src.core.database import db
from src.core.entity.tag import Tag
from sqlalchemy.exc import IntegrityError

# -------------------------------
# Consultas y operaciones con tags
# -------------------------------


def obtener_todas_las_tags():
    """Obtiene todas las etiquetas disponibles.

    Returns:
        Lista de todas las etiquetas en la base de datos
    """
    session = db.session
    query = session.query(Tag)
    all_tags = session.query(Tag).all()
    return all_tags


def buscar_tags(filtros):
    """Busca etiquetas con filtros, ordenamiento y paginación.

    Args:
        filtros: Diccionario con criterios de búsqueda

    Returns:
        Diccionario con etiquetas encontradas y metadatos de paginación
    """
    texto = filtros.get("texto", "").strip()
    page = int(filtros.get("page", 1))
    per_page = filtros.get("per_page", 25)
    sort = filtros.get("sort", "name")
    order = filtros.get("order", "asc")

    session = db.session
    query = session.query(Tag)

    if texto:
        query = query.filter(Tag.name.ilike(f"%{texto}%"))

    # Ordenamiento
    if sort == "name":
        query = query.order_by(Tag.name.desc() if order == "desc" else Tag.name.asc())
    elif sort == "date_created":
        query = query.order_by(
            Tag.date_created.desc() if order == "desc" else Tag.date_created.asc()
        )

    total_results = query.count()
    total_pages = (total_results + per_page - 1) // per_page
    tags = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "tags": tags,
        "texto": texto,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "sort": sort,
        "order": order,
        "total_results": total_results,
    }


def crear_tag(name):
    """Crea una nueva etiqueta.

    Args:
        name: Nombre de la etiqueta

    Returns:
        Tupla (etiqueta, error) donde error es None si fue exitoso
    """
    session = db.session
    tag = Tag(name=name)
    session.add(tag)
    try:
        session.commit()
        return tag, None
    except IntegrityError:
        session.rollback()
        return None, "Ya existe una etiqueta con ese nombre"


def actualizar_tag(tag_id, name):
    """Actualiza una etiqueta existente.

    Args:
        tag_id: ID de la etiqueta a actualizar
        name: Nuevo nombre para la etiqueta

    Returns:
        Tupla (etiqueta, error) donde error es None si fue exitoso
    """
    session = db.session
    tag = session.get(Tag, tag_id)
    if not tag:
        return None, "Etiqueta no encontrada"

    tag.name = name
    tag.slug = Tag.generate_slug(name)
    try:
        session.commit()
        return tag, None
    except IntegrityError:
        session.rollback()
        return None, "Ya existe una etiqueta con ese nombre"


def eliminar_tag(tag_id):
    """Elimina una etiqueta si no está asociada a sitios.

    Args:
        tag_id: ID de la etiqueta a eliminar

    Returns:
        Tupla (etiqueta, error) donde error es None si fue exitoso
    """
    session = db.session
    tag = session.get(Tag, tag_id)
    if not tag:
        return None, "Etiqueta no encontrada"
    if tag.sites:
        return None, "No se puede eliminar un tag asignado a sitios"

    session.delete(tag)
    session.commit()
    return tag, None
