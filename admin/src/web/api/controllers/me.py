"""Controlador para endpoints del usuario autenticado (/me)"""

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.sites import SiteQuerySchema, SitesListResponseSchema
from src.core.services.board.site_favorites import get_user_favorites
from src.web.api.services.site_serv.utils_site import site_to_dict
from src.web.api.services.me_serv import obtener_reviews_de_usuario
from src.web.api.services.review_serv.utils_review import delete_review, update_review
from src.web.api.utils.auth import require_auth

bp = Blueprint("api_me", __name__, url_prefix="/api/me")


@bp.route("/reviews", methods=["GET"])
def get_my_reviews():
    """Lista todas las reseñas del usuario autenticado (aprobadas, pendientes, rechazadas)."""
    try:
        # Verificar autenticación
        user, auth_error = require_auth()
        if auth_error:
            return auth_error

        public_user_id = user["public_user_id"]

        # Validar parámetros de paginación
        schema = SiteQuerySchema()
        try:
            params = schema.load(request.args)
        except ValidationError as err:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "invalid_query",
                            "message": "Parameter validation failed",
                            "details": err.messages,
                        }
                    }
                ),
                400,
            )

        # Obtener reseñas del usuario usando el servicio
        reviews_result = obtener_reviews_de_usuario(
            public_user_id,
            page=params.get("page", 1),
            per_page=params.get("per_page", 20)
        )
        
        reviews_data = reviews_result["items"]
        total = reviews_result["total"]

        response_data = {
            "data": reviews_data,
            "meta": {
                "page": params.get("page", 1), 
                "per_page": params.get("per_page", 20), 
                "total": total
            },
        }

        return jsonify(response_data)

    except Exception:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp.route("/favorites", methods=["GET"])
def get_my_favorites():
    """Lista los sitios favoritos del usuario autenticado."""
    try:
        # Verificar autenticación
        user, auth_error = require_auth()
        if auth_error:
            return auth_error

        public_user_id = user["public_user_id"]

        # Validar parámetros de paginación
        schema = SiteQuerySchema()
        try:
            params = schema.load(request.args)
        except ValidationError as err:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "invalid_query",
                            "message": "Parameter validation failed",
                            "details": err.messages,
                        }
                    }
                ),
                400,
            )

        # Obtener favoritos del usuario
        favorites_result = get_user_favorites(
            public_user_id,
            page=params.get("page", 1),
            per_page=params.get("per_page", 20),
        )

        # Convertir sitios favoritos a formato API
        sites_data = []
        for favorite in favorites_result["items"]:
            site_dict = site_to_dict(favorite.site_rel)
            sites_data.append(site_dict)

        # Respuesta en formato estándar
        response_data = {
            "data": sites_data,
            "meta": {
                "page": favorites_result["page"],
                "per_page": favorites_result["per_page"],
                "total": favorites_result["total"],
            },
        }

        # Serializar respuesta
        response_schema = SitesListResponseSchema()
        return jsonify(response_schema.dump(response_data))

    except Exception:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_my_review(review_id):
    """Elimina una reseña del usuario autenticado."""
    try:
        # Verificar autenticación
        user, auth_error = require_auth()
        if auth_error:
            return auth_error

        public_user_id = user["public_user_id"]

        # Eliminar reseña (con validación de usuario)
        success = delete_review(review_id, None, public_user_id)

        if not success:
            return (
                jsonify(
                    {"error": {"code": "not_found", "message": "Review not found or you don't have permission to delete it"}}
                ),
                404,
            )

        return "", 204

    except Exception:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp.route("/reviews/<int:review_id>", methods=["PUT"])
def update_my_review(review_id):
    """Actualiza una reseña del usuario autenticado."""
    try:
        # Verificar autenticación
        user, auth_error = require_auth()
        if auth_error:
            return auth_error

        public_user_id = user["public_user_id"]

        # Validar datos usando schema
        from src.web.schemas.reviews import ReviewCreateSchema
        schema = ReviewCreateSchema()
        try:
            review_data = schema.load(request.get_json())
        except ValidationError as err:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "invalid_data",
                            "message": "Invalid input data",
                            "details": err.messages,
                        }
                    }
                ),
                400,
            )

        # Actualizar reseña
        try:
            updated_review = update_review(review_id, review_data, public_user_id)
        except ValueError as e:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "forbidden",
                            "message": str(e)
                        }
                    }
                ),
                403,
            )

        # Serializar respuesta
        from src.web.schemas.reviews import ReviewResponseSchema
        response_schema = ReviewResponseSchema()
        return jsonify(response_schema.dump(updated_review))

    except Exception:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )