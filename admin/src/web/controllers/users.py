"""Controlador de gestión de usuarios para el panel administrativo."""

from flask import Blueprint, render_template, redirect, url_for, request, flash

# Importamos las funciones de la capa CORE/AUTH/USER (Ubicación correcta)
from src.core.services.auth.user_serv import listar_usuarios, eliminar_usuario, create_user, buscar_usuario, actualizar_usuario
from src.core.entity.users import Users
import re
from src.web.handlers.auth import admin_required



# Creamos un nuevo Blueprint con el nombre 'users' y el prefijo /gestion_usuarios
# Esto nos dará endpoints como 'users.user_index', 'users.user_new', etc.
user_bp = Blueprint("users", __name__, url_prefix="/gestion_usuarios")



# Ruta para LISTAR usuarios
@user_bp.route("/", methods=["GET"])
@admin_required
def user_index():
    """Lista usuarios con filtros, paginación y ordenamiento.
    
    Permite filtrar por estado activo, rol y email, además de
    ordenar por fecha de creación ascendente o descendente.
    """
    
    page = request.args.get('page', 1, type=int)
    PER_PAGE = 25
    
    is_active_param = request.args.get('is_active', type=str)

    rol_param = request.args.get('rol', type=str)
    
    search_email_param = request.args.get('email', type=str)

    sort_order = request.args.get('sort', 'asc')
    
    is_active_filter = None
    if is_active_param:
        lower_param = is_active_param.lower()
        if lower_param in ('true', '1'):
            is_active_filter = True
        elif lower_param in ('false', '0'):
            is_active_filter = False
    

    pagination = listar_usuarios(
        page=page,
        per_page=PER_PAGE,
        is_active=is_active_filter, 
        rol=rol_param, 
        search_email=search_email_param,
        sort_order = sort_order
    )
    
    start = ((pagination["page"] - 1) * pagination["per_page"]) + 1
    end = min(pagination["page"] * pagination["per_page"], pagination["total"])
    
    return render_template(
        "gestion_usuarios.html", 
        pagination=pagination,
        users=pagination["items"],  
        # Usamos la versión string para el filtro 'Activo' en la plantilla
        current_is_active=is_active_param, 
        current_rol=rol_param,
        # filters=request.args ya contiene todos los parámetros de la URL para la paginación
        filters=request.args,
        sort_order = request.args.get('sort', 'asc'),
        start=start,
        end=end
    )

# Ruta para el formulario de CREAR nuevo usuario
@user_bp.route("/new", methods=["GET"])
@admin_required
def user_new():
    """Muestra el formulario para crear un nuevo usuario."""
    # Aquí irá el formulario real de creación
    return render_template("user_new.html")

@user_bp.route("/create", methods=["POST"])
@admin_required
def user_create():
    """Procesa la creación de un nuevo usuario."""
    # Obtener los datos del formulario
    email = request.form.get("email", "").strip().lower()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    rol = request.form.get("rol", "")

    # Validaciones
    if not re.match(Users.EMAIL_REGEX, email):
        flash("Email inválido", "error")
        return render_template(
            "user_new.html",
            email=email,
            username=username,
            rol=rol
        )

    if len(password) < 6:
        flash("La contraseña debe tener al menos 6 caracteres", "error")
        return render_template(
            "user_new.html",
            email=email,
            username=username,
            rol=rol
        )

    if password != confirm_password:
        flash("Las contraseñas no coinciden", "error")
        return render_template(
            "user_new.html",
            email=email,
            username=username,
            rol=rol
        )

    
    try:
        rol = int(rol)
    except ValueError:
        flash("Debes seleccionar un rol válido", "error")
        return render_template(
            "user_new.html",
            email=email,
            username=username
        )

    
    result = create_user(email=email, user_name=username, password=password, role=rol)

    if isinstance(result, str):
        flash(result, "error")
        return render_template(
            "user_new.html",
            email=email,
            username=username,
            rol=rol
        )

    
    flash("Usuario creado exitosamente", "success")
    return redirect(url_for("users.user_index"))

# Ruta para PROCESAR la eliminación de un usuario
@user_bp.route("/<int:user_id>/delete", methods=["POST"])
@admin_required
def user_delete(user_id):
    """Desactiva un usuario (eliminación lógica)."""
    email = request.form.get("email")
    if email:
        # Llama a la función para eliminar el usuario de la DB
        eliminar_usuario(email)
    
    # Redirige de vuelta a la lista de usuarios.
    return redirect(url_for("users.user_index"))

@user_bp.route("/<string:email>/edit", methods=["GET"])
@admin_required
def user_edit(email):
    """Muestra el formulario de edición de usuario."""
    user = buscar_usuario(email)

    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("users.user_index"))

    return render_template("user_edit.html", user=user) 

@user_bp.route("/<string:email>/update", methods=["POST"])
@admin_required
def user_update(email):
    """Procesa la actualización de datos del usuario."""

    user = buscar_usuario(email)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("users.user_index"))
    
    rol_str = request.form.get("role")

    rol_value = int(rol_str)
    data = {
        "user_name": request.form.get("user_name"),
        "role": rol_value,
        "s_user": "s_user" in request.form
    }

    success, message = actualizar_usuario(email, **data)

    if success:
        flash(f"Usuario {data['user_name']} actualizado exitosamente.", "success")
        return redirect(url_for("users.user_index"))
    else:
        # Esto captura errores como problemas de DB o lógica del Core
        flash(f"Error al actualizar el usuario: {message}", "error")
        return redirect(url_for("users.user_edit", email=email))
