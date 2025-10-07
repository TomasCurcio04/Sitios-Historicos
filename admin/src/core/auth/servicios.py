from sqlalchemy import desc
from src.core.database import db
from src.core.auth.users import Users

def create_user(**kwargs):
    try:
        user = Users(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user
    except ValueError as e:
        # Si hay un error de validación, deshace la transacción
        db.session.rollback() 
        
        raise e
    

def listar_usuarios(is_active: bool | None = None, 
                    rol: str | None = None, 
                    order_by_creation_date: str | None = 'asc'
):
    """ Lista usuarios con filtros opcionales."""
    
    query = db.session.query(Users)
    
    if is_active is not None:
        query = query.filter(Users.active == is_active)
    
    if rol is not None:
        
        query = query.filter(Users.rol == rol)
    
    if order_by_creation_date == 'asc':
        # Ordena de la fecha más antigua a la más nueva
        query = query.order_by(Users.date_create) 
    elif order_by_creation_date == 'desc':
        # Ordena de la fecha más nueva a la más antigua (más común para listados recientes)
        query = query.order_by(desc(Users.date_create))

    return query.all()

def busqueda_por_mail(email: str):
    """Busca un usuario por su correo electrónico."""
    return db.session.query(Users).filter_by(email=email).first()

def actualizar_usuario(user_id: int, datos_a_actualizar: dict):
    """
    Actualiza los campos de un usuario específico.
    """

    user = db.session.query(Users).filter_by(id=user_id).first()

    if not user:
        return None

    campos_permitidos = ['user_name', 'rol', 'active', 'email'] 
    
    for key, value in datos_a_actualizar.items():
        if key in campos_permitidos:
            setattr(user, key, value)
        else:           
            print(f"Advertencia: El campo '{key}' no puede ser actualizado.") 

    try:
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar el usuario {user_id}: {e}")
        return None
    
def buscar_usuario(email,password):
    """Busca un usuario por su correo electrónico y contraseña."""
    return db.session.query(Users).filter_by(email=email, password=password).first()