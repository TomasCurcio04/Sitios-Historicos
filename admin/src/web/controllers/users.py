from flask import Blueprint, render_template, redirect, url_for, request, flash

# Importamos las funciones de la capa CORE/AUTH/USER (Ubicación correcta)
from src.core.auth.__init__ import listar_usuarios, eliminar_usuario, create_user, buscar_usuario, actualizar_usuario
from src.core.auth.users import Users
import re
from src.web.handlers.auth import admin_required
from src.core.auth.user_validador import UserValidator


# Creamos un nuevo Blueprint con el nombre 'users' y el prefijo /gestion_usuarios
# Esto nos dará endpoints como 'users.user_index', 'users.user_new', etc.
user_bp = Blueprint("users", __name__, url_prefix="/gestion_usuarios")



# Ruta para LISTAR usuarios
@user_bp.route("/", methods=["GET"])
@admin_required
def user_index():
    """Muestra la lista de todos los usuarios con filtros y ordenamiento."""
    
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
    """Muestra el formulario para crear un nuevo usuario. Endpoint: users.user_new"""
    # Aquí irá el formulario real de creación
    return render_template("user_new.html")

@user_bp.route("/create", methods=["POST"])
@admin_required
def user_create():

    # 1. Ejecutar el Validador (Maneja Formato, Limpieza y Conversión)
    validator = UserValidator(request.form)

    if not validator.validate():
        # Si la validación de formato falla:
        for field, error_msg in validator.errors.items():
            flash(error_msg, "error")
        
        # Devuelve el formulario con los datos brutos anteriores
        return render_template(
            "user_new.html",
            email=request.form.get("email"),
            username=request.form.get("username"),
            rol=request.form.get("rol")
        )

   
    clean_data = validator.data_cleaned 
    
    
    result = create_user(
        email=clean_data["email"],
        user_name=clean_data["username"],
        password=clean_data["password"],
        role=clean_data["rol"] 
    )

    #Manejo de Errores de Negocio/Persistencia
    if isinstance(result, str):
        flash(result, "error")
        

        return render_template(
            "user_new.html",
            email=clean_data["email"],
            username=clean_data["username"],
            rol=request.form.get("rol")
        )

    flash("Usuario creado exitosamente", "success")
    return redirect(url_for("users.user_index"))

# Ruta para PROCESAR la eliminación de un usuario
@user_bp.route("/<int:user_id>/delete", methods=["POST"])
@admin_required
def user_delete(user_id):
    """Elimina un usuario por su ID y redirige a la lista. Endpoint: users.user_delete"""
    email = request.form.get("email")
    if email:
        # Llama a la función para eliminar el usuario de la DB
        eliminar_usuario(email)
    
    # Redirige de vuelta a la lista de usuarios.
    return redirect(url_for("users.user_index"))

@user_bp.route("/<string:email>/edit", methods=["GET"])
@admin_required
def user_edit(email):
    user = buscar_usuario(email)

    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("users.user_index"))

    return render_template("user_edit.html", user=user) 

@user_bp.route("/<string:email>/update", methods=["POST"])
@admin_required
def user_update(email):
    """Procesa los datos y actualiza el usuario."""

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