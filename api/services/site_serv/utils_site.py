"""Funciones auxiliares para el servicio de sitios"""

from collections import OrderedDict
from api.services.site_serv import listar_sitios


def site_to_dict(site):
    """Convierte un objeto Site a diccionario."""
    return {
        "id": site.id_site,
        "name": site.name,
        "short_description": site.short_description,
        "full_description": site.full_description,
        "city": site.city,
        "state": site.state,
        "latitude": float(site.latitude) if site.latitude else None,
        "longitude": float(site.longitude) if site.longitude else None,
        "conservation_state": site.conservation_state,
        "inauguration_year": site.inauguration_year,
        "category": site.category,
        "date_registered": (
            site.date_registered.isoformat() if site.date_registered else None
        ),
        "is_visible": site.is_visible,
        "deleted": site.deleted,
        "created_by": site.created_by,
    }


def all_sites_to_json(**kwargs):
    """Listar sitios en formato json con filtros"""
    result = listar_sitios(**kwargs)

    # Convertir sitios a formato JSON
    items = [site_to_dict(site) for site in result["items"]]

    var_return = OrderedDict(
        [
            ("total", result["total"]),
            ("page", result["page"]),
            ("per_page", result["per_page"]),
            ("items", items),
        ]
    )

    return var_return
