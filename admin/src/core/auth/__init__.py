from src.core.database import db
from src.core.auth.users import Users
from src.core.auth.role import Role
from src.core.auth.permission import Permission

#### Funciones de usuarios ###
def list_users():
    """Listar todos los usuarios."""
    session = db.session
    users = session.query(Users).all()
    return users

def create_user(**kwargs):
    """Crear un nuevo usuario."""
    session = db.session
    new_user = Users(**kwargs)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

####Fin de funciones de usuarios###

####Funciones de roles###
def list_roles():
    session = db.session
    return session.query(Role).all()

def create_role(**kwargs):
    session = db.session
    new_role = Role(**kwargs)
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role

def assign_role(user_id, role_id):
    session = db.session
    user = session.query(Users).get(user_id)
    role = session.query(Role).get(role_id)
    user.role = role
    session.commit()
    return user

####Fin de funciones de roles###

####Funciones de permisos###
def list_permissions():
    session = db.session
    return session.query(Permission).all()

def create_permission(**kwargs):
    session = db.session
    perm = Permission(**kwargs)
    session.add(perm)
    session.commit()
    session.refresh(perm)
    return perm

def assign_permission(role_id, permission_id):
    session = db.session
    role = session.query(Role).get(role_id)
    perm = session.query(Permission).get(permission_id)
    role.permission.append(perm)
    session.commit()
    return role

####Fin de funciones de permisos###

####Funciones de feature flags###
def list_feature_flags():
    from src.core.auth import feature_flags
    session = db.session
    return session.query(feature_flags.FeatureFlag).all()

def modify_feature_flag(name, enabled, updated_by, maintenance_message=None):
    from src.core.auth import feature_flags
    session = db.session
    flag = session.query(feature_flags.FeatureFlag).filter_by(name=name).first()
    if flag:
        flag.enabled = enabled
        flag.updated_by = updated_by
        if maintenance_message:
            flag.maintenance_message = maintenance_message
        session.commit()
    return flag

####Fin de funciones de feature flags###
