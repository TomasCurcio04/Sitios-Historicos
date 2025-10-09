from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from sqlalchemy import or_, distinct
from src.core.board.site import Site
from src.core.board.tag import Tag
from src.core.database import db
from src.core.board.state import State
bp = Blueprint('busqueda_avanzada', __name__, url_prefix='/busqueda')


def parse_date(s):
    """Convierte string a datetime.date, devuelve None si falla."""
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


@bp.get('/')
def index():
    # -------------------- Leer parámetros --------------------
    ciudad = request.args.get("ciudad", "").strip()
    provincia = request.args.get("provincia", "").strip()
    estado = request.args.get("estado", "").strip()
    visibilidad = request.args.get("visibilidad")
    busqueda_texto = request.args.get("busqueda_texto", "").strip()
    tags = [int(t) for t in request.args.getlist("tags") if t.isdigit()]
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 25))
    sort = request.args.get("sort", "date_registered")
    order = request.args.get("order", "desc")
    fecha_desde = parse_date(request.args.get("fecha_desde"))
    fecha_hasta = parse_date(request.args.get("fecha_hasta"))

    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        flash("El rango de fechas es inválido: 'Desde' no puede ser mayor que 'Hasta'.", "error")
        return redirect(url_for("busqueda_avanzada.index"))

    session = db.session
    query = session.query(Site)

    # -------------------- Filtros --------------------
    if ciudad:
        query = query.filter(Site.city.ilike(f"%{ciudad}%"))
    
    if provincia:
        query = query.filter(Site.province.ilike(f"%{provincia}%"))
    
    if estado:
        query = query.filter(Site.conservation_state.ilike(f"%{estado}%"))
    
    if visibilidad == "true":
        query = query.filter(Site.is_visible.is_(True))
    elif visibilidad == "false":
        query = query.filter(Site.is_visible.is_(False))
    
    if fecha_desde:
        query = query.filter(Site.date_registered >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Site.date_registered <= fecha_hasta)
    
    if busqueda_texto:
        busqueda_texto_like = f"%{busqueda_texto}%"
        query = query.filter(
            or_(
                Site.name.ilike(busqueda_texto_like),
                Site.full_description.ilike(busqueda_texto_like)
            )
        )
    
    if tags:
        query = query.join(Site.tag).filter(Tag.id_tag.in_(tags))

    # -------------------- Ordenamiento --------------------
    if sort in ["name", "date_registered", "city"]:
        col = getattr(Site, sort)
        if order == "desc":
            col = col.desc()
        query = query.order_by(col)

    # -------------------- Paginación --------------------
    total_results = query.count()
    total_pages = (total_results + per_page - 1) // per_page
    page_items = query.offset((page - 1) * per_page).limit(per_page).all()

    # -------------------- Traer todos los tags y provincias --------------------
    all_tags = session.query(Tag).all()
    provincias = [p[0] for p in 
                  session.query(distinct(State.name))
                         .join(Site, Site.state == State.id_state)
                         .order_by(State.name)
                         .all()]

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
