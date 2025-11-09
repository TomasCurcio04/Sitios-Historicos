"""Servicios de sitios para la API"""

from src.core.services.board import list_sites


def site_to_dict(site):
    """Convierte un objeto Site a diccionario."""
    return {
        'id': site.id_site,
        'name': site.name,
        'short_description': site.short_description,
        'city': site.city,
        'latitude': float(site.latitude) if site.latitude else None,
        'longitude': float(site.longitude) if site.longitude else None,
        'is_visible': site.is_visible
    }


def all_sites_to_json():
    """Listar todos los sitios en formato json"""
    sites = list_sites()
    var_return = []

    # Convertir sitios a formato JSON
    if isinstance(sites, list):
        var_return = [site_to_dict(site) for site in sites]
    else:
        var_return = [site_to_dict(site) for site in sites.get("items", [])]

    return var_return
