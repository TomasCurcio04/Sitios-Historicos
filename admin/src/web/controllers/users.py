"""Controlador de gestión de usuarios para el panel administrativo."""

from flask import Blueprint, render_template, redirect, url_for, request, flash

# Importamos las funciones de la capa CORE/AUTH/USER (Ubicación correcta)
from src.core.services.auth.user_serv import (
    listar_usuarios,
    eliminar_usuario,
    create_user,
    obtener_usuario_por_id,
    actualizar_usuario,
    activar_usuario,
)
from src.core.services.auth.role_serv import list_roles
from src.web.handlers.utils import permissions_required
from src.core.services.auth.user_serv.user_validador import UserValidator

# Creamos un nuevo Blueprint con el nombre 'users' y el prefijo /gestion_usuarios
# Esto nos dará endpoints como 'users.user_index', 'users.user_new', etc.
user_bp = Blueprint("users", __name__, url_prefix="/gestion_usuarios")

PER_PAGE = 25


# Ruta para LISTAR usuarios
@user_bp.route("/", methods=["GET"])
@permissions_required("user", ["list"])
def user_index():
    """Lista usuarios con filtros, paginación y ordenamiento.

    Permite filtrar por estado activo, rol y email, además de
    ordenar por fecha de creación ascendente o descendente.
    Args:
        page (int): Página actual para paginación.
        is_active (str): Filtro por estado activo ("true"/"false").
        rol (str): Filtro por rol de usuario.
        email (str): Filtro por email (búsqueda parcial).
    Returns:
        Render de la plantilla con la lista de usuarios paginada.
    """

    page = request.args.get("page", 1, type=int)

    is_active_param = request.args.get("is_active", type=str)

    rol_param = request.args.get("rol", type=str)

    search_email_param = request.args.get("email", type=str)

    sort_order = request.args.get("sort", "asc")

    is_active_filter = None
    if is_active_param:
        lower_param = is_active_param.lower()
        if lower_param in ("true", "1"):
            is_active_filter = True
        elif lower_param in ("false", "0"):
            is_active_filter = False

    pagination = listar_usuarios(
        page=page,
        per_page=PER_PAGE,
        is_active=is_active_filter,
        rol=rol_param,
        search_email=search_email_param,
        sort_order=sort_order,
    )

    roles = list_roles()

    start = ((pagination["page"] - 1) * pagination["per_page"]) + 1
    end = min(pagination["page"] * pagination["per_page"], pagination["total"])

    return render_template(
        "gestion_usuarios.html",
        pagination=pagination,
        users=pagination["items"],
        roles=roles,
        # Usamos la versión string para el filtro 'Activo' en la plantilla
        current_is_active=is_active_param,
        current_rol=rol_param,
        # filters=request.args ya contiene todos los parámetros de la URL para la paginación
        filters=request.args,
        sort_order=request.args.get("sort", "asc"),
        start=start,
        end=end,
    )


# Ruta para el formulario de CREAR nuevo usuario
@user_bp.route("/new", methods=["GET"])
@permissions_required("user", ["create", "edit"])
def user_new():
    """Muestra el formulario para crear un nuevo usuario.
    Args:
        None
    Returns:
        Render del formulario de creación de usuario.
    """
    # Aquí irá el formulario real de creación

    roles = list_roles()

    return render_template("user_new.html", roles=roles)


@user_bp.route("/create", methods=["POST"])
@permissions_required("user", ["create"])
def user_create():
    """Procesa el formulario de creación de un nuevo usuario.
    Args:
        None (datos del formulario vía request.form)
    Returns:
        Redirección a la lista de usuarios o re-render del formulario con errores.
    """
    # 1. Ejecutar el Validador (Maneja Formato, Limpieza y Conversión)
    validator = UserValidator(request.form)

    if not validator.validate():
        # Si la validación de formato falla:
        for _, error_msg in validator.errors.items():
            flash(error_msg, "error")

        # Devuelve el formulario con los datos brutos anteriores
        return render_template(
            "user_new.html",
            email=request.form.get("email"),
            username=request.form.get("username"),
            rol=request.form.get("rol"),
            roles=list_roles(),
        )

    clean_data = validator.data_cleaned
    print("Valor rol", clean_data["rol"])
    result = create_user(
        email=clean_data["email"],
        user_name=clean_data["username"],
        password=clean_data["password"],
        rol=clean_data["rol"],
    )

    if isinstance(result, str):
        flash(result, "error")
        return render_template(
            "user_new.html",
            email=clean_data["email"],
            username=clean_data["username"],
            rol=request.form.get("role"),
            roles=list_roles(),
        )

    flash("Usuario creado exitosamente", "success")
    return redirect(url_for("users.user_index"))


@user_bp.route("/<int:user_id>/delete", methods=["POST"])
@permissions_required("user", ["delete"])
def user_delete(user_id):
    """Desactiva un usuario (eliminación lógica).
    Args:
        user_id (int): ID del usuario a desactivar.
    Returns:
        Redirección a la lista de usuarios.
    """
    user = obtener_usuario_por_id(user_id)

    if user:
        eliminar_usuario(user_id)
        flash("Usuario desactivado correctamente", "success")
    else:
        flash("Usuario no encontrado", "danger")

    return redirect(url_for("users.user_index"))


@user_bp.route("/<int:user_id>/activate", methods=["POST"])
@permissions_required("user", ["update"])
def user_activate(user_id):
    """Reactiva un usuario.
    Args:
        user_id (int): ID del usuario a reactivar.
    Returns:
        Redirección a la lista de usuarios.
    """
    user = obtener_usuario_por_id(user_id)

    if user:
        activar_usuario(user_id)
        flash("Usuario reactivado correctamente", "success")
    else:
        flash("Usuario no encontrado", "danger")

    return redirect(url_for("users.user_index"))


@user_bp.route("/<int:user_id>/edit", methods=["GET"])
@permissions_required("user", ["edit", "view"])
def user_edit(user_id):
    """Muestra el formulario para editar un usuario existente.
    Args:
        user_id (int): ID del usuario a editar.
    Returns:
        Render del formulario de edición de usuario.
    """
    user = obtener_usuario_por_id(user_id)

    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("users.user_index"))

    roles = list_roles()

    current_rol = user.rol_rel.name if user.rol_rel else None

    return render_template(
        "user_edit.html", user=user, roles=roles, current_rol=current_rol
    )


@user_bp.route("/<int:user_id>/update", methods=["POST"])
@permissions_required("user", ["edit"])
def user_update(user_id):
    """Procesa los datos y actualiza el usuario.
    Args:
        user_id (int): ID del usuario a actualizar.
    Returns:
        Redirección a la lista de usuarios o re-render del formulario con errores.
    """

    user = obtener_usuario_por_id(user_id)
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("users.user_index"))

    try:
        rol_id = int(request.form.get("role"))
    except (TypeError, ValueError):
        flash("Rol inválido.", "error")
        return redirect(url_for("users.user_edit", user_id=user_id))

    data = {
        "user_name": request.form.get("user_name"),
        "role": rol_id,
        "s_user": "s_user" in request.form,
    }

    success, message = actualizar_usuario(user_id, **data)

    if success:
        flash(f"Usuario {data['user_name']} actualizado exitosamente.", "success")
        return redirect(url_for("users.user_index"))
        # Esto captura errores como problemas de DB o lógica del Core
    flash(f"Error al actualizar el usuario: {message}", "error")
    return redirect(url_for("users.user_edit", user_id=user_id))
