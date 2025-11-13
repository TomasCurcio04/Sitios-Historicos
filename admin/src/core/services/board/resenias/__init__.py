"""Servicio de gestión de reseñas para sitios históricos."""

from src.core.database import db
from src.core.entity.review import Review
from src.core.entity.site import Site
from src.core.entity.users import Users

from sqlalchemy import or_, distinct


def buscar_review(filtros):
    """Devuelve una lista de reseñas filtradas según los parámetros de búsqueda."""
    query = db.session.query(Review)

    if filtros.get("sitio"):
        query = query.join(Review.site_rel).filter(
            Review.site_rel.has(Site.name.ilike(f"%{filtros['sitio']}%"))
        )

    if filtros.get("email_usuario"):
        query = query.join(Review.public_user_rel).filter(
            Review.public_user_rel.has(Users.email.ilike(f"%{filtros['email_usuario']}%"))
        )

    if filtros.get("puntuacion"):
        query = query.filter(Review.rating == filtros["puntuacion"])

    if filtros.get("estado"):
        query = query.filter(Review.status == filtros["estado"])

    if filtros.get("fecha_desde"):
        query = query.filter(Review.date_created >= filtros["fecha_desde"])

    if filtros.get("fecha_hasta"):
        query = query.filter(Review.date_created <= filtros["fecha_hasta"])

    # Ejecutar la query y devolver lista de diccionarios
    resultados = []
    for review in query.all():
        resultados.append({
            "name": review.site_rel.name if review.site_rel else None,
            "user_email": review.public_user_rel.email,
            "rating": review.rating,
            "content": review.content,
            "status": review.status,
            "date_created": review.date_created.isoformat() if review.date_created else None,
        })
    return resultados


def paginar_lista(results, page, per_page):
    """Devuelve los items de la página indicada y total de páginas."""
    total_results = len(results)
    total_pages = (total_results + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_items = results[start:end]
    return page_items, total_pages, total_results