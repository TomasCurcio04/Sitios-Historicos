"""Utilidades de autenticación para la API"""

from flask import request, jsonify


def get_authenticated_user():
    """
    Obtiene el usuario autenticado desde el token JWT.
    
    Returns:
        dict: Información del usuario o None si no está autenticado
    """
    # TODO: Implementar validación JWT real cuando esté disponible
    # auth_header = request.headers.get('Authorization')
    # if not auth_header or not auth_header.startswith('Bearer '):
    #     return None
    # 
    # token = auth_header.split(' ')[1]
    # try:
    #     # Validar y decodificar JWT
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    #     return {
    #         'public_user_id': payload.get('public_user_id'),
    #         'user_id': payload.get('user_id'),
    #         'email': payload.get('email')
    #     }
    # except jwt.InvalidTokenError:
    #     return None
    
    # Placeholder: simular usuario autenticado
    return {
        'public_user_id': 1,
        'user_id': 1,
        'email': 'test@example.com'
    }


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