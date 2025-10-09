from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from sqlalchemy import or_
from src.core.database import db
from src.core.board.site import Site
from src.core.board.tag import Tag
import csv
import io

bp = Blueprint("issues", __name__, url_prefix="/sitios")
PER_PAGE = 25

# ⚙️ Simulación de usuario administrador (cambiar a False si querés probar sin permisos)
USUARIO_ES_ADMIN = True


# =====================================================
# LISTAR SITIOS CON FILTROS Y PAGINACIÓN
# =====================================================
@bp.get("/")
def index():
    page = int(request.args.get("page", 1))
    per_page = PER_PAGE

    # Filtros
    filtros = {
        "nombre": request.args.get("nombre", "").strip().lower(),
        "ciudad": request.args.get("ciudad", "").strip().lower(),
        "provincia": request.args.get("provincia", "").strip().lower(),
        "categoria": request.args.get("categoria", "").strip().lower(),
        "estado": request.args.get("estado", "").strip().lower(),
        "anio": request.args.get("anio", "").strip(),
        "visible": request.args.get("visible", "").strip()
    }

    query = db.session.query(Site)

    if filtros["nombre"]:
        query = query.filter(Site.name.ilike(f"%{filtros['nombre']}%"))
    if filtros["ciudad"]:
        query = query.filter(Site.city.ilike(f"%{filtros['ciudad']}%"))
    if filtros["provincia"]:
        query = query.filter(Site.province.ilike(f"%{filtros['provincia']}%"))
    if filtros["categoria"]:
        query = query.filter(Site.category.ilike(f"%{filtros['categoria']}%"))
    if filtros["estado"]:
        query = query.filter(Site.conservation_state.ilike(f"%{filtros['estado']}%"))
    if filtros["anio"].isdigit():
        query = query.filter(Site.year_inaugurated == int(filtros["anio"]))
    if filtros["visible"]:
        if filtros["visible"] == "1":
            query = query.filter(Site.is_visible.is_(True))
        elif filtros["visible"] == "0":
            query = query.filter(Site.is_visible.is_(False))

    total_sites = query.count()
    total_pages = (total_sites + per_page - 1) // per_page
    sitios = query.offset((page - 1) * per_page).limit(per_page).all()

    return render_template(
        "sites/index.html",
        sitios=sitios,
        page=page,
        total_pages=total_pages,
        usuario_es_admin=USUARIO_ES_ADMIN
    )


# =====================================================
# CREAR NUEVO SITIO
# =====================================================
@bp.get("/nuevo")
def nuevo():
    return render_template("sites/form.html", sitio=None)


@bp.post("/nuevo")
def crear():
    data = _extraer_y_validar_form()
    if isinstance(data, str):
        flash(data, "error")
        return redirect(url_for("issues.nuevo"))

    nuevo_sitio = Site(**data)
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
    return render_template("sites/form.html", sitio=sitio)


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
# EXPORTAR CSV
# =====================================================
@bp.get("/exportar")
def exportar():
    query = db.session.query(Site).all()

    output = io.StringIO()
    output.write('\ufeff')  # BOM para Excel
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    campos = [
        "ID", "Nombre", "Ciudad", "Provincia", "Estado", "Año", "Visible",
        "Categoría", "Latitud", "Longitud", "Descripción Breve",
        "Descripción Completa"
    ]
    writer.writerow(campos)

    for s in query:
        writer.writerow([
            s.id, s.name, s.city, s.province,
            s.conservation_state, s.year_inaugurated,
            "Sí" if s.is_visible else "No",
            s.category, s.latitude, s.longitude,
            s.short_description, s.full_description
        ])

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
        ciudad = request.form.get("ciudad", "").strip()
        provincia = request.form.get("provincia", "").strip()
        latitud = float(request.form.get("latitud", 0))
        longitud = float(request.form.get("longitud", 0))
        anio_inauguracion = int(request.form.get("anio_inauguracion", 0))

        if not nombre or not ciudad or not provincia:
            return "Nombre, ciudad y provincia son obligatorios."

        return {
            "name": nombre,
            "short_description": request.form.get("descripcion_breve", "").strip(),
            "full_description": request.form.get("descripcion_completa", "").strip(),
            "city": ciudad,
            "province": provincia,
            "latitude": latitud,
            "longitude": longitud,
            "conservation_state": request.form.get("estado_conservacion", "").strip(),
            "year_inaugurated": anio_inauguracion,
            "category": request.form.get("categoria", "").strip(),
            "is_visible": request.form.get("visible") == "on"
        }
    except ValueError:
        return "Latitud, longitud y año deben ser números válidos."
