"""Funciones auxiliares para el servicio de reseñas"""

from src.web.api.services.review_serv import listar_reviews_by_site


def review_to_dict(review, public_user):
    """Convierte un objeto Review a diccionario según especificación API."""
    return {
        "id": review.id_review,
        "site_id": review.id_site,
        "user_name": public_user if public_user else None,
        "public_user_id": review.id_public_user,
        "rating": review.rating,
        "comment": review.content,
        "inserted_at": (
            review.date_created.isoformat() + "Z" if review.date_created else None
        ),
        "updated_at": (
            review.updated_at.isoformat() + "Z" if review.updated_at else None
        ),
    }


def get_reviews_by_site(site_id, **kwargs):
    """Listar reseñas de un sitio en formato json"""
    result = listar_reviews_by_site(site_id, **kwargs)
    print(f"Esto tiene result ", result)
    # Convertir reseñas a formato JSON
    data = [review_to_dict(review, user_name) for review, user_name in result["items"]]
    print(f"Esto tiene data ", data)

    return {
        "data": data,
        "meta": {
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
        },
    }


def get_user_review_for_site(site_id, public_user_id):
    """Obtiene la reseña de un usuario para un sitio específico"""
    from src.web.api.services.review_serv import get_user_review_for_site as get_user_review_service
    
    review = get_user_review_service(site_id, public_user_id)
    return review_to_dict(review, None) if review else None


def create_review(site_id, review_data, public_user_id):
    """Crea una nueva reseña"""
    from src.web.api.services.review_serv import create_review_service

    review = create_review_service(site_id, review_data, public_user_id)
    return review_to_dict(review, None)


def update_review(review_id, review_data, public_user_id):
    """Actualiza una reseña existente"""
    from src.web.api.services.review_serv import update_review_service

    review = update_review_service(review_id, review_data, public_user_id)
    return review_to_dict(review, None)


def get_review_by_id(review_id, site_id, include_pending=False):
    """Obtiene una reseña por ID"""
    from src.web.api.services.review_serv import get_review_by_id_service

    review = get_review_by_id_service(review_id, site_id, include_pending)

    if not review:
        return None

    return review_to_dict(review, None)


def delete_review(review_id, site_id, public_user_id=None):
    """Elimina una reseña por ID"""
    from src.web.api.services.review_serv import delete_review_service

    return delete_review_service(review_id, site_id, public_user_id)
