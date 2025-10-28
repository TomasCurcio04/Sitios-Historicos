# pylint: disable=import-error
"""Servicio de usuarios."""

import math
from datetime import datetime, timezone
from src.core.entity.users import Users
from src.core.database import db
from src.core.entity.role import Role
from src.core.services.auth.bcrypt import bcrypt
from sqlalchemy import desc


def listar_usuarios(
    page=1,
    per_page=25,
    is_active: bool | None = None,
    rol: str | None = None,
    search_email=None,
    sort_order="asc",
):
    """Lista usuarios con filtros y paginación.

    Args:
        page: Número de página
        per_page: Usuarios por página
        is_active: Filtro por estado activo
        rol: Filtro por nombre de rol
        search_email: Búsqueda por email
        sort_order: Orden de clasificación (asc/desc)

    Returns:
        Diccionario con usuarios, total, páginas y metadatos
    """

    query = db.session.query(Users)

    if is_active is not None:
        query = query.filter(Users.active == is_active)

    if rol is not None:
        query = query.join(Users.rol_rel).filter(Role.name == rol)

    if search_email:
        query = query.filter(Users.email.ilike(f"%{search_email}%"))

    if sort_order == "desc":
        query = query.order_by(Users.date_create.desc())
    else:
        query = query.order_by(Users.date_create.asc())

    total = query.count()
    items = (
        query.order_by(Users.date_create.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    pages = math.ceil(total / per_page)

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
        "sort_order": sort_order,
    }


def buscar_usuario(email):
    """Busca un usuario por su correo electrónico.

    Args:
        email: Correo electrónico del usuario

    Returns:
        Usuario encontrado o None
    """
    return db.session.query(Users).filter_by(email=email).first()


def verificar_usuario(email, password):
    """Verifica las credenciales de un usuario.

    Args:
        email: Correo electrónico
        password: Contraseña en texto plano

    Returns:
        Tupla (usuario, error) donde usuario es None si hay error
    """
    user = buscar_usuario(email)
    if not user:
        return None, "Email o contraseña incorrectos"

    if (
        not user.password
        or user.password.strip() == ""
        or not bcrypt.check_password_hash(user.password, password)
    ):
        return None, "Email o contraseña incorrectos"

    if not user.active:
        return None, "El usuario no está activo"

    return user, None


def create_user(**kwargs):
    """Crea un nuevo usuario con contraseña hasheada.

    Args:
        **kwargs: Datos del usuario (email, password, user_name, etc.)

    Returns:
        Usuario creado o mensaje de error
    """
    if "email" in kwargs and buscar_usuario(kwargs["email"]):
        return "El email ya está registrado"
    if "password" in kwargs:
        kwargs["password"] = bcrypt.generate_password_hash(kwargs["password"]).decode(
            "utf-8"
        )
    new_user = Users(**kwargs)
    db.session.add(new_user)

    try:
        db.session.commit()
        return new_user
    except:
        db.session.rollback()
        return "Error al crear el usuario"


def eliminar_usuario(email):
    """Desactiva un usuario (eliminación lógica).

    Args:
        email: Correo electrónico del usuario

    Returns:
        Usuario desactivado o None si no existe
    """
    user = buscar_usuario(email)
    if user:
        user.active = False
        db.session.commit()
        return user
    return None


def actualizar_usuario(email, **kwargs):
    """Actualiza los datos de un usuario.

    Args:
        email: Correo electrónico del usuario
        **kwargs: Campos a actualizar

    Returns:
        Tupla (exito, mensaje)
    """
    user = buscar_usuario(email)

    if not user:
        return False, "Usuario no encontrado"

    user.user_name = kwargs.get("user_name", user.user_name)
    user.role = kwargs.get("role", user.role)
    user.s_user = kwargs.get("s_user", user.s_user)
    user.modify = datetime.now(timezone.utc)

    db.session.commit()
    return True, "Usuario actualizado."


def obtener_usuario_por_id(usuario_id):
    """Obtiene un usuario por su ID.

    Args:
        usuario_id: ID del usuario

    Returns:
        Usuario encontrado o None
    """
    return db.session.query(Users).get(usuario_id)


def usuario_actual():
    """Obtiene el usuario actual desde la sesión.

    Returns:
        Usuario actual o None si no hay sesión activa
    """
    try:
        from flask import session as current_user

        if not current_user.get("user"):
            return None
        return buscar_usuario(current_user.get("user"))
    except RuntimeError:
        # Fuera del contexto de request
        return None
