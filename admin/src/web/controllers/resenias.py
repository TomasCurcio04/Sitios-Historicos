"""Controlador de moderación de reseñas para sitios históricos."""

from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.services.board.resenias import paginar_lista
from src.web.handlers.utils import permissions_required
from datetime import datetime
from src.core.services.board.resenias import buscar_review

bp = Blueprint("gestion_resenias", __name__, url_prefix="/moderacion_resenias")



def parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


@bp.get('/')
def index():

    """Muestra el menú principal de moderación de reseñas."""

    sitio = request.args.get("ciudad", "").strip()
    email_usuario = request.args.get("email_usuario", "").strip()
    puntuacion = request.args.get("puntuacion", "").strip()
    contenido = request.args.get("contenido", "").strip()
    estado = request.args.get("estado", "").strip()
    fecha_desde = parse_date(request.args.get("fecha_desde"))
    fecha_hasta = parse_date(request.args.get("fecha_hasta"))


    per_page = int(request.args.get("per_page", 25))
    page = int(request.args.get("page", 1))


    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        flash("El rango de fechas es inválido: 'Desde' no puede ser mayor que 'Hasta'.", "error")


    results=buscar_review({
        "sitio": sitio,
        "email_usuario": email_usuario,
        "puntuacion": puntuacion,
        "contenido": contenido,
        "estado": estado,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
    })

    # Paginación
    page_items, total_pages, total_results = paginar_lista(results, page, per_page)
    total_pages = max(1, total_pages)

    return render_template(
        "resenias/moderacion_resenias.html",
         results=page_items,
         total_pages=total_pages,
         total_results=total_results,
         sitio=sitio,
         email_usuario=email_usuario,
         puntuacion=puntuacion,
         contenido=contenido,
         estado=estado,
         fecha_desde=fecha_desde,
         fecha_hasta=fecha_hasta,
         per_page=per_page,
         page=page,

    )
