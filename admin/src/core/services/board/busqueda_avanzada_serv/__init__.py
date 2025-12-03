"""Servicio de búsqueda avanzada de sitios históricos."""

from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.tag import Tag
from sqlalchemy import or_, distinct
from src.core.entity.state import State


def buscar_sites(filtros):
    """Devuelve una lista de sitios filtrados según los parámetros de búsqueda."""
    query = db.session.query(Site)

    if filtros.get("ciudad"):
        query = query.filter(Site.city.ilike(f"%{filtros['ciudad']}%"))
    if filtros.get("provincia"):
        query = query.join(Site.state_rel).filter(
            State.name.ilike(f"%{filtros['provincia']}%")
        )
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

    # Ejecutar la query y devolver lista de diccionarios
    resultados = []
    for site in query.all():
        resultados.append(
            {
                "id": site.id_site,
                "name": site.name,
                "city": site.city,
                "state": site.state_rel.name if site.state_rel else None,
                "conservation_state": site.conservation_state,
                "is_visible": site.is_visible,
                "date_registered": (
                    site.date_registered.isoformat() if site.date_registered else None
                ),
                "tags": [t.id_tag for t in site.tag],
            }
        )
    return resultados


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


def ordenar_lista(results, sort, order):
    """Ordena una lista de diccionarios según un campo."""
    if sort in ["name", "date_registered", "city"]:
        results.sort(key=lambda r: r.get(sort), reverse=(order == "desc"))
    return results


def paginar_lista(results, page, per_page):
    """Devuelve los items de la página indicada y total de páginas."""
    total_results = len(results)
    total_pages = (total_results + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_items = results[start:end]
    return page_items, total_pages, total_results
