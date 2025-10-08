from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from src.core import board
import csv
import io

# =====================================================
# CONTROLADOR: GESTIÓN DE SITIOS HISTÓRICOS CON ETIQUETAS
# -----------------------------------------------------
# - CRUD completo (crear, leer, actualizar, eliminar)
# - Paginación (máx. 25 registros por página)
# - Restricción de eliminación a administradores
# - Filtros de búsqueda
# - Exportación CSV
# - Gestión de etiquetas (múltiples etiquetas por sitio)
# =====================================================

# ---------------------------
# Configuración del Blueprint
# ---------------------------
bp = Blueprint("issues", __name__, url_prefix="/sitios")
PER_PAGE = 25  # Cantidad de sitios por página

# ---------------------------
# Simulación de usuario (admin)
# ---------------------------
# ⚠️ Cambiar a False para simular usuario no admin
USUARIO_ES_ADMIN = True

# ---------------------------
# LISTADO DE SITIOS CON PAGINACIÓN Y BÚSQUEDA
# ---------------------------
@bp.get("/")
def index():
    """
    Renderiza el listado de sitios históricos con paginación y filtros opcionales:
    - nombre, ciudad, provincia, categoría, estado de conservación, año, visible
    - muestra también las etiquetas asociadas a cada sitio
    """
    page = int(request.args.get("page", 1))

    # Extraer filtros
    filtros = {
        "nombre": request.args.get("nombre", "").strip().lower(),
        "ciudad": request.args.get("ciudad", "").strip().lower(),
        "provincia": request.args.get("provincia", "").strip().lower(),
        "categoria": request.args.get("categoria", "").strip().lower(),
        "estado": request.args.get("estado", "").strip().lower(),
        "anio": request.args.get("anio", "").strip(),
        "visible": request.args.get("visible", "").strip()
    }

    # Obtener todos los sitios
    sitios = board.get_all_sites_json()

    # Aplicar filtros
    if filtros["nombre"]:
        sitios = [s for s in sitios if filtros["nombre"] in s.get('nombre', '').lower()]
    if filtros["ciudad"]:
        sitios = [s for s in sitios if filtros["ciudad"] in s.get('ciudad', '').lower()]
    if filtros["provincia"]:
        sitios = [s for s in sitios if filtros["provincia"] in s.get('provincia', '').lower()]
    if filtros["categoria"]:
        sitios = [s for s in sitios if filtros["categoria"] in s.get('categoria', '').lower()]
    if filtros["estado"]:
        sitios = [s for s in sitios if filtros["estado"] in s.get('estado_conservacion', '').lower()]
    if filtros["anio"]:
        try:
            anio_int = int(filtros["anio"])
            sitios = [s for s in sitios if s.get('anio_inauguracion') == anio_int]
        except ValueError:
            pass
    if filtros["visible"]:
        if filtros["visible"] == "1":
            sitios = [s for s in sitios if s.get('visible')]
        elif filtros["visible"] == "0":
            sitios = [s for s in sitios if not s.get('visible')]

    # Paginación
    total_sites = len(sitios)
    total_pages = (total_sites // PER_PAGE) + (1 if total_sites % PER_PAGE else 0)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    sitios_page = sitios[start:end]

    return render_template(
        "sites/index.html",
        sitios=sitios_page,
        page=page,
        total_pages=total_pages,
        usuario_es_admin=USUARIO_ES_ADMIN
    )

# ---------------------------
# FORMULARIO PARA CREAR NUEVO SITIO
# ---------------------------
@bp.get("/nuevo")
def nuevo():
    """Renderiza el formulario vacío para crear un sitio histórico con posibilidad de agregar etiquetas."""
    return render_template("sites/form.html", sitio=None)

# ---------------------------
# CREAR SITIO NUEVO CON VALIDACIONES
# ---------------------------
@bp.post("/nuevo")
def crear():
    """Procesa el formulario de creación de sitio histórico, incluyendo etiquetas."""
    data = _extraer_y_validar_form()
    if isinstance(data, str):
        flash(data, "error")
        return redirect(url_for("issues.nuevo"))

    board.create_site_json(data)
    flash("Sitio creado correctamente", "success")
    return redirect(url_for("issues.index"))

# ---------------------------
# FORMULARIO PARA EDITAR UN SITIO
# ---------------------------
@bp.get("/<int:site_id>/editar")
def editar(site_id):
    """Renderiza el formulario de edición con los datos del sitio, incluyendo etiquetas."""
    sitio = board.get_site_json(site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("issues.index"))

    return render_template("sites/form.html", sitio=sitio)

# ---------------------------
# GUARDAR CAMBIOS DE EDICIÓN
# ---------------------------
@bp.post("/<int:site_id>/editar")
def actualizar(site_id):
    """Procesa el formulario de edición y actualiza los datos del sitio, incluyendo etiquetas."""
    updated_data = _extraer_y_validar_form()
    if isinstance(updated_data, str):
        flash(updated_data, "error")
        return redirect(url_for("issues.editar", site_id=site_id))

    board.update_site_json(site_id, updated_data)
    flash("Sitio actualizado correctamente", "success")
    return redirect(url_for("issues.index"))

# ---------------------------
# ELIMINAR UN SITIO
# ---------------------------
@bp.post("/<int:site_id>/eliminar")
def eliminar(site_id):
    """Elimina un sitio histórico (solo admin)."""
    if not USUARIO_ES_ADMIN:
        flash("No tenés permisos para eliminar este sitio.", "error")
        return redirect(url_for("issues.index"))

    sitio = board.get_site_json(site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("issues.index"))

    board.delete_site_json(site_id)
    flash("Sitio eliminado correctamente", "success")
    return redirect(url_for("issues.index"))

# ---------------------------
# EXPORTAR CSV (original)
# ---------------------------
@bp.get("/exportar")
def exportar():
    """
    Exporta los sitios históricos filtrados a CSV.
    - Respeta filtros activos.
    - UTF-8 con BOM para Excel.
    - Todo en memoria, sin archivos temporales.
    - Incluye etiquetas en la exportación
    """
    filtros = {
        "nombre": request.args.get("nombre", "").strip().lower(),
        "ciudad": request.args.get("ciudad", "").strip().lower(),
        "provincia": request.args.get("provincia", "").strip().lower(),
        "categoria": request.args.get("categoria", "").strip().lower(),
        "estado": request.args.get("estado", "").strip().lower(),
        "anio": request.args.get("anio", "").strip(),
        "visible": request.args.get("visible", "").strip()
    }

    sitios = board.get_all_sites_json()

    # Aplicar filtros
    if filtros["nombre"]:
        sitios = [s for s in sitios if filtros["nombre"] in s.get('nombre', '').lower()]
    if filtros["ciudad"]:
        sitios = [s for s in sitios if filtros["ciudad"] in s.get('ciudad', '').lower()]
    if filtros["provincia"]:
        sitios = [s for s in sitios if filtros["provincia"] in s.get('provincia', '').lower()]
    if filtros["categoria"]:
        sitios = [s for s in sitios if filtros["categoria"] in s.get('categoria', '').lower()]
    if filtros["estado"]:
        sitios = [s for s in sitios if filtros["estado"] in s.get('estado_conservacion', '').lower()]
    if filtros["anio"]:
        try:
            anio_int = int(filtros["anio"])
            sitios = [s for s in sitios if s.get('anio_inauguracion') == anio_int]
        except ValueError:
            pass
    if filtros["visible"]:
        if filtros["visible"] == "1":
            sitios = [s for s in sitios if s.get('visible')]
        elif filtros["visible"] == "0":
            sitios = [s for s in sitios if not s.get('visible')]

    # Generar CSV
    output = io.StringIO()
    output.write('\ufeff')  # BOM para Excel
    campos = [
        "ID", "Nombre", "Ciudad", "Provincia", "Estado", "Año", "Visible",
        "Categoría", "Latitud", "Longitud", "Descripción Breve", "Descripción Completa", "Etiquetas"
    ]
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(campos)

    for s in sitios:
        etiquetas_str = ", ".join(s.get('etiquetas', []))
        writer.writerow([
            s.get('id', ''),
            s.get('nombre', ''),
            s.get('ciudad', ''),
            s.get('provincia', ''),
            s.get('estado_conservacion', ''),
            s.get('anio_inauguracion', ''),
            "Sí" if s.get('visible') else "No",
            s.get('categoria', ''),
            s.get('latitud', ''),
            s.get('longitud', ''),
            s.get('descripcion_breve', ''),
            s.get('descripcion_completa', ''),
            etiquetas_str
        ])

    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=sitios_historicos.csv'}
    )

