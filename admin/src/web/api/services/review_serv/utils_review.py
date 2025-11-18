"""Funciones auxiliares para el servicio de reseñas"""

from src.web.api.services.review_serv import listar_reviews_by_site


def review_to_dict(review):
    """Convierte un objeto Review a diccionario según especificación API."""
    return {
        "id": review.id_review,
        "site_id": review.id_site,
        "rating": review.rating,
        "comment": review.content,
        "inserted_at": review.date_created.isoformat() + "Z" if review.date_created else None,
        "updated_at": review.updated_at.isoformat() + "Z" if review.updated_at else None
    }


def get_reviews_by_site(site_id, **kwargs):
    """Listar reseñas de un sitio en formato json"""
    result = listar_reviews_by_site(site_id, **kwargs)
    
    # Convertir reseñas a formato JSON
    data = [review_to_dict(review) for review in result["items"]]
    
    return {
        "data": data,
        "meta": {
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"]
        }
    }


def create_review(site_id, review_data, user_id):
    """Crea una nueva reseña"""
    from src.web.api.services.review_serv import create_review_service
    
    review = create_review_service(site_id, review_data, user_id)
    return review_to_dict(review)


def get_review_by_id(review_id, site_id, include_pending=False):
    """Obtiene una reseña por ID"""
    from src.web.api.services.review_serv import get_review_by_id_service
    
    review = get_review_by_id_service(review_id, site_id, include_pending)
    
    if not review:
        return None
    
    return review_to_dict(review)


def delete_review(review_id, site_id):
    """Elimina una reseña por ID"""
    from src.web.api.services.review_serv import delete_review_service
    
    return delete_review_service(review_id, site_id)