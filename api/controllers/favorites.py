"""Controlador de favoritos de la API"""

from flask import Blueprint, jsonify
from api.services.site_serv.utils_site import get_site_by_id
from src.core.services.board.site_favorites import toggle_site_favorite

bp = Blueprint("api_favorites", __name__, url_prefix="/api/sites")


@bp.route("/<int:site_id>/favorite", methods=["PUT"])
def toggle_site_favorite_endpoint(site_id):
    """Alterna el estado de favorito de un sitio."""
    try:
        # TODO: Implementar autenticación JWT cuando esté disponible
        # Placeholder: usar public_user_id = 1 hasta que esté la autenticación
        public_user_id = 1
        
        # Verificar que el sitio existe
        site_data = get_site_by_id(site_id)
        if not site_data:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        # Llamar a la función que maneja todo
        toggle_site_favorite(site_id, public_user_id)
        
        # Respuesta 204 No Content (éxito sin contenido)
        return '', 204
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500