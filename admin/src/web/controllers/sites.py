"""Controlador de gestión de sitios para el panel administrativo."""

import csv
import io
from datetime import datetime
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    Response,
    session,
    current_app,
)
from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.site_history import SiteHistory
from src.core.entity.site_image import SiteImage
from src.core.services.board.busqueda_avanzada_serv import (
    buscar_sites,
    obtener_provincias_con_sitios,
    ordenar_lista,
    paginar_lista,
)
from src.core.services.board.tag_serv import obtener_todas_las_tags
from src.core.services.board import site_history_serv as SiteHistoryService
from src.web.handlers.utils import permissions_required

from src.core.services.board.site_history_serv import obtener_historial_sitios

from src.core.services.board.sites import(obtener_todos_las_provincias, obtener_todas_las_categorias,
obtener_sitio_id,actualizar_sitio,eliminar_sitio,crear_sitio,obtener_nuevas_etiquetas)




bp = Blueprint("sites", __name__, url_prefix="/sitios")


# USUARIO_ES_ADMIN = True  //esto era para pruebas


# =====================================================
# LISTAR SITIOS CON FILTROS Y PAGINACIÓN
# =====================================================


def parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


@bp.get("/")
@permissions_required("site",["view"])
def index():
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
        flash(
            "El rango de fechas es inválido: 'Desde' no puede ser mayor que 'Hasta'.",
            "error",
        )

    results = buscar_sites(
        {
            "ciudad": ciudad,
            "provincia": provincia,
            "estado": estado,
            "visibilidad": visibilidad,
            "busqueda_texto": busqueda_texto,
            "tags": tags,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
        }
    )

    # Ordenar la lista en Python
    results = ordenar_lista(results, sort, order)

    # Paginación
    page_items, total_pages, total_results = paginar_lista(results, page, per_page)
    total_pages = max(1, total_pages)

    # --- LÓGICA PARA BUSCAR PORTADAS ---

    # Obtenemos config de MinIO
    base_url = current_app.config["MINIO_SERVER"]
    bucket_name = current_app.config["MINIO_BUCKET"]

    for item in page_items:
        # Buscamos la portada para este item['id']
        portada = (
            db.session.query(SiteImage.image_path)
            .filter_by(site_id=item["id"], is_thumbnail=True)
            .first()
        )

        if portada and portada.image_path:
            # Construimos la URL completa
            item["portada_url"] = (
                f"http://{base_url}/{bucket_name}/{portada.image_path}"
            )
        else:
            item["portada_url"] = None  # Para mostrar "Sin imagen"

    all_tags = obtener_todas_las_tags()
    provincias = obtener_provincias_con_sitios()

    # 1. Obtenemos el rol REAL de la sesión
    user_role = session.get("role", 0)  # 0 significa "invitado" si no está logueado

    # 2. Determinamos si es admin (rol 1)
    usuario_es_admin = user_role == 1

    return render_template(
        "sites/index.html",
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
        request=request,
        usuario_es_admin=usuario_es_admin,
        user_role=user_role,
    )


# =====================================================
# CREAR NUEVO SITIO
# =====================================================
@bp.get("/nuevo")
@permissions_required("site",["create"])
def nuevo():
    """Muestra el formulario para crear un nuevo sitio."""
    states = obtener_todos_las_provincias()
    categorys = obtener_todas_las_categorias()
    tags = obtener_todas_las_tags()
    return render_template(
        "sites/form.html",
        estados=states,
        categorias=categorys,
        etiquetas=tags,
    )


@bp.post("/crear")
@permissions_required("site",["create"])
def crear():
    """Crea un nuevo sitio histórico."""
    user_id = int(request.form.get("user_id", 1))
    data = _extraer_y_validar_form()

    if isinstance(data, str):
        flash(data, "error")
        return redirect(url_for("sites.nuevo"))


    tags_ids = request.form.getlist("tags")

    try:
        nuevo_sitio=crear_sitio(data,tags_ids,user_id)
        action_detail = (
            f"Sitio '{nuevo_sitio.name}' creado (estaba en {nuevo_sitio.city})"
        )
        SiteHistoryService.register_modify(
            nuevo_sitio,
            user_id,
            "CREATE",
            action_detail,
        )

        flash("Sitio creado correctamente.", "success")
        return redirect(url_for("sites.index"))

    except Exception as e:
        flash(f"Error al crear el sitio: {str(e)}", "error")
        return redirect(url_for("sites.nuevo"))


