# pylint: disable=import-error
"""Módulo de autenticación y autorización."""

import math
from datetime import datetime, timezone
from src.core.auth.users import Users
from src.core.auth.feature_flag import FeatureFlag
from sqlalchemy import desc
from src.core.database import db
from src.core.auth.role import Role
from src.core.auth.permission import Permission
from src.core.auth.bcrypt import bcrypt


####Funciones de usuarios###
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
    """Busca un usuario por su correo electrónico y contraseña."""
    return db.session.query(Users).filter_by(email=email).first()


def verificar_usuario(email, password):
    """Verifica las credenciales de un usuario."""
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
    """Función para crear un nuevo usuario con contraseña hasheada."""
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
    """Funcion para recibir un usuario y eliminarlo."""
    user = buscar_usuario(email)
    if user:
        user.active = False
        db.session.commit()
        return user
    return None


def actualizar_usuario(email, **kwargs):
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
    return db.session.query(Users).get(usuario_id)


####Fin de funciones de usuarios###


####Funciones de roles###
def list_roles():
    """Función para listar todos los roles."""
    session = db.session
    return session.query(Role).all()


def create_role(**kwargs):
    """Crea un nuevo rol."""
    session = db.session
    new_role = Role(**kwargs)
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role


def assign_role(user_id, role_id):
    """Asigna un rol a un usuario."""
    session = db.session
    user = session.query(Users).get(user_id)
    role = session.query(Role).get(role_id)
    user.role = role
    session.commit()
    return user


####Fin de funciones de roles###


####Funciones de permisos###
def list_permissions():
    """Función para listar todos los permisos."""
    session = db.session
    return session.query(Permission).all()


def create_permission(**kwargs):
    """Crea un nuevo permiso."""
    session = db.session
    perm = Permission(**kwargs)
    session.add(perm)
    session.commit()
    session.refresh(perm)
    return perm


def assign_permission(role_id, permission_id):
    """Asigna un permiso a un rol."""
    session = db.session
    role = session.query(Role).get(role_id)
    perm = session.query(Permission).get(permission_id)
    role.permission.append(perm)
    session.commit()
    return role


####Fin de funciones de permisos###


####Funciones de feature flags###
def list_feature_flags():
    """Función para listar todas las feature flags."""

    flags = db.session.query(FeatureFlag).order_by(FeatureFlag.id).all()
    return flags


def get_feature_flag(name):
    """Función para obtener una feature flag por su nombre."""

    flag = db.session.query(FeatureFlag).filter_by(name=name).first()
    return flag


def modify_feature_flag(name, enabled, updated_by, maintenance_message=None):
    """Función para modificar una feature flag."""

    flag = FeatureFlag.get_flag(name)
    if flag:
        flag.enabled = enabled
        flag.updated_by = updated_by
        if maintenance_message is not None:
            flag.maintenance_message = maintenance_message
        db.session.commit()
    return flag


def update_feature_flags(flags_data, updated_by):
    """Función para actualizar múltiples feature flags."""
    flags = list_feature_flags()
    has_changes = False
    for flag in flags:
        flag_id = str(flag.id)
        if flag_id in flags_data:
            new_enabled = flags_data[flag_id].get("enabled", False)
            new_message = flags_data[flag_id].get("maintenance_message", "")

            if flag.enabled != new_enabled or flag.maintenance_message != new_message:
                flag.enabled = new_enabled
                flag.maintenance_message = new_message
                flag.updated_by = updated_by
                has_changes = True

    if has_changes:
        db.session.commit()
    return has_changes


####Fin de funciones de feature flags###
