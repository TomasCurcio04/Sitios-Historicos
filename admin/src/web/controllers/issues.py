from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, session
from sqlalchemy import or_
from src.core.database import db
from src.core.board.site import Site
from src.core.board.site_history import SiteHistory
from src.core.board.site_history_serv import SiteHistoryService
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

@bp.post("/crear")
def crear():
    user_id = int(request.form.get("user_id", 1))
    data = _extraer_y_validar_form()
    if isinstance(data, str):
        flash(data, "error")
        return redirect(url_for("issues.nuevo"))

    nuevo_sitio = Site(**data, created_by=user_id)
    tags_ids = request.form.getlist("tags")
    nuevo_sitio.tag = db.session.query(Tag).filter(Tag.id_tag.in_(tags_ids)).all()
    
    try:
        db.session.add(nuevo_sitio)
        db.session.flush()  # Para obtener el ID del sitio antes del commit
        
        # ✅ Lógica delegada al servicio
        SiteHistoryService.register_creation(db.session, site=nuevo_sitio, user_id=user_id)
        
        db.session.commit()
        flash("Sitio creado correctamente.", "success")
        return redirect(url_for("issues.index"))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear el sitio: {str(e)}", "error")
        return redirect(url_for("issues.nuevo"))

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
    
    # --- La lógica de guardar estado anterior, validar y detectar cambios sigue aquí ---
    estado_anterior = { 'name': sitio.name, 'short_description': sitio.short_description, # ... etc.
    }
    data = _extraer_y_validar_form()
    # ... (código que aplica los datos al objeto 'sitio')
    cambios_detectados = []
    # ... (todos los 'if' que comparan y llenan la lista 'cambios_detectados')
    # ----------------------------------------------------------------------------
    
    try:
        if cambios_detectados:
            user_id = int(request.form.get("user_id", 1))
            
            # ✅ Lógica delegada al servicio
            SiteHistoryService.register_update(
                db_session=db.session,
                site_id=site_id,
                user_id=user_id,
                changes=cambios_detectados
            )
            flash(f"Sitio actualizado correctamente. {len(cambios_detectados)} cambio(s) registrado(s).", "success")
        else:
            flash("Sitio guardado sin cambios detectados.", "info")
            
        db.session.commit()
        return redirect(url_for("issues.index"))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar el sitio: {str(e)}", "error")
        return redirect(url_for("issues.editar", site_id=site_id))

# =====================================================
# ELIMINAR SITIO
# =====================================================
@bp.post("/<int:site_id>/eliminar")
def eliminar(site_id):
    user_id = int(request.form.get("user_id", 1))
    sitio = db.session.get(Site, site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("issues.index"))
    
    try:
        # ✅ Lógica delegada al servicio ANTES de eliminar el objeto
        SiteHistoryService.register_deletion(db.session, site=sitio, user_id=user_id)
        
        db.session.delete(sitio)
        db.session.commit()
        
        flash("Sitio eliminado correctamente", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar el sitio: {str(e)}", "error")

    return redirect(url_for("issues.index"))

# =====================================================
# HISTORIAL DE CAMBIOS DE SITIO
# =====================================================
@bp.get("/<int:site_id>/historial")
def historial(site_id):
    sitio = db.session.get(Site, site_id)
    if not sitio:
        # En el contexto de una llamada fetch, un redirect no es ideal.
        # Sería mejor devolver un error, pero por ahora esto funciona.
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("issues.index"))
    
    cambios = db.session.query(SiteHistory).filter_by(id_site=site_id).order_by(SiteHistory.date_action.desc()).all()
    
    # Aquí está el cambio clave:
    return render_template("sites/_historial_partial.html", sitio=sitio, cambios=cambios)
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
        fila = [getattr(sitio, campo.name, "") for campo in Site.__table__.columns]
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
