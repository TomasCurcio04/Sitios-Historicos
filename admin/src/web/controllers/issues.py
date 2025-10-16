from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, session
from sqlalchemy import or_
from src.core.database import db
from src.core.board.site import Site
from src.core.board.site_history import SiteHistory
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
    # Obtener el user_id del formulario
    user_id = int(request.form.get("user_id", 1))
    
    data = _extraer_y_validar_form()
    if isinstance(data, str):
        flash(data, "error")
        return redirect(url_for("issues.nuevo"))

    nuevo_sitio = Site(**data)
    nuevo_sitio.created_by = user_id  # ← Usar el user_id del form
    
    tags_ids = request.form.getlist("tags")
    etiquetas = db.session.query(Tag).filter(Tag.id_tag.in_(tags_ids)).all()
    nuevo_sitio.tag = etiquetas
    
    try:
        db.session.add(nuevo_sitio)
        db.session.flush()
        
        estado = db.session.get(State, nuevo_sitio.state)
        historial_creacion = SiteHistory(
            id_site=nuevo_sitio.id_site,
            id_user=user_id,  # ← Usar el user_id del form
            action_type="CREATE",
            action_detail=f"Sitio '{nuevo_sitio.name}' creado en {nuevo_sitio.city}, {estado.name if estado else 'N/A'}"
        )
        db.session.add(historial_creacion)
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
    print(f"\n{'='*60}")
    print(f"INICIANDO ACTUALIZACIÓN DE SITIO {site_id}")
    print(f"{'='*60}\n")
    
    sitio = db.session.get(Site, site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("issues.index"))
    
    print(f"✓ Sitio encontrado: {sitio.name}")
    print(f"  - ID: {sitio.id_site}")
    print(f"  - Visible antes: {sitio.is_visible}")

    # Guardar estado ANTES de modificar
    estado_anterior = {
        'name': sitio.name,
        'short_description': sitio.short_description,
        'full_description': sitio.full_description,
        'city': sitio.city,
        'state': sitio.state,
        'latitude': float(sitio.latitude) if sitio.latitude else None,
        'longitude': float(sitio.longitude) if sitio.longitude else None,
        'conservation_state': sitio.conservation_state,
        'inauguration_year': sitio.inauguration_year,
        'category': sitio.category,
        'is_visible': sitio.is_visible,
        'tags': set([tag.id_tag for tag in sitio.tag])
    }

    # Validar y aplicar cambios
    data = _extraer_y_validar_form()
    if isinstance(data, str):
        print(f"❌ ERROR EN VALIDACIÓN: {data}")
        flash(data, "error")
        return redirect(url_for("issues.editar", site_id=site_id))

    print(f"\n✓ Datos validados correctamente:")
    print(f"  Data recibida: {data}")
    
    for key, value in data.items():
        print(f"  - Actualizando {key}: {getattr(sitio, key, 'N/A')} → {value}")
        setattr(sitio, key, value)

    # Etiquetas
    tags_ids = request.form.getlist("tags")
    print(f"\n✓ Tags recibidos: {tags_ids}")
    etiquetas = db.session.query(Tag).filter(Tag.id_tag.in_(tags_ids)).all()
    print(f"✓ Tags encontrados en BD: {[t.name for t in etiquetas]}")
    sitio.tag = etiquetas

    print(f"\n✓ Sitio después de cambios (ANTES de commit):")
    print(f"  - Nombre: {sitio.name}")
    print(f"  - Ciudad: {sitio.city}")
    print(f"  - Visible: {sitio.is_visible}")
    print(f"  - Tags: {[t.name for t in sitio.tag]}")

    # Detectar cambios (código existente...)
    cambios_detectados = []
    
    if estado_anterior['name'] != sitio.name:
        cambios_detectados.append(f"Nombre: '{estado_anterior['name']}' → '{sitio.name}'")
    
    if estado_anterior['short_description'] != sitio.short_description:
        cambios_detectados.append("Descripción breve modificada")
    
    if estado_anterior['full_description'] != sitio.full_description:
        cambios_detectados.append("Descripción completa modificada")
    
    if estado_anterior['city'] != sitio.city:
        cambios_detectados.append(f"Ciudad: '{estado_anterior['city']}' → '{sitio.city}'")
    
    if estado_anterior['state'] != sitio.state:
        estado_viejo = db.session.get(State, estado_anterior['state'])
        estado_nuevo = db.session.get(State, sitio.state)
        cambios_detectados.append(f"Provincia: '{estado_viejo.name}' → '{estado_nuevo.name}'")
    
    lat_anterior = estado_anterior['latitude']
    lat_nueva = float(sitio.latitude) if sitio.latitude else None
    if lat_anterior != lat_nueva:
        cambios_detectados.append(f"Latitud: {lat_anterior} → {lat_nueva}")
    
    lon_anterior = estado_anterior['longitude']
    lon_nueva = float(sitio.longitude) if sitio.longitude else None
    if lon_anterior != lon_nueva:
        cambios_detectados.append(f"Longitud: {lon_anterior} → {lon_nueva}")
    
    if estado_anterior['conservation_state'] != sitio.conservation_state:
        cambios_detectados.append(f"Estado conservación: '{estado_anterior['conservation_state'] or 'N/A'}' → '{sitio.conservation_state or 'N/A'}'")
    
    if estado_anterior['inauguration_year'] != sitio.inauguration_year:
        cambios_detectados.append(f"Año inauguración: {estado_anterior['inauguration_year'] or 'N/A'} → {sitio.inauguration_year or 'N/A'}")
    
    if estado_anterior['category'] != sitio.category:
        cat_vieja = db.session.get(Category, estado_anterior['category'])
        cat_nueva = db.session.get(Category, sitio.category)
        cambios_detectados.append(f"Categoría: '{cat_vieja.name}' → '{cat_nueva.name}'")
    
    if estado_anterior['is_visible'] != sitio.is_visible:
        cambios_detectados.append(f"Visibilidad: {'Visible' if estado_anterior['is_visible'] else 'Oculto'} → {'Visible' if sitio.is_visible else 'Oculto'}")
    
    # Comparar tags
    tags_nuevos = set([tag.id_tag for tag in sitio.tag])
    if estado_anterior['tags'] != tags_nuevos:
        tags_agregados = tags_nuevos - estado_anterior['tags']
        tags_eliminados = estado_anterior['tags'] - tags_nuevos
        
        if tags_agregados:
            nombres_tags = [db.session.get(Tag, tid).name for tid in tags_agregados]
            cambios_detectados.append(f"Etiquetas agregadas: {', '.join(nombres_tags)}")
        
        if tags_eliminados:
            nombres_tags = [db.session.get(Tag, tid).name for tid in tags_eliminados]
            cambios_detectados.append(f"Etiquetas eliminadas: {', '.join(nombres_tags)}")

    print(f"\n✓ Cambios detectados: {len(cambios_detectados)}")
    for cambio in cambios_detectados:
        print(f"  - {cambio}")

    # Guardar en base de datos
    try:
        print(f"\n⏳ Ejecutando primer commit (actualización del sitio)...")
        db.session.commit()
        print(f"✓ Primer commit exitoso")
        
        # Verificar que el sitio sigue existiendo
        sitio_verificacion = db.session.get(Site, site_id)
        if sitio_verificacion:
            print(f"✓ Sitio verificado después del commit: {sitio_verificacion.name}")
        else:
            print(f"❌ ALERTA El sitio desapareció después del commit")
        
        # Registrar en historial si hubo cambios
        if cambios_detectados:
            detalle_cambios = "\n".join(cambios_detectados)
            
            user_id = int(request.form.get("user_id", 1))
            print(f"\n⏳ Registrando en historial (user_id: {user_id})...")
            
            nuevo_historial = SiteHistory(
                id_site=site_id,
                id_user=user_id,
                #email=session.get("user", "unknown"),  # <-- tomamos el email desde la sesión
                action_type="UPDATE",
                action_detail=detalle_cambios
            )
            db.session.add(nuevo_historial)
            
            print(f"⏳ Ejecutando segundo commit (historial)...")
            db.session.commit()
            print(f"✓ Segundo commit exitoso")
            
            flash(f"Sitio actualizado correctamente. {len(cambios_detectados)} cambio(s) registrado(s).", "success")
        else:
            flash("Sitio guardado sin cambios detectados.", "info")
        
        print(f"\n{'='*60}")
        print(f"✓ ACTUALIZACIÓN COMPLETADA CON ÉXITO")
        print(f"{'='*60}\n")
        
        return redirect(url_for("issues.index"))
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ ERROR EN COMMIT:")
        print(f"  {str(e)}")
        print(f"{'='*60}\n")
        
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
    
    nombre_sitio = sitio.name
    ciudad_sitio = sitio.city
    
    try:
        historial_eliminacion = SiteHistory(
            id_site=site_id,
            id_user=user_id,  # ← Usar el user_id del form
            action_type="DELETE",
            action_detail=f"Sitio '{nombre_sitio}' eliminado (estaba en {ciudad_sitio})"
        )
        db.session.add(historial_eliminacion)
        db.session.commit()
        
        db.session.delete(sitio)
        db.session.commit()
        
        flash("Sitio eliminado correctamente", "success")
        return redirect(url_for("issues.index"))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar el sitio: {str(e)}", "error")
        return redirect(url_for("issues.index"))

# =====================================================
# HISTORIAL DE CAMBIOS DE SITIO
# =====================================================
@bp.get("/<int:site_id>/historial")
def historial(site_id):
    """Muestra el historial de cambios de un sitio."""
    
    # Verificar que el sitio existe
    sitio = db.session.get(Site, site_id)
    if not sitio:
        flash("Sitio no encontrado.", "error")
        return redirect(url_for("issues.index"))
    
    # Obtener todos los cambios del sitio ordenados por fecha (más reciente primero)
    cambios = (
        db.session.query(SiteHistory)
        .filter(SiteHistory.id_site == site_id)
        .order_by(SiteHistory.date_action.desc())
        .all()
    )
    
    return render_template("sites/historial.html", sitio=sitio, cambios=cambios)

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
