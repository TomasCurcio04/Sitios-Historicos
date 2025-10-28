"""Servicio de búsqueda avanzada de sitios históricos."""

from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.tag import Tag
from sqlalchemy import or_, distinct
from src.core.entity.state import State

def buscar_sites(filtros):
    """Construye query filtrada de sitios según criterios de búsqueda.
    
    Args:
        filtros: Dict con criterios de búsqueda
    
    Returns:
        Query de SQLAlchemy filtrada
    """
    query = db.session.query(Site)

    if filtros.get("ciudad"):
        query = query.filter(Site.city.ilike(f"%{filtros['ciudad']}%"))
    if filtros.get("provincia"):
        query = query.join(Site.state_rel).filter(State.name.ilike(f"%{filtros['provincia']}%"))
    if filtros.get("estado"):
        query = query.filter(Site.conservation_state.ilike(f"%{filtros['estado']}%"))
    if filtros.get("visibilidad") == "true":
        query = query.filter(Site.is_visible.is_(True))
    elif filtros.get("visibilidad") == "false":
        query = query.filter(Site.is_visible.is_(False))
    if filtros.get("fecha_desde"):
        query = query.filter(Site.date_registered >= filtros["fecha_desde"])
    if filtros.get("fecha_hasta"):
        query = query.filter(Site.date_registered <= filtros["fecha_hasta"])
    if filtros.get("busqueda_texto"):
        texto = f"%{filtros['busqueda_texto']}%"
        query = query.filter(
            or_(Site.name.ilike(texto), Site.full_description.ilike(texto))
        )
    if filtros.get("tags"):
        query = query.join(Site.tag).filter(Tag.id_tag.in_(filtros["tags"])).distinct()

    return query

def obtener_provincias_con_sitios():
    """Obtiene provincias que tienen al menos un sitio registrado.
    
    Returns:
        Lista de nombres de provincias
    """
    resultados = (
        db.session.query(distinct(State.name))
        .join(Site, Site.state == State.id_state)
        .order_by(State.name)
        .all()
    )
    return [r[0] for r in resultados]

    # Ordenamiento
def ordenar_query(query, sort, order):
    """Aplica ordenamiento a la query.
    
    Args:
        query: Query de SQLAlchemy
        sort: Campo por el cual ordenar
        order: Dirección del ordenamiento (asc/desc)
    
    Returns:
        Query ordenada
    """
    if sort in ["name", "date_registered", "city"]:
        col = getattr(Site, sort)
        if order == "desc":
            col = col.desc()
        query = query.order_by(col)
    return query

    # Conteo total
def get_total_results(query):
    """Cuenta el total de resultados de la query.
    
    Args:
        query: Query de SQLAlchemy
    
    Returns:
        Número total de resultados
    """
    return query.count()

def get_total_pages(query, per_page):
    """Calcula el número total de páginas.
    
    Args:
        query: Query de SQLAlchemy
        per_page: Elementos por página
    
    Returns:
        Número total de páginas
    """
    return (get_total_results(query) + per_page - 1) // per_page

def get_page_items(query, page, per_page):
    """Obtiene los elementos de una página específica.
    
    Args:
        query: Query de SQLAlchemy
        page: Número de página
        per_page: Elementos por página
    
    Returns:
        Lista de sitios de la página
    """
    return query.offset((page - 1) * per_page).limit(per_page).all()

    return page_items