# ---------------------------
# FUNCIÓN AUXILIAR: EXTRAER Y VALIDAR FORMULARIO
# ---------------------------
def _extraer_y_validar_form():
    """
    Extrae y valida los datos del formulario de creación/edición, incluyendo etiquetas.
    Asegura que latitud, longitud y año sean numéricos y que las etiquetas
    se manejen correctamente como lista de strings.
    """
    try:
        nombre = request.form.get("nombre", "").strip()
        ciudad = request.form.get("ciudad", "").strip()
        provincia = request.form.get("provincia", "").strip()
        latitud = float(request.form.get("latitud", 0))
        longitud = float(request.form.get("longitud", 0))
        anio_inauguracion = int(request.form.get("anio_inauguracion", 0))

        if not nombre or not ciudad or not provincia:
            return "Nombre, ciudad y provincia son obligatorios."

        # Extraer etiquetas como lista (separadas por coma)
        etiquetas_raw = request.form.get("etiquetas", "").strip()
        etiquetas = [e.strip() for e in etiquetas_raw.split(",") if e.strip()]

        return {
            "nombre": nombre,
            "descripcion_breve": request.form.get("descripcion_breve", "").strip(),
            "descripcion_completa": request.form.get("descripcion_completa", "").strip(),
            "ciudad": ciudad,
            "provincia": provincia,
            "latitud": latitud,
            "longitud": longitud,
            "estado_conservacion": request.form.get("estado_conservacion", "").strip(),
            "anio_inauguracion": anio_inauguracion,
            "categoria": request.form.get("categoria", "").strip(),
            "visible": request.form.get("visible") == "on",
            "etiquetas": etiquetas  # ✅ etiquetas incluidas
        }
    except ValueError:
        return "Latitud, longitud y año de inauguración deben ser números válidos."