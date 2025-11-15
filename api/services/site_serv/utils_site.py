"""Funciones auxiliares para el servicio de sitios"""

from collections import OrderedDict
from api.services.site_serv import listar_sitios
from src.core.database import db
from src.core.entity.site_image import SiteImage


def site_to_dict(site):
    """Convierte un objeto Site a diccionario según especificación API."""
    # Limitar tags a máximo 5 para el portal público
    tags = [tag.name for tag in site.tag[:5]] if site.tag else []
    
    # Imagen de portada (buscar thumbnail o primera disponible)
    cover_image = None
    try:
        # Buscar primero la imagen thumbnail
        thumbnail = db.session.query(SiteImage).filter(
            SiteImage.id_site == site.id_site,
            SiteImage.is_thumbnail == True
        ).first()
        
        if thumbnail:
            cover_image = thumbnail.file_path
        else:
            # Si no hay thumbnail, tomar la primera imagen
            first_image = db.session.query(SiteImage).filter(
                SiteImage.id_site == site.id_site
            ).first()
            if first_image:
                cover_image = first_image.file_path
    except Exception:
        cover_image = None
    
    return {
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
        "inserted_at": site.date_registered.isoformat() + "Z" if site.date_registered else None,
        "updated_at": site.date_registered.isoformat() + "Z" if site.date_registered else None
    }


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
            "total": result["total"]
        }
    }
