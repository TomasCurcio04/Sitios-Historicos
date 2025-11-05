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

# --- Importaciones de tu proyecto (Corregidas) ---

# Importa TUS decoradores
from src.web.handlers.auth import login_required, admin_required 

# Importa el cliente de MinIO (storage)
from src.web.storage import storage 

# Importa la sesión de BD
from src.core.database import db 

# --- ¡AQUÍ ESTÁ LA CORRECCIÓN IMPORTANTE! ---
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


# --- NUEVA RUTA PARA SUBIR IMÁGENES (Actualizada) ---
@mantenimiento_admin_bp.route('/upload-image', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_image():
    
    # --- LÓGICA GET ---
    if request.method == 'GET':
        try:
            # Asumo que tu modelo Site tiene 'nombre'
            sites = db.session.query(Site).order_by(Site.name).all()
        except Exception as e:
            flash(f'Error al cargar los sitios: {e}', 'danger')
            sites = []
            
        return render_template('mantenimiento_upload.html', sites=sites)

    # --- LÓGICA POST ---
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
        # Si el usuario marcó 'es_portada' en el formulario...
        if form_es_portada:
            # 1. Buscamos la portada actual (si existe) para ese sitio
            portada_actual = db.session.query(SiteImage).filter_by(
                id_site=form_sitio_id, 
                is_thumbnail=True
            ).first()
            
            # 2. Si existe, le quitamos la marca de portada
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
        # Asumo que tienes MINIO_BUCKET en tu config de Flask
        bucket_name = current_app.config['MINIO_BUCKET']
        
        # --- ¡ESTA ES LA LÍNEA CORREGIDA! ---
        # Usamos el cliente MinIO adjuntado a la app (app.storage)
        current_app.storage.put_object(
            bucket_name,
            object_name,
            data=file, # Pasamos el objeto 'file' directamente
            length=file_size,
            content_type=file.content_type
        )
        
        # 5. ¡AQUÍ MAPEAMOS LOS DATOS A TU MODELO 'SiteImage'!
        
        # Tu modelo 'SiteImage' guarda solo el 'file_path' (el object_name)
        # y no la URL completa, lo cual es una mejor práctica.
        
        nueva_imagen = SiteImage(
            id_site=form_sitio_id,         # Form 'sitio_id' -> Model 'id_site'
            file_path=object_name,         # Guardamos el path de MinIO
            title=form_titulo,             # Form 'titulo' -> Model 'title'
            description=form_descripcion,  # Form 'descripcion' -> Model 'description'
            display_order=form_orden,      # Form 'orden' -> Model 'display_order'
            is_thumbnail=form_es_portada   # Form 'es_portada' -> Model 'is_thumbnail'
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