# =====================================================
# EDITAR SITIO
# =====================================================
@bp.get("/<int:site_id>/editar")
@permissions_required("site",["edit"])
def editar(site_id):
    """Muestra el formulario para editar un sitio existente."""
    site = obtener_sitio_id(site_id)
    if not site:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("sites.index"))
    states = obtener_todos_las_provincias()
    categorys = obtener_todas_las_categorias()
    tags = obtener_todas_las_tags()
    return render_template(
        "sites/form.html",
        sitio=site,
        estados=states,
        categorias=categorys,
        etiquetas=tags,
    )


@bp.post("/<int:site_id>/editar")
@permissions_required("site",["edit"])
def actualizar(site_id):
    """Actualiza los datos de un sitio existente y registra los cambios detectados."""
    sitio = obtener_sitio_id(site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("sites.index"))

    # Extraer y validar datos del formulario
    data = _extraer_y_validar_form()

    if isinstance(data, str):
        flash(data, "error")
        return redirect(url_for("sites.editar", site_id))

    # Recuperar etiquetas seleccionadas del formulario
    tags_ids = request.form.getlist("tags")
    nuevas_etiquetas = obtener_nuevas_etiquetas(tags_ids)

    user_id = int(request.form.get("user_id", 1))

    try:
        # ✅ Primero: detectar los cambios (comparar el estado actual con los nuevos valores)
        cambios_detectados = SiteHistoryService.detect_changes(
            sitio,
            data,
            nuevas_etiquetas,
        )

        # ✅ Si hay cambios, registrar en el historial ANTES del commit
        if cambios_detectados:
            detalle = "\n".join(cambios_detectados)
            action_detail = f"Cambios:\n{detalle}"
            SiteHistoryService.register_modify(
                sitio,
                user_id,
                "UPDATE",
                action_detail,
            )

        # ✅ Luego aplicar los cambios al objeto `sitio`
        actualizar_sitio(sitio,data,nuevas_etiquetas)

        if cambios_detectados:
            flash(
                f"Sitio actualizado correctamente. {len(cambios_detectados)} cambio(s) registrado(s).",
                "success",
            )
        else:
            flash("Sitio guardado sin cambios detectados.", "info")

        return redirect(url_for("sites.index"))

    except Exception as e:
        flash(f"Error al actualizar el sitio: {str(e)}", "error")
        return redirect(url_for("sites.editar", site_id))


# =====================================================
# ELIMINAR SITIO
# =====================================================
@bp.post("/<int:site_id>/eliminar")
@permissions_required("site",["delete"])
def eliminar(site_id):
    """Elimina un sitio histórico."""
    user_id = int(request.form.get("user_id", 1))
    sitio = obtener_sitio_id(site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("sites.index"))

    try:

        eliminar_sitio(sitio)
        action_detail = f"Sitio '{sitio.name}' eliminado."
        SiteHistoryService.register_modify(sitio, user_id, "DELETE", action_detail)
        flash("Sitio eliminado correctamente", "success")

    except Exception as e:
        flash(f"Error al eliminar el sitio: {str(e)}", "error")

    return redirect(url_for("sites.index"))


# =====================================================
# HISTORIAL DE CAMBIOS DE SITIO
# =====================================================
@bp.get("/<int:site_id>/historial")
@permissions_required("site_history", ["view"])
def historial(site_id):
    """Muestra el historial de cambios de un sitio."""
    sitio = db.session.get(Site, site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("sites.index"))

    cambios = obtener_historial_sitios(site_id)

    # Aquí está el cambio clave:
    return render_template(
        "sites/_historial_partial.html", sitio=sitio, cambios=cambios
    )


# =====================================================
# EXPORTAR CSV (TODOS LOS CAMPOS)
# =====================================================
@bp.get("/exportar")
def exportar():
    """Exporta todos los sitios a un archivo CSV."""
    sitios = db.session.query(Site).all()
    output = io.StringIO()
    output.write("\ufeff")  # BOM para Excel
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
        headers={"Content-Disposition": "attachment; filename=sitios_historicos.csv"},
    )


# =====================================================
# FUNCIÓN AUXILIAR DE VALIDACIÓN
# =====================================================
def _extraer_y_validar_form():
    """Extrae y valida los datos del formulario de sitio."""
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
        if not nombre or not city or not state or not category or not latitude or not longitude:
            return "Nombre, ciudad, estado, latitud, longitud y categoría son obligatorios."

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
            return (
                "Latitud, longitud, año, estado y categoría deben ser números válidos."
            )

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
            "is_visible": is_visible,
        }
    except Exception as e:
        return f"Error en el formulario: {str(e)}"
