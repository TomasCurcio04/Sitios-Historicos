"""Servicio de búsqueda geoespacial estilo ZonaProp"""

from sqlalchemy import func, and_, or_
from geoalchemy2.functions import ST_DWithin, ST_Distance, ST_GeogFromText
from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.category import Category
from src.core.entity.state import State


def search_sites_nearby(lat, lng, radius_km=10, filters=None):
    """
    Busca sitios cerca de una ubicación (estilo ZonaProp)
    
    Args:
        lat: Latitud del punto de búsqueda
        lng: Longitud del punto de búsqueda  
        radius_km: Radio de búsqueda en kilómetros
        filters: Diccionario con filtros adicionales
    """
    if filters is None:
        filters = {}
    
    # Crear punto de búsqueda
    search_point = func.ST_GeogFromText(f'POINT({lng} {lat})')
    
    # Query base
    query = db.session.query(Site).filter(
        and_(
            Site.is_visible == True,
            Site.deleted == False,
            ST_DWithin(Site.location, search_point, radius_km * 1000)  # metros
        )
    )
    
    # Aplicar filtros adicionales
    if filters.get('city'):
        query = query.filter(Site.city.ilike(f"%{filters['city']}%"))
    
    if filters.get('category_id'):
        query = query.filter(Site.category == filters['category_id'])
    
    if filters.get('state_id'):
        query = query.filter(Site.state == filters['state_id'])
    
    if filters.get('conservation_state'):
        query = query.filter(Site.conservation_state == filters['conservation_state'])
    
    if filters.get('year_from'):
        query = query.filter(Site.inauguration_year >= filters['year_from'])
    
    if filters.get('year_to'):
        query = query.filter(Site.inauguration_year <= filters['year_to'])
    
    # Ordenar por distancia
    query = query.order_by(ST_Distance(Site.location, search_point))
    
    return query.all()


def search_sites_by_text(search_text, filters=None):
    """Búsqueda por texto en nombre y descripción"""
    if filters is None:
        filters = {}
    
    query = db.session.query(Site).filter(
        and_(
            Site.is_visible == True,
            Site.deleted == False,
            or_(
                Site.name.ilike(f"%{search_text}%"),
                Site.short_description.ilike(f"%{search_text}%"),
                Site.city.ilike(f"%{search_text}%")
            )
        )
    )
    
    # Aplicar filtros adicionales (mismo código que arriba)
    if filters.get('city'):
        query = query.filter(Site.city.ilike(f"%{filters['city']}%"))
    
    if filters.get('category_id'):
        query = query.filter(Site.category == filters['category_id'])
    
    return query.all()


def get_search_filters():
    """Obtiene opciones para filtros de búsqueda"""
    categories = db.session.query(Category).all()
    states = db.session.query(State).all()
    cities = db.session.query(Site.city).distinct().all()
    
    return {
        'categories': [{'id': c.id_category, 'name': c.name} for c in categories],
        'states': [{'id': s.id_state, 'name': s.name} for s in states],
        'cities': [city[0] for city in cities if city[0]]
    }