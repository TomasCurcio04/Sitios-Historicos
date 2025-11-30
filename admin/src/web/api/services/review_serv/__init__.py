"""Servicios de reseñas para la API"""

from src.core.database import db
from src.core.entity.review import Review, ReviewStatus


def listar_reviews_by_site(site_id, page=1, per_page=10):
    """Listar reseñas de un sitio con paginación"""
    query = (
        db.session.query(Review)
        .filter(
            Review.id_site == site_id,
            Review.status == ReviewStatus.APROBADA,  # Solo reseñas aprobadas
        )
        .order_by(Review.date_created.desc())
    )

    # Paginación
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return {"total": total, "page": page, "per_page": per_page, "items": items}


def create_review_service(site_id, review_data, public_user_id):
    """Crea una nueva reseña en la base de datos"""
    from datetime import datetime, timezone

    # Crear reseña (estado pendiente por defecto)
    now = datetime.now(timezone.utc)
    review = Review(
        id_site=site_id,
        id_public_user=public_user_id,
        rating=review_data["rating"],
        content=review_data["comment"],
        status=ReviewStatus.PENDIENTE,
        date_created=now,
        updated_at=now,
    )

    db.session.add(review)
    db.session.commit()

    return review


def get_review_by_id_service(review_id, site_id, include_pending=False):
    """Obtiene una reseña por ID y site_id"""
    try:
        query = db.session.query(Review).filter(
            Review.id_review == review_id, Review.id_site == site_id
        )

        if not include_pending:
            query = query.filter(Review.status == ReviewStatus.APROBADA)

        return query.first()
    except Exception:
        db.session.rollback()
        raise


def delete_review_service(review_id, site_id):
    """Elimina una reseña por ID"""
    review = (
        db.session.query(Review)
        .filter(Review.id_review == review_id, Review.id_site == site_id)
        .first()
    )

    if review:
        db.session.delete(review)
        db.session.commit()
        return True

    return False
