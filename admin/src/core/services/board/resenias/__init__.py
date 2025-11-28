"""Servicio de gestión de reseñas para sitios históricos."""

from src.core.database import db
from src.core.entity.review import Review
from src.core.entity.site import Site
from src.core.entity.public_user import PublicUser
from src.core.entity.review import ReviewStatus
from datetime import datetime, timezone
from sqlalchemy import or_, distinct


def buscar_review_con_filtros(filtros):
    """Construye y ejecuta una consulta de reseñas aplicando filtros.

    Args:
        filtros (dict): Diccionario con posibles filtros:
            - sitio: lista de ids de sitios
            - email_usuario: texto para buscar email de usuario público
            - puntuacion: lista o string con puntuaciones
            - contenido: texto a buscar en el contenido
            - estado: estado de la reseña (str)
            - fecha_desde, fecha_hasta: fechas para rango

    Returns:
        list[dict]: Lista de reseñas como diccionarios serializados.
    """
    query = db.session.query(Review)

    # Filtrar por sitio por ID
    if filtros.get("sitio"):
        query = query.filter(Review.id_site.in_(filtros["sitio"]))

    # Filtrar por email de usuario público
    if filtros.get("email_usuario"):
        texto = f"%{filtros['email_usuario']}%"
        query = query.join(Review.public_user_rel).filter(PublicUser.email.ilike(texto))

    # Filtrar por puntuación
    if filtros.get("puntuacion"):
        puntuaciones = filtros["puntuacion"]
        if isinstance(puntuaciones, str):
            puntuaciones = [puntuaciones]
        puntuaciones = [int(p) for p in puntuaciones if p]
        if puntuaciones:
            query = query.filter(Review.rating.in_(puntuaciones))

    # Filtrar por contenido
    if filtros.get("contenido"):
        texto = f"%{filtros['contenido']}%"
        query = query.filter(Review.content.ilike(texto))

    # Filtrar por estado (solo si no está vacío)
    if filtros.get("estado") and filtros["estado"].strip():
        try:
            estado_enum = ReviewStatus(filtros["estado"])
            query = query.filter(Review.status == estado_enum)
        except ValueError:
            pass

    # Filtrar por rango de fechas
    if filtros.get("fecha_desde"):
        query = query.filter(Review.date_created >= filtros["fecha_desde"])
    if filtros.get("fecha_hasta"):
        query = query.filter(Review.date_created <= filtros["fecha_hasta"])

    resultados = []
    for review in query.all():
        resultados.append(
            {
                "id_review": review.id_review,
                "name": review.site_rel.name,
                "user_email": review.public_user_rel.email,
                "rating": review.rating,
                "content": review.content,
                "status": review.status.value,
                "date_created": review.date_created.strftime("%Y-%m-%d"),
            }
        )
    return resultados


def paginar_lista(results, page, per_page):
    """Devuelve los items de la página indicada y total de páginas.

    Args:
        results (list): Lista completa de resultados.
        page (int): Página solicitada (1-indexed).
        per_page (int): Elementos por página.

    Returns:
        tuple: (page_items, total_pages, total_results)
            - page_items (list): Subconjunto de resultados para la página.
            - total_pages (int): Número total de páginas.
            - total_results (int): Número total de resultados.
    """
    total_results = len(results)
    total_pages = (total_results + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_items = results[start:end]
    return page_items, total_pages, total_results


def ordenar_lista(results, sort, order):
    """Ordena una lista de diccionarios según un campo simple.

    Args:
        results (list[dict]): Lista de registros.
        sort (str): Campo por el que ordenar ('rating' o 'date_created').
        order (str): 'asc' o 'desc'.

    Returns:
        list[dict]: Lista ordenada (la misma lista, ordenada in-place).
    """
    if sort in ["rating", "date_created"]:
        results.sort(key=lambda r: r.get(sort), reverse=(order == "desc"))
    return results


def eliminar_review(review_id):
    """Elimina una reseña por su ID.

    Args:
        review_id (int): ID de la reseña a eliminar.

    Returns:
        tuple: (review, error)
            - review: Objeto Review eliminado o None si no existe.
            - error: Mensaje de error o None si fue exitoso.
    """
    review = db.session.get(Review, review_id)
    if not review:
        return None, "Reseña no encontrada."
    else:
        db.session.delete(review)
        db.session.commit()
    return review, None


def aprobar_review(review_id, moderator_id):
    """Aprueba una reseña por su ID.

    Args:
        review_id (int): ID de la reseña.
        moderator_id (int): ID del moderador que aprueba.

    Returns:
        tuple: (review, error)
            - review: Objeto Review actualizado o None si no existe.
            - error: Mensaje de error o None si fue exitoso.
    """
    review = db.session.get(Review, review_id)
    if not review:
        return None, "Reseña no encontrada."
    else:
        review.status = ReviewStatus.APROBADA
        review.moderated_by = moderator_id
        review.date_moderated = datetime.now(timezone.utc)
        db.session.commit()
    return review, None


def buscar_review_por_id(review_id):
    """Busca una reseña por su ID.

    Args:
        review_id (int): ID de la reseña.

    Returns:
        Review|None: Instancia Review si existe, o None.
    """
    review = db.session.get(Review, review_id)
    return review


def rechazar_review(review_id, moderator_id, reason):
    """Rechaza una reseña por su ID con una razón.

    Args:
        review_id (int): ID de la reseña.
        moderator_id (int): ID del moderador.
        reason (str): Motivo del rechazo.

    Returns:
        tuple: (review, error)
            - review: Objeto Review actualizado o None si no existe.
            - error: Mensaje de error o None si fue exitoso.
    """
    review = db.session.get(Review, review_id)
    if not review:
        return None, "Reseña no encontrada."
    else:
        review.status = ReviewStatus.RECHAZADA
        review.rejection_reason = reason
        review.moderated_by = moderator_id
        review.date_moderated = datetime.now(timezone.utc)
        db.session.commit()
    return review, None


def obtener_sitios_con_reviews():
    """Obtiene sitios que tienen al menos una reseña asociada.

    Returns:
        list[tuple]: Lista de tuplas (id_sitio, nombre).
    """
    resultados = (
        db.session.query(Site.id_site, Site.name)
        .join(Review, Review.id_site == Site.id_site)
        .distinct()
        .order_by(Site.name)
        .all()
    )
    return resultados
