"""Servicio para manejo de sitios favoritos."""

from src.core.entity.site_favorite import SiteFavorite
from src.core.database import db


def toggle_site_favorite(site_id, public_user_id):
    """Alterna el estado de favorito de un sitio para un usuario.

    Args:
        site_id: ID del sitio
        public_user_id: ID del usuario público

    Returns:
        bool: True si se agregó a favoritos, False si se removió
    """
    favorite = (
        db.session.query(SiteFavorite)
        .filter_by(id_site=site_id, id_public_user=public_user_id)
        .first()
    )

    if favorite:
        # Si existe, lo removemos
        db.session.delete(favorite)
        db.session.commit()
        return False
    # Si no existe, lo agregamos
    new_favorite = SiteFavorite(id_site=site_id, id_public_user=public_user_id)
    db.session.add(new_favorite)
    db.session.commit()
    return True


def is_site_favorite(site_id, public_user_id):
    """Verifica si un sitio está marcado como favorito por un usuario.

    Args:
        site_id: ID del sitio
        public_user_id: ID del usuario público

    Returns:
        bool: True si está en favoritos, False caso contrario
    """
    return (
        db.session.query(SiteFavorite)
        .filter_by(id_site=site_id, id_public_user=public_user_id)
        .first()
        is not None
    )


def get_user_favorites(public_user_id, page=1, per_page=25):
    """Obtiene los sitios favoritos de un usuario con paginación.

    Args:
        public_user_id: ID del usuario público
        page: Página actual
        per_page: Elementos por página

    Returns:
        dict: Diccionario con items, total, page, per_page, pages
    """
    import math

    query = db.session.query(SiteFavorite).filter_by(id_public_user=public_user_id)
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    pages = math.ceil(total / per_page)

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
    }
