from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from src.core.board.tag import Tag
from src.core.database import db

bp = Blueprint("tags", __name__, url_prefix="/etiquetas")


# Función auxiliar para filtros, orden y paginación
def get_tags_with_filters():
    texto = request.args.get("texto", "").strip()
    page = int(request.args.get("page", 1))
    per_page = 25
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")

    session = db.session
    query = session.query(Tag)
    if texto:
        query = query.filter(Tag.name.ilike(f"%{texto}%"))

    tags = query.all()

    # Ordenamiento
    if sort == "name":
        tags.sort(key=lambda t: t.name.lower(), reverse=(order=="desc"))
    elif sort == "fecha_creacion":
        tags.sort(key=lambda t: t.date_created, reverse=(order=="desc"))

    total_results = len(tags)
    total_pages = (total_results + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_items = tags[start:end]

    return {
        "tags": page_items,
        "texto": texto,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "sort": sort,
        "order": order,
        "total_results": total_results
    }


# Menú principal
@bp.get("/")
def menu_tags():
    return render_template("tags/menu.html")


# Listar etiquetas
@bp.get("/listar")
def list_tags():
    context = get_tags_with_filters()
    context["endpoint"] = "tags.list_tags"
    return render_template("tags/listar.html", **context)


# Crear etiqueta
@bp.get("/crear")
def create_tag_form():
    return render_template("tags/crear.html")


@bp.post("/crear")
def create_tag():
    name = request.form.get("name", "").strip()
    if not name:
        flash("El nombre es obligatorio", "error")
        return redirect(url_for("tags.create_tag_form"))

    session = db.session
    tag = Tag(name=name)
    session.add(tag)
    try:
        session.commit()
        flash("Etiqueta creada correctamente", "success")
    except IntegrityError:
        session.rollback()
        flash("Ya existe una etiqueta con ese nombre", "error")

    return redirect(url_for("tags.create_tag_form"))


# Editar etiqueta individual (POST)
@bp.post("/editar/<int:tag_id>")
def edit_tag(tag_id):
    name = request.form.get("name", "").strip()
    if not name:
        flash("El nombre es obligatorio", "error")
        return redirect(url_for("tags.edit_all_tags"))

    session = db.session
    tag = session.query(Tag).get(tag_id)
    if not tag:
        flash("Etiqueta no encontrada", "error")
        return redirect(url_for("tags.edit_all_tags"))

    tag.name = name
    tag.slug = Tag.generate_slug(name)
    try:
        session.commit()
        flash("Etiqueta actualizada correctamente", "success")
    except IntegrityError:
        session.rollback()
        flash("Ya existe una etiqueta con ese nombre", "error")
    return redirect(url_for("tags.edit_all_tags"))


# Página de edición de todas las etiquetas
@bp.get("/editar")
def edit_all_tags():
    context = get_tags_with_filters()
    context["endpoint"] = "tags.edit_all_tags"
    return render_template("tags/actualizar.html", **context)


# Página de eliminación de todas las etiquetas
@bp.get("/eliminar")
def delete_all_tags():
    context = get_tags_with_filters()
    context["endpoint"] = "tags.delete_all_tags"
    return render_template("tags/eliminar.html", **context)


# Eliminar etiqueta individual
@bp.post("/eliminar/<int:tag_id>")
def delete_tag(tag_id):
    session = db.session
    tag = session.query(Tag).get(tag_id)
    if not tag:
        flash("Etiqueta no encontrada", "error")
        return redirect(url_for("tags.delete_all_tags"))

    if tag.sites:
        flash("No se puede eliminar un tag asignado a sitios", "error")
        return redirect(url_for("tags.delete_all_tags"))

    session.delete(tag)
    session.commit()
    flash("Etiqueta eliminada correctamente", "success")
    return redirect(url_for("tags.delete_all_tags"))
