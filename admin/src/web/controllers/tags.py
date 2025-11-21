"""Controlador de gestión de etiquetas para sitios históricos."""

from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.services.board.tag_serv import buscar_tags, crear_tag, actualizar_tag, eliminar_tag
from src.web.handlers.utils import permissions_required

bp = Blueprint("tags", __name__, url_prefix="/etiquetas")


@bp.get("/")
@permissions_required("tag", ["view"])
def menu_tags():

    """Muestra el menú principal de gestión de etiquetas."""
    return render_template("tags/menu.html")

    
@bp.get("/listar")
@permissions_required("tag", ["view"])
def list_tags():
    """Lista todas las etiquetas con filtros aplicados."""
    filtros = request.args.to_dict()
    context = buscar_tags(filtros)
    context["endpoint"] = "tags.list_tags"
    return render_template("tags/listar.html", **context)


@bp.get("/crear")
@permissions_required("tag", ["create"])
def create_tag_form():
    """Muestra el formulario para crear una nueva etiqueta."""
    return render_template("tags/crear.html")


@bp.post("/crear")
@permissions_required("tag", ["create"])
def create_tag():
    """Procesa la creación de una nueva etiqueta."""
    name = request.form.get("name", "").strip()
    if not name:
        flash("El nombre es obligatorio", "error")
        return redirect(url_for("tags.create_tag_form"))
    if len(name) < 3:
        flash("El nombre debe tener al menos 3 caracteres", "error")
        return redirect(url_for("tags.create_tag_form"))
    tag, error = crear_tag(name)
    if error:
        flash(error, "error")
    else:
        flash("Etiqueta creada correctamente", "success")

    return redirect(url_for("tags.create_tag_form"))


@bp.post("/editar/<int:tag_id>")
@permissions_required("tag", ["edit"])
def edit_tag(tag_id):
    """Procesa la actualización de una etiqueta existente."""
    name = request.form.get("name", "").strip()
    if not name:
        flash("El nombre es obligatorio", "error")
        return redirect(url_for("tags.edit_all_tags"))
    if len(name) < 3:
        flash("El nombre debe tener al menos 3 caracteres", "error")
        return redirect(url_for("tags.edit_all_tags"))
    tag, error = actualizar_tag(tag_id, name)
    if error:
        flash(error, "error")
    else:
        flash("Etiqueta actualizada correctamente", "success")
    return redirect(url_for("tags.edit_all_tags"))


@bp.get("/editar")
@permissions_required("tag", ["edit"])
def edit_all_tags():
    """Muestra la lista de etiquetas para edición."""
    filtros = request.args.to_dict()
    context = buscar_tags(filtros)
    context["endpoint"] = "tags.edit_all_tags"
    return render_template("tags/editar.html", **context)


@bp.get("/eliminar")
@permissions_required("tag", ["delete"])
def delete_all_tags():
    """Muestra la lista de etiquetas para eliminación."""
    filtros = request.args.to_dict()
    context = buscar_tags(filtros)
    context["endpoint"] = "tags.delete_all_tags"
    return render_template("tags/eliminar.html", **context)


@bp.post("/eliminar/<int:tag_id>")
@permissions_required("tag", ["delete"])
def delete_tag(tag_id):
    """Procesa la eliminación de una etiqueta."""
    tag, error = eliminar_tag(tag_id)
    if error:
        flash(error, "error")
    else:
        flash("Etiqueta eliminada correctamente", "success")
    return redirect(url_for("tags.delete_all_tags"))
