"""Controlador de sitios de la API"""

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.sites import SiteQuerySchema, SitesListResponseSchema, SiteResponseSchema, SiteCreateSchema
from src.web.api.services.site_serv.utils_site import all_sites_to_json, get_site_by_id, create_site
from src.web.api.utils.auth import require_auth

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
        
        # Verificar si necesita buscar en favoritos
        user_id = None
        if params.get('search_favorites'):
            user, auth_error = require_auth()
            if auth_error:
                return auth_error
            user_id = user['user_id']
        
        # Obtener sitios
        sites_data = all_sites_to_json(user_id=user_id, **params)
        
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
        # Verificar si hay usuario autenticado para mostrar favoritos
        user_id = None
        from flask import request
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            try:
                user, auth_error = require_auth()
                if not auth_error and user:
                    user_id = user.get('public_user_id') or user.get('user_id')
            except Exception as e:
                pass  # Token inválido, continuar sin user_id
            
        site_data = get_site_by_id(site_id, user_id=user_id)
        
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


@bp.route("/", methods=["POST"])
@bp.route("", methods=["POST"])
def create_site_endpoint():
    """Crea un nuevo sitio histórico."""
    try:
        # Verificar autenticación
        user, auth_error = require_auth()
        if auth_error:
            return auth_error
        
        user_id = user['user_id']
        
        # Validar datos usando schema
        schema = SiteCreateSchema()
        try:
            site_data = schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({
                "error": {
                    "code": "invalid_data",
                    "message": "Invalid input data",
                    "details": err.messages
                }
            }), 400
        
        # Crear sitio
        new_site = create_site(site_data, user_id)
        
        # Serializar respuesta
        response_schema = SiteResponseSchema()
        response_data = response_schema.dump(new_site)
        response_data['user_id'] = user_id
        
        return jsonify(response_data), 201
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500