"""Servicios API del usuario"""

from src.core.database import db
from src.core.entity.review import Review, ReviewStatus
from src.core.entity.public_user import PublicUser
from src.core.entity.site import Site
from src.web.api.services.review_serv.utils_review import review_to_dict


def obtener_reviews_de_usuario(public_user_id, page, per_page):
    """Obtiene las reseñas de un usuario excluyendo sitios eliminados y no visibles.

    Args:
        public_user_id (int): ID del usuario público
        page (int): Número de página
        per_page (int): Elementos por página

    Returns:
        dict: Diccionario con items, total, page y per_page
    """

    query = (
        db.session.query(Review)
        .join(Site, Review.id_site == Site.id_site)
        .filter(
            Review.id_public_user == public_user_id,
            ~Site.deleted,
            Site.is_visible,
        )
        .order_by(Review.date_created.desc())
    )

    total = query.count()
    reviews = query.offset((page - 1) * per_page).limit(per_page).all()

    # Convertir a formato API
    reviews_data = []
    for review in reviews:
        review_dict = review_to_dict(review, None)
        review_dict["status"] = review.status.value
        review_dict["site_name"] = review.site_rel.name if review.site_rel else None
        reviews_data.append(review_dict)

    return {"items": reviews_data, "total": total, "page": page, "per_page": per_page}
