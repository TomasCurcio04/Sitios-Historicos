"""Controlador de página de mantenimiento administrativo."""

from flask import (
    render_template,
    Blueprint,
    abort,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
import uuid
from sqlalchemy.orm import joinedload

# --- Importaciones ---
# Usamos el nuevo decorador de permisos
from src.web.handlers.auth import login_required, permission_required
from src.web.storage import storage
from src.core.database import db
from src.core.entity.site import Site
from src.core.entity.site_image import SiteImage


mantenimiento_admin_bp = Blueprint(
    "mantenimiento_admin", __name__, url_prefix="/mantenimiento_admin"
)


@mantenimiento_admin_bp.route("/", methods=["GET"])
def mantenimiento_admin():
    """Muestra la página de mantenimiento administrativo si la feature flag está activada.

    Returns:
        Response: Plantilla renderizada de mantenimiento o abort(404) si la flag no existe o está desactivada.
    """
    from src.core.services.auth.feature_flag_serv import get_feature_flag

    flag = get_feature_flag("admin_maintenance_mode")
    if not flag or not flag.enabled:
        abort(404)
    message = flag.maintenance_message if flag else None
    return render_template("mantenimiento_admin.html", message=message)


# --- RUTA UPLOAD ---
@mantenimiento_admin_bp.route("/upload-image", methods=["GET", "POST"])
@login_required
@permission_required("site_edit")  # <-- Permiso corregido
def upload_image():
    """Muestra el formulario de upload (GET) y procesa la subida de imágenes (POST).

    GET:
        - Carga sitios e imágenes y renderiza el formulario.
    POST:
        - Valida archivo, tamaño, formato y límite por sitio.
        - Sube el archivo a MinIO y crea un registro SiteImage en la BD.

    Returns:
        Response: Renderizado del template o redirección según resultado y validaciones.
    """

    # --- GET ---
    if request.method == "GET":
        try:
            # Cargamos sitios e imágenes
            sites = (
                db.session.query(Site)
                .options(joinedload(Site.images))
                .order_by(Site.name)
                .all()
            )

            base_url = current_app.config["MINIO_SERVER"]
            bucket_name = current_app.config["MINIO_BUCKET"]

        except Exception as e:
            flash(f"Error al cargar los sitios: {e}", "danger")
            sites = []
            base_url = ""
            bucket_name = ""

        return render_template(
            "mantenimiento_upload.html",
            sites=sites,
            minio_base_url=base_url,
            minio_bucket=bucket_name,
        )

    # --- POST ---
    try:
        file = request.files.get("imagen")
        form_sitio_id = request.form.get("sitio_id")
        form_titulo = request.form.get("titulo")
        form_descripcion = request.form.get("descripcion")
        form_orden = int(request.form.get("orden", 0))
        form_es_portada = "es_portada" in request.form

        # --- VALIDACIONES ---

        # 1. Básicas
        if not file or file.filename == "":
            flash("Error: No se seleccionó ningún archivo.", "danger")
            return redirect(request.url)

        if not form_sitio_id:
            flash("Error: Debe seleccionar un sitio histórico.", "danger")
            return redirect(request.url)

        # 2. Límite de 10 imágenes (Usa site_id)
        image_count = (
            db.session.query(SiteImage).filter_by(site_id=form_sitio_id).count()
        )
        if image_count >= 10:
            flash(
                f"Error: El sitio ya tiene {image_count} imágenes (límite de 10).",
                "danger",
            )
            return redirect(request.url)

        # 3. Formato (JPG, PNG, WEBP)
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
        extension = file.filename.rsplit(".", 1)[-1].lower()
        if "." not in file.filename or extension not in ALLOWED_EXTENSIONS:
            flash(
                "Error: Formato no permitido. Solo se aceptan: JPG, PNG, WEBP.",
                "danger",
            )
            return redirect(request.url)

        # 4. Tamaño (Máx 5MB)
        file_data = file.read()
        file_size = len(file_data)
        MAX_FILE_SIZE = 5 * 1024 * 1024

        if file_size > MAX_FILE_SIZE:
            flash("Error: El archivo es demasiado grande (Máximo 5 MB).", "danger")
            return redirect(request.url)

        file.seek(0)  # Rebobinar tras leer el tamaño

        # --- LÓGICA DE NEGOCIO ---

        # 1. Portada Única
        if form_es_portada:
            portada_actual = (
                db.session.query(SiteImage)
                .filter_by(site_id=form_sitio_id, is_thumbnail=True)
                .first()
            )
            if portada_actual:
                portada_actual.is_thumbnail = False
                db.session.add(portada_actual)

        # 2. Subir a MinIO
        object_name = f"public/sites/{form_sitio_id}/{uuid.uuid4()}.{extension}"
        bucket_name = current_app.config["MINIO_BUCKET"]

        current_app.storage.put_object(
            bucket_name,
            object_name,
            data=file,
            length=file_size,
            content_type=file.content_type,
        )

        # 3. Guardar en BD (Usa nombres correctos: site_id, image_path)
        nueva_imagen = SiteImage(
            site_id=form_sitio_id,
            image_path=object_name,
            title=form_titulo,
            description=form_descripcion,
            display_order=form_orden,
            is_thumbnail=form_es_portada,
        )

        db.session.add(nueva_imagen)
        db.session.commit()

        flash("¡Imagen subida y registrada con éxito!", "success")
        return redirect(url_for("mantenimiento_admin.upload_image"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error grave al subir la imagen: {str(e)}", "danger")
        return redirect(request.url)


# --- DELETE IMAGE ---
@mantenimiento_admin_bp.route("/delete-image/<int:image_id>", methods=["POST"])
@login_required
@permission_required("site_edit")
def delete_image(image_id):
    """Elimina una imagen asociada a un sitio y la remueve de MinIO.

    Args:
        image_id (int): ID de la imagen a eliminar.

    Returns:
        Response: Redirección a la página de upload con mensaje de resultado.
    """
    try:
        image = db.session.get(SiteImage, image_id)

        if not image:
            flash("Imagen no encontrada.", "danger")
            return redirect(url_for("mantenimiento_admin.upload_image"))

        if image.is_thumbnail:
            flash(
                "Error: No se puede eliminar una imagen marcada como portada.", "danger"
            )
            return redirect(url_for("mantenimiento_admin.upload_image"))

        # Borrar de MinIO (Usa image_path y remove_object)
        bucket_name = current_app.config["MINIO_BUCKET"]
        current_app.storage.remove_object(bucket_name, image.image_path)

        db.session.delete(image)
        db.session.commit()

        flash("Imagen eliminada correctamente.", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar la imagen: {str(e)}", "danger")

    return redirect(url_for("mantenimiento_admin.upload_image"))


# --- MAKE COVER ---
@mantenimiento_admin_bp.route("/make-cover/<int:image_id>", methods=["POST"])
@login_required
@permission_required("site_edit")
def make_cover(image_id):
    """Marca una imagen como portada (thumbnail) para su sitio, desmarcando la existente.

    Args:
        image_id (int): ID de la imagen que será portada.

    Returns:
        Response: Redirección a la página de upload con mensaje de resultado.
    """
    try:
        image_to_make_cover = db.session.get(SiteImage, image_id)

        if not image_to_make_cover:
            flash("Imagen no encontrada.", "danger")
            return redirect(url_for("mantenimiento_admin.upload_image"))

        if image_to_make_cover.is_thumbnail:
            flash("Esa imagen ya es la portada.", "info")
            return redirect(url_for("mantenimiento_admin.upload_image"))

        # Buscar portada actual del sitio
        portada_actual = (
            db.session.query(SiteImage)
            .filter_by(site_id=image_to_make_cover.site_id, is_thumbnail=True)
            .first()
        )

        if portada_actual:
            portada_actual.is_thumbnail = False
            db.session.add(portada_actual)

        image_to_make_cover.is_thumbnail = True
        db.session.add(image_to_make_cover)

        db.session.commit()

        flash("Nueva imagen de portada establecida con éxito.", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al cambiar la portada: {str(e)}", "danger")

    return redirect(url_for("mantenimiento_admin.upload_image"))
