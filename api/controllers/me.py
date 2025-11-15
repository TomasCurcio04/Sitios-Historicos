"""Controlador para endpoints del usuario autenticado (/me)"""

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.sites import SiteQuerySchema, SitesListResponseSchema
from src.core.services.board.site_favorites import get_user_favorites
from api.services.site_serv.utils_site import site_to_dict

bp = Blueprint("api_me", __name__, url_prefix="/api/me")


@bp.route("/favorites", methods=["GET"])
def get_my_favorites():
    """Lista los sitios favoritos del usuario autenticado."""
    try:
        # TODO: Implementar autenticación JWT cuando esté disponible
        # Placeholder: usar public_user_id = 1 hasta que esté la autenticación
        public_user_id = 1
        
        # Validar parámetros de paginación
        schema = SiteQuerySchema()
        try:
            params = schema.load(request.args)
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "invalid_query",
                    "message": "Parameter validation failed",
                    "details": err.messages
                }
            }), 400
        
        # Obtener favoritos del usuario
        favorites_result = get_user_favorites(
            public_user_id, 
            page=params.get('page', 1),
            per_page=params.get('per_page', 20)
        )
        
        # Convertir sitios favoritos a formato API
        sites_data = []
        for favorite in favorites_result['items']:
            site_dict = site_to_dict(favorite.site_rel)
            sites_data.append(site_dict)
        
        # Respuesta en formato estándar
        response_data = {
            "data": sites_data,
            "meta": {
                "page": favorites_result['page'],
                "per_page": favorites_result['per_page'],
                "total": favorites_result['total']
            }
        }
        
        # Serializar respuesta
        response_schema = SitesListResponseSchema()
        return jsonify(response_schema.dump(response_data))
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500