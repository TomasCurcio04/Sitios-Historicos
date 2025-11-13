"""Servicios de sitios para la API"""

from sqlalchemy import func, or_
from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.state import State
from src.core.entity.tag import Tag
from src.core.entity.site import site_tag


def listar_sitios(name=None, description=None, city=None, province=None, tags=None, 
                  order_by=None, lat=None, long=None, radius=None, page=1, per_page=20):
    """Listar sitios con filtros y paginación"""
    query = db.session.query(Site).filter(Site.is_visible, ~Site.deleted)
    
    # Filtro por nombre
    if name:
        query = query.filter(Site.name.ilike(f'%{name}%'))
    
    # Filtro por descripción
    if description:
        query = query.filter(or_(
            Site.short_description.ilike(f'%{description}%'),
            Site.full_description.ilike(f'%{description}%')
        ))
    
    # Filtro por ciudad
    if city:
        query = query.filter(Site.city.ilike(city))
    
    # Filtro por provincia
    if province:
        query = query.join(State).filter(State.name.ilike(province))
    
    # Filtro por tags
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        query = query.join(site_tag).join(Tag).filter(Tag.name.in_(tag_list))
    
    # Filtro geoespacial
    if lat and long and radius:
        distance = func.sqrt(
            func.pow(69.1 * (Site.latitude - lat), 2) +
            func.pow(69.1 * (Site.longitude - long) * func.cos(Site.latitude / 57.3), 2)
        )
        query = query.filter(distance <= radius)
    
    # Ordenamiento
    if order_by == 'latest':
        query = query.order_by(Site.date_registered.desc())
    elif order_by == 'oldest':
        query = query.order_by(Site.date_registered.asc())
    else:
        query = query.order_by(Site.id_site)
    
    # Paginación
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        'total': total,
        'page': page,
        'per_page': per_page,
        'items': items
    }
