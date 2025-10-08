from sqlalchemy import desc
from .users import Users

"""Modulo para gestionar usuarios"""

# pylint: disable=import-error
from src.core.database import db
from src.core.auth.users import Users
from src.core.auth.role import Role
from src.core.auth.permission import Permission
from src.core.auth.bcrypt import bcrypt


####Funciones de usuarios###
from sqlalchemy import desc
# Asegúrate de importar el modelo Role
from src.core.auth.role import Role
# Asegúrate de importar db y Users

def listar_usuarios(is_active: bool | None = None, 
 rol: str | None = None, 
 order_by_creation_date: str | None = 'asc'
):
    """ Lista usuarios aplicando solo un criterio """
    
    query = db.session.query(Users)

    
    if is_active is not None:
        query = query.filter(Users.active == is_active)
        return query.all() 

    
    if rol is not None:
        query = query.join(Users.rol_rel).filter(Role.name == rol)
        return query.all() 

    
    if order_by_creation_date == 'asc':
        query = query.order_by(Users.date_create.asc()) 
    elif order_by_creation_date == 'desc':
        query = query.order_by(Users.date_create.desc())
    
    
    return query.all()

def buscar_usuario(email):
    """Busca un usuario por su correo electrónico y contraseña."""
    return db.session.query(Users).filter_by(email=email).first()

def verificar_usuario(email, password):
    user = buscar_usuario(email)
    if not user:
        return None, "Email o contraseña incorrectos"
    if not user.active:
        return None, "El usuario no está activo"
    if not user.password or user.password.strip() == "" or not bcrypt.check_password_hash(user.password, password):
        return None, "Email o contraseña incorrectos"
    return user, None
def create_user(**kwargs):
    """Función para crear un nuevo usuario con contraseña hasheada."""
    if "password" in kwargs:
        kwargs["password"] = bcrypt.generate_password_hash(kwargs["password"]).decode("utf-8")
    new_user = Users(**kwargs)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def eliminar_usuario(email):
    """Funcion para recibir un usuario y eliminarlo."""
    user = buscar_usuario(email)
    if user:
        user.active = False
        db.session.commit()
        return user
    return None


####Fin de funciones de usuarios###

####Funciones de roles###


def list_roles():
    """Función para listar todos los roles."""
    roles = db.session.query(Role).all()
    return roles


def create_role(**kwargs):
    """Función para crear un nuevo rol."""
    new_role = Role(**kwargs)
    db.session.add(new_role)
    db.session.commit()
    return new_role


def assign_role(user, role):
    """Función para asignar un rol a un usuario."""
    user.role = role
    db.session.commit()
    return user


# ####Fin de funciones de roles###


####Funciones de permisos###
def list_permissions():
    """Función para listar todos los permisos."""
    permissions = db.session.query(Permission).all()
    return permissions


def assign_permission(role, permission):
    """Función para asignar un permiso a un rol."""
    role.permission.append(permission)
    db.session.commit()
    return role


def create_permission(**kwargs):
    """Función para crear un nuevo permiso."""
    new_permission = Permission(**kwargs)
    db.session.add(new_permission)
    db.session.commit()
    return new_permission


# ####Fin de funciones de permisos###
