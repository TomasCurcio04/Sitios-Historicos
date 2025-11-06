# pylint: disable=import-error
"""Controlador de página de mantenimiento administrativo."""

from flask import (
    render_template, 
    Blueprint, 
    abort, 
    request, 
    redirect, 
    url_for, 
    flash, 
    current_app
)
import uuid # Para nombres de archivo únicos
from sqlalchemy.orm import joinedload 

# --- Importaciones de tu proyecto (Corregidas) ---

# Importa TUS decoradores
from src.web.handlers.auth import login_required, admin_required 

# Importa el cliente de MinIO (storage)
from src.web.storage import storage 

# Importa la sesión de BD
from src.core.database import db 

# Importamos los modelos desde sus archivos correctos
from src.core.entity.site import Site
from src.core.entity.site_image import SiteImage


# --- Blueprint (Tu código original) ---
mantenimiento_admin_bp = Blueprint(
    "mantenimiento_admin", __name__, url_prefix="/mantenimiento_admin"
)


# --- Ruta de Mantenimiento (Tu código original) ---
@mantenimiento_admin_bp.route("/", methods=["GET"])
def mantenimiento_admin():
    """Muestra la página de mantenimiento cuando está activo el modo mantenimiento."""
    from src.core.services.auth.feature_flag_serv import get_feature_flag
    
    flag = get_feature_flag("admin_maintenance_mode")
    if not flag or not flag.enabled:
        abort(404)
    message = flag.maintenance_message if flag else None
    return render_template("mantenimiento_admin.html", message=message)


# --- RUTA PARA SUBIR Y LISTAR IMÁGENES (Actualizada) ---
@mantenimiento_admin_bp.route('/upload-image', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_image():
    
    # --- LÓGICA GET (Actualizada) ---
    if request.method == 'GET':
        try:
            # Obtenemos sitios Y sus imágenes (eager loading)
            sites = db.session.query(Site).options(
                joinedload(Site.images)
            ).order_by(Site.name).all()
            
            # Pasamos config de MinIO para construir URLs
            base_url = current_app.config['MINIO_SERVER'] 
            bucket_name = current_app.config['MINIO_BUCKET']

        except Exception as e:
            flash(f'Error al cargar los sitios: {e}', 'danger')
            sites = []
            base_url = ""
            bucket_name = ""
            
        return render_template(
            'mantenimiento_upload.html', 
            sites=sites,
            minio_base_url=base_url,
            minio_bucket=bucket_name
        )

    # --- LÓGICA POST (Subir imagen) ---
    try:
        # 1. Obtener datos del formulario (esto no cambia)
        file = request.files.get('imagen')
        form_sitio_id = request.form.get('sitio_id') # Lo recibimos del form
        form_titulo = request.form.get('titulo')
        form_descripcion = request.form.get('descripcion')
        form_orden = int(request.form.get('orden', 0))
        form_es_portada = 'es_portada' in request.form 

        # 2. Validaciones (esto no cambia)
        if not file or file.filename == '':
            flash('Error: No se seleccionó ningún archivo.', 'danger')
            return redirect(request.url)
        
        if not form_sitio_id:
            flash('Error: Debe seleccionar un sitio histórico.', 'danger')
            return redirect(request.url)

        # --- ¡NUEVA LÓGICA DE PORTADA ÚNICA! ---
        if form_es_portada:
            portada_actual = db.session.query(SiteImage).filter_by(
                id_site=form_sitio_id, 
                is_thumbnail=True
            ).first()
            if portada_actual:
                portada_actual.is_thumbnail = False
                db.session.add(portada_actual)
        # --- FIN LÓGICA PORTADA ÚNICA ---

        # 3. Preparar el archivo para MinIO (esto no cambia)
        extension = file.filename.rsplit('.', 1)[-1].lower()
        object_name = f"public/sites/{form_sitio_id}/{uuid.uuid4()}.{extension}"
        
        file_data = file.read()
        file_size = len(file_data)
        file.seek(0) 
        
       # 4. Subir a MinIO
        bucket_name = current_app.config['MINIO_BUCKET']
        
        current_app.storage.put_object(
            bucket_name,
            object_name,
            data=file,
            length=file_size,
            content_type=file.content_type
        )
        
        # 5. Mapear datos al modelo
        nueva_imagen = SiteImage(
            id_site=form_sitio_id,
            file_path=object_name,
            title=form_titulo,
            description=form_descripcion,
            display_order=form_orden,
            is_thumbnail=form_es_portada
        )
        
        # 6. Guardar en la Base de Datos
        db.session.add(nueva_imagen)
        db.session.commit()

        flash('¡Imagen subida y registrada con éxito!', 'success')
        return redirect(url_for('mantenimiento_admin.upload_image'))

    except Exception as e:
        db.session.rollback() 
        flash(f'Error grave al subir la imagen: {str(e)}', 'danger')
        return redirect(request.url)


# --- RUTA PARA ELIMINAR IMÁGENES (Sin cambios) ---
@mantenimiento_admin_bp.route('/delete-image/<int:image_id>', methods=['POST'])
@login_required
@admin_required
def delete_image(image_id):
    
    try:
        # 1. Buscar la imagen en la BD
        image = db.session.get(SiteImage, image_id)
        
        if not image:
            flash('Imagen no encontrada.', 'danger')
            return redirect(url_for('mantenimiento_admin.upload_image'))
            
        # 2. Aplicar la restricción
        if image.is_thumbnail:
            flash('Error: No se puede eliminar una imagen marcada como portada.', 'danger')
            return redirect(url_for('mantenimiento_admin.upload_image'))
            
        # 3. Borrar de MinIO
        bucket_name = current_app.config['MINIO_BUCKET']
        current_app.storage.remove_object(bucket_name, image.file_path) 
        
        # 4. Borrar de la BD
        db.session.delete(image)
        db.session.commit()
        
        flash('Imagen eliminada correctamente.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la imagen: {str(e)}', 'danger')

    return redirect(url_for('mantenimiento_admin.upload_image'))


# --- ¡NUEVA RUTA PARA HACER PORTADA! ---
@mantenimiento_admin_bp.route('/make-cover/<int:image_id>', methods=['POST'])
@login_required
@admin_required
def make_cover(image_id):
    
    try:
        # 1. Buscar la imagen que queremos hacer portada
        image_to_make_cover = db.session.get(SiteImage, image_id)
        
        if not image_to_make_cover:
            flash('Imagen no encontrada.', 'danger')
            return redirect(url_for('mantenimiento_admin.upload_image'))
            
        # 2. Si ya es portada, no hacemos nada
        if image_to_make_cover.is_thumbnail:
            flash('Esa imagen ya es la portada.', 'info')
            return redirect(url_for('mantenimiento_admin.upload_image'))

        # 3. Buscar la portada actual de ESE sitio
        portada_actual = db.session.query(SiteImage).filter_by(
            id_site=image_to_make_cover.id_site, 
            is_thumbnail=True
        ).first()

        # 4. Desmarcar la portada vieja (si existe)
        if portada_actual:
            portada_actual.is_thumbnail = False
            db.session.add(portada_actual)
            
        # 5. Marcar la nueva portada
        image_to_make_cover.is_thumbnail = True
        db.session.add(image_to_make_cover)
        
        # 6. Guardar cambios
        db.session.commit()
        
        flash('Nueva imagen de portada establecida con éxito.', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar la portada: {str(e)}', 'danger')

    return redirect(url_for('mantenimiento_admin.upload_image'))