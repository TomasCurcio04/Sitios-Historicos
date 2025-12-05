"""Servicios de reseñas para la API"""

from src.core.database import db
from src.core.entity.review import Review, ReviewStatus
from src.core.entity.public_user import PublicUser


# def listar_reviews_by_site(site_id, page=1, per_page=10):
#     """Listar reseñas de un sitio con paginación"""
#     query = (
#         db.session.query(Review)
#         .filter(
#             Review.id_site == site_id,
#             Review.status == ReviewStatus.APROBADA,  # Solo reseñas aprobadas
#         )
#         .order_by(Review.date_created.desc())
#     )

#     # Paginación
#     total = query.count()
#     items = query.offset((page - 1) * per_page).limit(per_page).all()


#     return {"total": total, "page": page, "per_page": per_page, "items": items}
def listar_reviews_by_site(site_id, page=1, per_page=10):
    """Listar reseñas de un sitio con paginación, devolviendo nombre de usuario"""
    query = (
        db.session.query(Review, PublicUser.name)
        .join(PublicUser, Review.id_public_user == PublicUser.id_public_user)
        .filter(
            Review.id_site == site_id,
            Review.status == ReviewStatus.APROBADA,
        )
        .order_by(Review.date_created.desc())
    )
    # Paginación
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return {"total": total, "page": page, "per_page": per_page, "items": items}


def get_user_review_for_site(site_id, public_user_id):
    """Obtiene la reseña de un usuario para un sitio específico (cualquier estado)"""
    return (
        db.session.query(Review)
        .filter(
            Review.id_site == site_id,
            Review.id_public_user == public_user_id
        )
        .first()
    )


def create_review_service(site_id, review_data, public_user_id):
    """Crea una nueva reseña en la base de datos"""
    from datetime import datetime, timezone

    # Verificar si el usuario ya tiene una reseña para este sitio
    existing_review = get_user_review_for_site(site_id, public_user_id)
    if existing_review:
        if existing_review.status == ReviewStatus.RECHAZADA:
            # Si tiene una rechazada, editarla en lugar de crear nueva
            existing_review.rating = review_data["rating"]
            existing_review.content = review_data["comment"]
            existing_review.status = ReviewStatus.PENDIENTE
            existing_review.updated_at = datetime.now(timezone.utc)
            existing_review.date_moderated = None
            existing_review.moderated_by = None
            existing_review.rejection_reason = None
            db.session.commit()
            return existing_review
        else:
            raise ValueError("Ya tienes una reseña para este sitio. Puedes editarla en tu perfil.")

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


def update_review_service(review_id, review_data, public_user_id):
    """Actualiza una reseña existente y la pone en estado pendiente"""
    from datetime import datetime, timezone

    review = (
        db.session.query(Review)
        .filter(
            Review.id_review == review_id,
            Review.id_public_user == public_user_id,
            Review.status.in_([ReviewStatus.APROBADA, ReviewStatus.PENDIENTE])
        )
        .first()
    )

    if not review:
        raise ValueError("Reseña no encontrada o no tienes permisos para editarla")

    # Actualizar campos
    review.rating = review_data["rating"]
    review.content = review_data["comment"]
    review.status = ReviewStatus.PENDIENTE  # Volver a pendiente al editar
    review.updated_at = datetime.now(timezone.utc)
    review.date_moderated = None  # Resetear fecha de moderación
    review.moderated_by = None  # Resetear moderador
    review.rejection_reason = None  # Limpiar razón de rechazo

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


def delete_review_service(review_id, site_id, public_user_id=None):
    """Elimina una reseña por ID"""
    query = db.session.query(Review).filter(Review.id_review == review_id)
    
    # Si se proporciona site_id, filtrar por él
    if site_id is not None:
        query = query.filter(Review.id_site == site_id)
    
    # Si se proporciona public_user_id, verificar que sea el dueño
    if public_user_id:
        query = query.filter(Review.id_public_user == public_user_id)
    
    review = query.first()

    if review:
        # No permitir eliminar reseñas rechazadas
        if review.status == ReviewStatus.RECHAZADA:
            raise ValueError("No se pueden eliminar reseñas rechazadas")
        
        db.session.delete(review)
        db.session.commit()
        return True

    return False
