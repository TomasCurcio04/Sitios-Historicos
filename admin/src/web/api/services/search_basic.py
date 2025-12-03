"""Servicio de búsqueda básico sin PostGIS"""

import math
from sqlalchemy import and_, or_, func
from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.category import Category
from src.core.entity.state import State


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula distancia entre dos puntos usando fórmula Haversine"""
    R = 6371  # Radio de la Tierra en km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def search_sites_nearby_basic(lat, lng, radius_km=10, filters=None):
    """Búsqueda por proximidad usando coordenadas lat/lng actuales"""
    if filters is None:
        filters = {}

    # Query base - filtrar por rango aproximado primero
    lat_range = radius_km / 111.0  # Aproximadamente 111 km por grado
    lng_range = radius_km / (111.0 * math.cos(math.radians(lat)))

    query = db.session.query(Site).filter(
        and_(
            Site.is_visible,
            ~Site.deleted,
            Site.latitude.between(lat - lat_range, lat + lat_range),
            Site.longitude.between(lng - lng_range, lng + lng_range),
        )
    )

    # Aplicar filtros
    if filters.get("city"):
        query = query.filter(Site.city.ilike(f"%{filters['city']}%"))

    if filters.get("category_id"):
        query = query.filter(Site.category == filters["category_id"])

    if filters.get("state_id"):
        query = query.filter(Site.state == filters["state_id"])

    sites = query.all()

    # Filtrar por distancia exacta y ordenar
    nearby_sites = []
    for site in sites:
        if site.latitude and site.longitude:
            distance = haversine_distance(
                lat, lng, float(site.latitude), float(site.longitude)
            )
            if distance <= radius_km:
                nearby_sites.append((site, distance))

    # Ordenar por distancia
    nearby_sites.sort(key=lambda x: x[1])

    return [site for site, _ in nearby_sites]


def search_sites_by_filters(filters=None):
    """Búsqueda por filtros sin coordenadas"""
    if filters is None:
        filters = {}

    query = db.session.query(Site).filter(
        and_(Site.is_visible == True, Site.deleted == False)
    )

    if filters.get("text"):
        search_text = filters["text"]
        query = query.filter(
            or_(
                Site.name.ilike(f"%{search_text}%"),
                Site.short_description.ilike(f"%{search_text}%"),
                Site.city.ilike(f"%{search_text}%"),
            )
        )

    if filters.get("city"):
        query = query.filter(Site.city.ilike(f"%{filters['city']}%"))

    if filters.get("category_id"):
        query = query.filter(Site.category == filters["category_id"])

    if filters.get("state_id"):
        query = query.filter(Site.state == filters["state_id"])

    if filters.get("conservation_state"):
        query = query.filter(Site.conservation_state == filters["conservation_state"])

    if filters.get("year_from"):
        query = query.filter(Site.inauguration_year >= filters["year_from"])

    if filters.get("year_to"):
        query = query.filter(Site.inauguration_year <= filters["year_to"])

    return query.all()


def site_to_search_result(site, distance=None):
    """Convierte Site a resultado de búsqueda"""
    result = {
        "id": site.id_site,
        "name": site.name,
        "short_description": site.short_description,
        "city": site.city,
        "state": site.state_rel.name if site.state_rel else None,
        "category": site.category_rel.name if site.category_rel else None,
        "latitude": float(site.latitude) if site.latitude else None,
        "longitude": float(site.longitude) if site.longitude else None,
        "conservation_state": site.conservation_state,
        "inauguration_year": site.inauguration_year,
    }

    if distance is not None:
        result["distance_km"] = round(distance, 2)

    return result
