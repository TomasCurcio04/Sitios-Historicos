from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, session
from sqlalchemy import or_
from src.core.database import db
from src.core.board.site import Site
from src.core.board.tag import Tag
from src.core.board.state import State
from src.core.board.category import Category
import csv
import io

bp = Blueprint("issues", __name__, url_prefix="/sitios")
PER_PAGE = 25

USUARIO_ES_ADMIN = True

# =====================================================
# LISTAR SITIOS CON FILTROS Y PAGINACIÓN
# =====================================================
@bp.get("/")
def index():
    page = int(request.args.get("page", 1))
    per_page = PER_PAGE

    filtros = {
        "nombre": request.args.get("nombre", "").strip(),
        "short_description": request.args.get("short_description", "").strip(),
        "full_description": request.args.get("full_description", "").strip(),
        "city": request.args.get("city", "").strip(),
        "state": request.args.get("state", ""),  # id_state
        "conservation_state": request.args.get("conservation_state", "").strip(),
        "inauguration_year": request.args.get("inauguration_year", "").strip(),
        "latitude": request.args.get("latitude", "").strip(),
        "longitude": request.args.get("longitude", "").strip(),
        "category": request.args.get("category", ""),  # id_category
        "is_visible": request.args.get("is_visible", ""),
        "tags": request.args.getlist("tags"),  # lista de id_tag
    }

    query = db.session.query(Site)

    if filtros["nombre"]:
        query = query.filter(Site.name.ilike(f"%{filtros['nombre']}%"))
    if filtros["short_description"]:
        query = query.filter(Site.short_description.ilike(f"%{filtros['short_description']}%"))
    if filtros["full_description"]:
        query = query.filter(Site.full_description.ilike(f"%{filtros['full_description']}%"))
    if filtros["city"]:
        query = query.filter(Site.city.ilike(f"%{filtros['city']}%"))
    if filtros["state"]:
        query = query.filter(Site.state == int(filtros["state"]))
    if filtros["conservation_state"]:
        query = query.filter(Site.conservation_state.ilike(f"%{filtros['conservation_state']}%"))
    if filtros["inauguration_year"].isdigit():
        query = query.filter(Site.inauguration_year == int(filtros["inauguration_year"]))
    if filtros["latitude"]:
        query = query.filter(Site.latitude == float(filtros["latitude"]))
    if filtros["longitude"]:
        query = query.filter(Site.longitude == float(filtros["longitude"]))
    if filtros["category"]:
        query = query.filter(Site.category == int(filtros["category"]))
    if filtros["is_visible"]:
        query = query.filter(Site.is_visible.is_(filtros["is_visible"] == "1"))
    if filtros["tags"]:
        for tag_id in filtros["tags"]:
            query = query.filter(Site.tag.any(id_tag=int(tag_id)))

    total_sites = query.count()
    total_pages = (total_sites + per_page - 1) // per_page
    sitios = query.offset((page - 1) * per_page).limit(per_page).all()

    # Cargar listas para los selects
    estados = db.session.query(State).all()
    categorias = db.session.query(Category).all()
    etiquetas = db.session.query(Tag).all()

    return render_template(
        "sites/index.html",
        sitios=sitios,
        page=page,
        total_pages=total_pages,
        usuario_es_admin=USUARIO_ES_ADMIN,
        estados=estados,
        categorias=categorias,
        etiquetas=etiquetas
    )

# =====================================================
# CREAR NUEVO SITIO
# =====================================================
@bp.get("/nuevo")
def nuevo():
    estados = db.session.query(State).all()
    categorias = db.session.query(Category).all()
    etiquetas = db.session.query(Tag).all()
    return render_template("sites/form.html", sitio=None, estados=estados, categorias=categorias, etiquetas=etiquetas)

@bp.post("/nuevo")
def crear():
    data = _extraer_y_validar_form()
    if isinstance(data, str):
        flash(data, "error")
        return redirect(url_for("issues.nuevo"))

    # Etiquetas
    tags_ids = request.form.getlist("tags")
    etiquetas = db.session.query(Tag).filter(Tag.id_tag.in_(tags_ids)).all()

    # Obtener el ID del usuario actual (ajusta según tu sistema de login)
    usuario_id = session.get("user_id", 1)  # Usa el ID del usuario logueado, o 1 si no hay login
    data["created_by"] = usuario_id

    nuevo_sitio = Site(**data)
    nuevo_sitio.tag = etiquetas
    db.session.add(nuevo_sitio)
    db.session.commit()

    flash("Sitio creado correctamente", "success")
    return redirect(url_for("issues.index"))

