"""Funciones auxiliares para el servicio de sitios"""

from collections import OrderedDict
from src.web.api.services.site_serv import listar_sitios, get_site_by_id_service
from src.core.database import db
from src.core.entity.site_image import SiteImage


def site_to_dict(site, include_full_data=False):
    """Convierte un objeto Site a diccionario según especificación API."""
    # Para listado: limitar tags a 5, para detalle: todos los tags
    tags = (
        [tag.name for tag in (site.tag[:5] if not include_full_data else site.tag)]
        if site.tag
        else []
    )

    # Imagen de portada (buscar thumbnail o primera disponible)
    cover_image = None
    images = []

    try:
        # Obtener todas las imágenes si es detalle completo
        if include_full_data:
            all_images = (
                db.session.query(SiteImage)
                .filter(SiteImage.id_site == site.id_site)
                .order_by(SiteImage.display_order, SiteImage.id_site_image)
                .all()
            )

            images = [
                {
                    "id": img.id_site_image,
                    "title": img.title,
                    "description": img.description,
                    "image_path": img.image_path,
                    "is_thumbnail": img.is_thumbnail,
                    "display_order": img.display_order,
                }
                for img in all_images
            ]

        # Buscar imagen thumbnail
        thumbnail = (
            db.session.query(SiteImage)
            .filter(SiteImage.id_site == site.id_site, SiteImage.is_thumbnail)
            .first()
        )

        if thumbnail:
            cover_image = thumbnail.image_path
        else:
            # Si no hay thumbnail, tomar la primera imagen
            first_image = (
                db.session.query(SiteImage)
                .filter(SiteImage.id_site == site.id_site)
                .first()
            )
            if first_image:
                cover_image = first_image.image_path
    except Exception:
        cover_image = None
        images = []

    # Calcular rating promedio y cantidad de reseñas si es detalle completo
    average_rating = None
    review_count = 0

    if include_full_data:
        try:
            from src.core.entity.review import Review, ReviewStatus

            reviews_query = db.session.query(Review).filter(
                Review.id_site == site.id_site,
                Review.status == ReviewStatus.APROBADA,  # Solo reseñas aprobadas
            )

            review_count = reviews_query.count()
            if review_count > 0:
                ratings = [r.rating for r in reviews_query.all()]
                average_rating = sum(ratings) / len(ratings)
        except Exception:
            pass

    result = {
        "id": site.id_site,
        "name": site.name,
        "short_description": site.short_description,
        "description": site.full_description,
        "city": site.city,
        "province": site.state_rel.name if site.state_rel else None,
        "country": "AR",
        "lat": float(site.latitude) if site.latitude else None,
        "long": float(site.longitude) if site.longitude else None,
        "tags": tags,
        "state_of_conservation": site.conservation_state,
        "cover_image": cover_image,
        "inserted_at": (
            site.date_registered.isoformat() + "Z" if site.date_registered else None
        ),
        "updated_at": (
            site.date_registered.isoformat() + "Z" if site.date_registered else None
        ),
    }

    # Agregar datos adicionales para detalle completo
    if include_full_data:
        result.update(
            {
                "images": images,
                "average_rating": round(average_rating, 1) if average_rating else None,
                "review_count": review_count,
            }
        )

    return result


def all_sites_to_json(**kwargs):
    """Listar sitios en formato json con filtros según especificación API"""
    result = listar_sitios(**kwargs)

    # Convertir sitios a formato JSON
    data = [site_to_dict(site) for site in result["items"]]

    return {
        "data": data,
        "meta": {
            "page": result["page"],
            "per_page": result["per_page"],
            "total": result["total"],
        },
    }


def get_site_by_id(site_id):
    """Obtiene un sitio por ID y registra la visita"""
    site = get_site_by_id_service(site_id)

    if not site:
        return None

    return site_to_dict(site, include_full_data=True)


def create_site(site_data, user_id):
    """Crea un nuevo sitio histórico"""
    from src.web.api.services.site_serv import create_site_service

    site = create_site_service(site_data, user_id)
    return site_to_dict(site, include_full_data=True)