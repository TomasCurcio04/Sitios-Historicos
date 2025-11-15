"""Controlador de sitios de la API"""

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.sites import SiteQuerySchema, SitesListResponseSchema, SiteResponseSchema
from api.services.site_serv.utils_site import all_sites_to_json, get_site_by_id

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
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp.route("/<int:site_id>", methods=["GET"])
def get_site(site_id):
    """Obtiene detalles de un sitio específico por ID."""
    try:
        site_data = get_site_by_id(site_id)
        
        if not site_data:
            return jsonify({
                "error": {
                    "code": "not_found",
                    "message": "Site not found"
                }
            }), 404
        
        # Serializar respuesta usando schema
        response_schema = SiteResponseSchema()
        return jsonify(response_schema.dump(site_data))
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500
