# pylint: disable=import-error
"""Servicio de usuarios."""

import math
from datetime import datetime, timezone
from src.core.entity.users import Users
from src.core.database import db
from src.core.entity.role import Role
from src.core.services.auth.bcrypt import bcrypt
from sqlalchemy import desc
from src.core.database import db
from src.core.entity.public_user import PublicUser

def listar_usuarios(
    page=1,
    per_page=25,
    is_active: bool | None = None,
    rol: str | None = None,
    search_email=None,
    sort_order="asc",
):
    """Lista usuarios aplicando solo un criterio."""

    query = db.session.query(Users)

    if is_active is not None:
        query = query.filter(Users.active == is_active)

    if rol:
        query = query.outerjoin(Users.rol_rel).filter(Role.name == rol)

    if search_email:
        query = query.filter(Users.email.ilike(f"%{search_email}%"))

    if sort_order == "desc":
        query = query.order_by(Users.date_create.desc())
    else:
        query = query.order_by(Users.date_create.asc())
    
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    pages = math.ceil(total / per_page)

    roles = db.session.query(Role).order_by(Role.name).all()

    return {
        "items": items,
        "roles": roles,
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
    if "user_name" in kwargs and buscar_username(kwargs["user_name"]):
        return "El nombre de usuario ya está registrado"
    if "password" in kwargs:
        kwargs["password"] = bcrypt.generate_password_hash(kwargs["password"]).decode(
            "utf-8"
        )

    role_id = kwargs.get("rol")
    try:
        role_id = int(role_id)
    except (TypeError, ValueError):
        return "Debes seleccionar un rol válido2"
    role_obj = db.session.get(Role, role_id)
    if not role_obj:
        return "Debes seleccionar un rol válido3"

    new_user = Users(
        email=kwargs["email"],
        user_name=kwargs["user_name"],
        password=kwargs["password"],
        s_user=kwargs.get("s_user", False),
        active=kwargs.get("active", True),
        rol_rel = role_obj,
        role = role_id
    )
    
    db.session.add(new_user)

    try:
        db.session.commit()
        return new_user
    except:
        db.session.rollback()
        return "Error al crear el usuario"



def create_user_public(**kwargs):
    """
    Crea un nuevo usuario público (PublicUser).

    Args:
        **kwargs: Datos del usuario (google_id, email, name, picture)

    Returns:
        PublicUser creado o mensaje de error
    """

    # Validaciones básicas
    if "google_id" not in kwargs or not kwargs["google_id"]:
        return "Debe proporcionar un google_id"
    if "email" not in kwargs or not kwargs["email"]:
        return "Debe proporcionar un email"
    if "name" not in kwargs or not kwargs["name"]:
        return "Debe proporcionar un nombre"

    # Evitar duplicados por google_id
    existing_user = db.session.query(PublicUser).filter_by(google_id=kwargs["google_id"]).first()
    if existing_user:
        return "El google_id ya está registrado"

    # Crear el usuario público
    new_user = PublicUser(
        google_id=kwargs["google_id"],
        email=kwargs["email"],
        name=kwargs["name"],
        picture=kwargs.get("picture")
    )

    db.session.add(new_user)

    try:
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        return f"Error al crear el usuario público: {str(e)}"



def eliminar_usuario(user_id):
    """Desactiva un usuario (eliminación lógica).

    Args:
        email: Correo electrónico del usuario

    Returns:
        Usuario desactivado o None si no existe
    """
    print("Eliminando usuario con ID:", user_id)
    user = obtener_usuario_por_id(user_id)
    if user:
        user.active = False
        db.session.commit()
        return user
    return None


def actualizar_usuario(user_id, **kwargs):
    """Actualiza los datos de un usuario.

    Args:
        email: Correo electrónico del usuario
        **kwargs: Campos a actualizar

    Returns:
        Tupla (exito, mensaje)
    """
    user = obtener_usuario_por_id(user_id)

    if not user:
        return False, "Usuario no encontrado"
    
    if "user_name" in kwargs:
        existing_user = buscar_username(kwargs["user_name"])
        if existing_user and existing_user.id_user != user_id:
            return False, "El nombre de usuario ya está registrado"

    user.user_name = kwargs.get("user_name", user.user_name)
    user.s_user = kwargs.get("s_user", user.s_user)
    user.modify = datetime.now(timezone.utc)

    role_id = kwargs.get("role")
    if role_id is not None:
        role = db.session.get(Role, role_id)
        if not role:
            return False, "Rol no encontrado"
        user.rol_rel = role

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
    
def buscar_username(username):
    """Busca un usuario por su nombre de usuario.
    
    Args:
        username: Nombre de usuario
    Returns:
        Usuario encontrado o None
    """
    
    return db.session.query(Users).filter_by(user_name=username).first()
