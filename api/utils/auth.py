"""Utilidades de autenticación para la API"""

from flask import request, jsonify, current_app
import jwt
from src.core.services.auth.user_serv import buscar_usuario_public


def get_authenticated_user():
    """
    Obtiene el usuario autenticado desde el token JWT.
    
    Returns:
        dict: Información del usuario o None si no está autenticado
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        
        # Buscar usuario en la base de datos por email del token
        user = buscar_usuario_public(payload.get('email'))
        if not user:
            return None
        
        return {
            'public_user_id': user.id,
            'user_id': user.id,
            'email': user.email
        }
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        print(f"Error en get_authenticated_user: {str(e)}")
        return None


def require_auth():
    """
    Verifica que el usuario esté autenticado.
    
    Returns:
        tuple: (user_info, error_response) - Si hay error, user_info es None
    """
    user = get_authenticated_user()
    if not user:
        error_response = jsonify({
            "error": {
                "code": "unauthorized",
                "message": "Authentication required"
            }
        }), 401
        return None, error_response
    
    return user, None