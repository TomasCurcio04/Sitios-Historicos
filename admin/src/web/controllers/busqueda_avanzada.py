"""Controlador de búsqueda avanzada de sitios históricos."""

from flask import Blueprint, request, render_template, flash, redirect, url_for
from datetime import datetime
from src.core.services.board.busqueda_avanzada_serv import buscar_sites, obtener_provincias_con_sitios, get_page_items, get_total_results, ordenar_query, get_total_pages
from src.core.services.board.tag_serv import obtener_todas_las_tags
from src.core.entity.site import Site

bp = Blueprint('busqueda_avanzada', __name__, url_prefix='/busqueda')

def parse_date(s):
    """Convierte string de fecha a objeto date.
    
    Args:
        s: String de fecha en formato YYYY-MM-DD
    
    Returns:
        Objeto date o None si es inválido
    """
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

@bp.get('/')
def index():
    """Página principal de búsqueda avanzada con filtros múltiples."""
    ciudad = request.args.get("ciudad", "").strip()
    provincia = request.args.get("provincia", "").strip()
    estado = request.args.get("estado", "").strip()
    visibilidad = request.args.get("visibilidad")
    busqueda_texto = request.args.get("busqueda_texto", "").strip()
    tags = [int(t) for t in request.args.getlist("tags") if t.isdigit()]
    fecha_desde = parse_date(request.args.get("fecha_desde"))
    fecha_hasta = parse_date(request.args.get("fecha_hasta"))

    sort = request.args.get("sort", "date_registered")
    order = request.args.get("order", "desc")
    per_page = int(request.args.get("per_page", 25))
    page = int(request.args.get("page", 1))

    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        flash("El rango de fechas es inválido: 'Desde' no puede ser mayor que 'Hasta'.", "error")
        return redirect(url_for("busqueda_avanzada.index"))

    query = buscar_sites({
        "ciudad": ciudad,
        "provincia": provincia,
        "estado": estado,
        "visibilidad": visibilidad,
        "busqueda_texto": busqueda_texto,
        "tags": tags,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta
    })  

    all_tags = obtener_todas_las_tags()
    provincias = obtener_provincias_con_sitios()
    query = ordenar_query(query, sort, order)
    total_pages = get_total_pages( query, per_page)
    page_items = get_page_items(query, page, per_page)
    total_results = get_total_results(query)
    
    return render_template(
        "busqueda/index.html",
        results=page_items,
        tags=all_tags,
        provincias=provincias,
        ciudad=ciudad,
        provincia=provincia,
        estado=estado,
        selected_tags=tags,
        visibilidad=visibilidad,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        busqueda_texto=busqueda_texto,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        sort=sort,
        order=order,
        total_results=total_results,
        request=request
    )

