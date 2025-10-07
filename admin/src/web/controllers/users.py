from flask import Blueprint, render_template, redirect, url_for, request

# Importamos las funciones de la capa CORE/AUTH/USER (Ubicación correcta)
from src.core.auth.__init__ import listar_usuarios


# Creamos un nuevo Blueprint con el nombre 'users' y el prefijo /gestion_usuarios
# Esto nos dará endpoints como 'users.user_index', 'users.user_new', etc.
user_bp = Blueprint("users", __name__, url_prefix="/gestion_usuarios")


# Ruta para LISTAR usuarios
@user_bp.route("/", methods=["GET"])
def user_index():
    """Muestra la lista de todos los usuarios con filtros y ordenamiento."""
    

    is_active_param = request.args.get('is_active', type=str)
    

    rol_param = request.args.get('rol', type=str)
    

    order_param = request.args.get('order_by_creation_date', 'asc', type=str).lower()
    

    is_active_filter = None
    if is_active_param is not None:
        is_active_param_lower = is_active_param.lower()
        if is_active_param_lower in ('true', '1'):
            is_active_filter = True
        elif is_active_param_lower in ('false', '0'):
            is_active_filter = False
    

    users = listar_usuarios(
        is_active=is_active_filter, 
        rol=rol_param, 
        order_by_creation_date=order_param
    )
    
    
    return render_template("gestion_usuarios.html", 
                           users=users,
                           # Variables para el HTML (current_X)
                           current_is_active=is_active_param,
                           current_rol=rol_param,
                           current_order=order_param)

# Ruta para el formulario de CREAR nuevo usuario
@user_bp.route("/new", methods=["GET"])
def user_new():
    """Muestra el formulario para crear un nuevo usuario. Endpoint: users.user_new"""
    # Aquí irá el formulario real de creación
    return render_template("user_new.html") # Necesitas crear user_new.html


# Ruta para PROCESAR la eliminación de un usuario
@user_bp.route("/<int:user_id>/delete", methods=["POST"])
def user_delete(user_id):
    """Elimina un usuario por su ID y redirige a la lista. Endpoint: users.user_delete"""
    
    # Llama a la función para eliminar el usuario de la DB
    delete_user(user_id)
    
    # Redirige de vuelta a la lista de usuarios.
    return redirect(url_for("users.user_index"))
