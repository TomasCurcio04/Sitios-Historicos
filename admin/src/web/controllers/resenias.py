"""Controlador de moderación de reseñas para sitios históricos."""

from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.web.handlers.utils import permissions_required
from src.core.services.board.resenias import (
    buscar_review_con_filtros,
    ordenar_lista,
    eliminar_review,
    paginar_lista,
    aprobar_review,
    buscar_review_por_id,
    rechazar_review,
    obtener_sitios_con_reviews,
)
from src.core.services.auth.user_serv import usuario_actual

bp = Blueprint("gestion_resenias", __name__, url_prefix="/moderacion_resenias")


def parse_date(s):
    """Parseo de una fecha en formato YYYY-MM-DD."""
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


@bp.get("/")
@permissions_required("review", ["list"])
def index():
    """Muestra el menú principal de moderación de reseñas.

    Args:
        Ninguno

    Returns:
        Renderiza la plantilla de moderación de reseñas con los resultados filtrados y paginados.
    """

    sitio = request.args.getlist("sitio")
    sitio = [int(s) for s in sitio if s.strip()]

    email_usuario = request.args.get("email_usuario", "").strip()
    puntuacion = request.args.getlist("puntuacion")
    contenido = request.args.get("contenido", "").strip()
    estado = request.args.get("estado", "").strip()
    fecha_desde = parse_date(request.args.get("fecha_desde"))
    fecha_hasta = parse_date(request.args.get("fecha_hasta"))
    sort = request.args.get("sort", "date_created")
    order = request.args.get("order", "desc")

    per_page = int(request.args.get("per_page", 25))
    page = int(request.args.get("page", 1))

    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        flash(
            "El rango de fechas es inválido: 'Desde' no puede ser mayor que 'Hasta'.",
            "error",
        )

    results = buscar_review_con_filtros(
        {
            "sitio": sitio,
            "email_usuario": email_usuario,
            "puntuacion": puntuacion,
            "contenido": contenido,
            "estado": estado,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
        }
    )

    results = ordenar_lista(results, sort, order)

    # Paginación
    page_items, total_pages, total_results = paginar_lista(results, page, per_page)
    total_pages = max(1, total_pages)

    todos_sitios = obtener_sitios_con_reviews()
    return render_template(
        "resenias/moderacion_resenias.html",
        results=page_items,
        total_pages=total_pages,
        total_results=total_results,
        sitio=sitio,
        email_usuario=email_usuario,
        puntuacion=[str(p) for p in puntuacion],
        contenido=contenido,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        per_page=per_page,
        page=page,
        sort=sort,
        order=order,
        sitios=todos_sitios,
    )


@bp.post("/eliminar/<int:id_review>")
@permissions_required("review", ["delete"])
def delete_review(id_review):
    """Procesa la eliminación de una etiqueta.
    Args:
        id_review (int): ID de la reseña a eliminar.
    Returns:
        Redirige a la página principal de moderación de reseñas con un mensaje de éxito o error
    """
    _, error = eliminar_review(id_review)
    if error:
        flash(error, "error")
    else:
        flash("Reseña eliminada correctamente", "success")
    return redirect(url_for("gestion_resenias.index"))


@bp.post("/aprobar/<int:id_review>")
@permissions_required("review", ["moderate"])
def approve_review(id_review):
    """Procesa la aprobación de una reseña.
    Args:
        id_review (int): ID de la reseña a aprobar.
    Returns:
        Redirige a la página principal de moderación de reseñas con un mensaje de éxito o error
    """

    usuario = usuario_actual()

    _, error = aprobar_review(id_review, usuario.id_user)

    if error:
        flash(error, "error")
    else:
        flash("Reseña aprobada correctamente", "success")

    return redirect(url_for("gestion_resenias.index"))


@bp.get("/detalle/<int:id_review>")
@permissions_required("review", ["moderate"])
def review_detail(id_review):
    """Muestra el detalle de una reseña para moderación.
    Args:
        id_review (int): ID de la reseña a mostrar.
    Returns:
        Renderiza la plantilla de detalle de reseña.
    """
    review = buscar_review_por_id(id_review)
    if not review:
        flash("La reseña no existe", "error")
        return redirect(url_for("gestion_resenias.index"))
    return render_template("resenias/detalle_resenias.html", review=review)


@bp.post("/rechazar/<int:id_review>")
@permissions_required("review", ["moderate"])
def reject_review(id_review):
    """Procesa el rechazo de una reseña.
    Args:
        id_review (int): ID de la reseña a rechazar.
    Returns:
        Redirige a la página principal de moderación de reseñas con un mensaje de éxito o error
    """

    usuario = usuario_actual()

    reject_reason = request.form.get("rejection_reason", "").strip()
    if not reject_reason:
        flash("Debe proporcionar una razón para el rechazo.", "error")
        return redirect(url_for("gestion_resenias.review_detail", id_review=id_review))
    if len(reject_reason) > 200:
        flash("La razón de rechazo no puede exceder los 200 caracteres.", "error")
        return redirect(url_for("gestion_resenias.review_detail", id_review=id_review))
    _, error = rechazar_review(id_review, usuario.id_user, reject_reason)
    if error:
        flash(error, "error")
    else:
        flash("Reseña rechazada correctamente", "success")

    return redirect(url_for("gestion_resenias.index"))
