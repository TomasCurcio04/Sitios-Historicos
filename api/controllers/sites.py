"""Controlador de sitios de la API"""

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.sites import SiteQuerySchema, SitesListResponseSchema
from api.services.site_serv.utils_site import all_sites_to_json

bp = Blueprint("api_sites", __name__, url_prefix="/api/sites")


@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def all_sites():
    """Retorna sitios con filtros."""
    try:
        # Validar parámetros usando schema
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
        
        # Obtener sitios
        sites_data = all_sites_to_json(**params)
        
        # Serializar respuesta usando schema
        response_schema = SitesListResponseSchema()
        return jsonify(response_schema.dump(sites_data))
        
    except Exception as e:
        # Log temporal para debuggear
        print(f"Error en API sites: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500