# =====================================================
# EDITAR SITIO
# =====================================================
@bp.get("/<int:site_id>/editar")
def editar(site_id):
    sitio = db.session.get(Site, site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("issues.index"))
    estados = db.session.query(State).all()
    categorias = db.session.query(Category).all()
    etiquetas = db.session.query(Tag).all()
    return render_template("sites/form.html", sitio=sitio, estados=estados, categorias=categorias, etiquetas=etiquetas)

@bp.post("/<int:site_id>/editar")
def actualizar(site_id):
    sitio = db.session.get(Site, site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("issues.index"))

    data = _extraer_y_validar_form()
    if isinstance(data, str):
        flash(data, "error")
        return redirect(url_for("issues.editar", site_id=site_id))

    for key, value in data.items():
        setattr(sitio, key, value)

    # Etiquetas
    tags_ids = request.form.getlist("tags")
    etiquetas = db.session.query(Tag).filter(Tag.id_tag.in_(tags_ids)).all()
    sitio.tag = etiquetas

    db.session.commit()
    flash("Sitio actualizado correctamente", "success")
    return redirect(url_for("issues.index"))

# =====================================================
# ELIMINAR SITIO
# =====================================================
@bp.post("/<int:site_id>/eliminar")
def eliminar(site_id):
    if not USUARIO_ES_ADMIN:
        flash("No tenés permisos para eliminar este sitio.", "error")
        return redirect(url_for("issues.index"))

    sitio = db.session.get(Site, site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("issues.index"))

    db.session.delete(sitio)
    db.session.commit()
    flash("Sitio eliminado correctamente", "success")
    return redirect(url_for("issues.index"))

# =====================================================
# EXPORTAR CSV (TODOS LOS CAMPOS)
# =====================================================
@bp.get("/exportar")
def exportar():
    sitios = db.session.query(Site).all()
    output = io.StringIO()
    output.write('\ufeff')  # BOM para Excel
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)

    campos = [col.name for col in Site.__table__.columns]
    campos.append("tags")  # Exportar etiquetas como texto

    writer.writerow(campos)

    for sitio in sitios:
        fila = [getattr(sitio, campo, "") for campo in Site.__table__.columns]
        fila.append(", ".join([tag.name for tag in sitio.tag]))
        writer.writerow(fila)

    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=sitios_historicos.csv"}
    )

# =====================================================
# FUNCIÓN AUXILIAR DE VALIDACIÓN
# =====================================================
def _extraer_y_validar_form():
    try:
        nombre = request.form.get("nombre", "").strip()
        short_description = request.form.get("short_description", "").strip()
        full_description = request.form.get("full_description", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        latitude = request.form.get("latitude", "").strip()
        longitude = request.form.get("longitude", "").strip()
        conservation_state = request.form.get("conservation_state", "").strip()
        inauguration_year = request.form.get("inauguration_year", "").strip()
        category = request.form.get("category", "").strip()
        is_visible = request.form.get("is_visible", "0") == "1"

        # Validaciones obligatorias
        if not nombre or not city or not state or not category:
            return "Nombre, ciudad, estado y categoría son obligatorios."

        # Etiquetas obligatorias
        tags_ids = request.form.getlist("tags")
        if not tags_ids:
            return "Debes seleccionar al menos una etiqueta."

        # Validación de tipos
        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
            inauguration_year = int(inauguration_year) if inauguration_year else None
            state = int(state)
            category = int(category)
        except ValueError:
            return "Latitud, longitud, año, estado y categoría deben ser números válidos."

        return {
            "name": nombre,
            "short_description": short_description,
            "full_description": full_description,
            "city": city,
            "state": state,
            "latitude": latitude,
            "longitude": longitude,
            "conservation_state": conservation_state,
            "inauguration_year": inauguration_year,
            "category": category,
            "is_visible": is_visible
        }
    except Exception as e:
        return f"Error en el formulario: {str(e)}"
