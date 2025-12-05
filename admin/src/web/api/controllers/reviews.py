"""Controlador de reseñas de la API"""

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.reviews import (
    ReviewQuerySchema,
    ReviewsListResponseSchema,
    ReviewResponseSchema,
    ReviewCreateSchema,
)
from src.web.api.services.site_serv.utils_site import get_site_by_id
from src.web.api.services.review_serv.utils_review import (
    get_reviews_by_site,
    create_review,
    get_review_by_id,
    delete_review,
    update_review,
)
from src.web.api.utils.auth import require_auth

bp = Blueprint("api_reviews", __name__, url_prefix="/api/sites")


@bp.route("/<int:site_id>/reviews", methods=["GET"])
def get_site_reviews(site_id):
    """Obtiene reseñas de un sitio específico."""
    try:

        # Verificar que el sitio existe
        site_data = get_site_by_id(site_id)
        if not site_data:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        # Validar parámetros usando schema
        schema = ReviewQuerySchema()
        try:
            params = schema.load(request.args)
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

        # Obtener reseñas
        reviews_data = get_reviews_by_site(site_id, **params)

        # Serializar respuesta usando schema
        response_schema = ReviewsListResponseSchema()
        return jsonify(response_schema.dump(reviews_data))

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


@bp.route("/<int:site_id>/reviews", methods=["POST"])
def create_site_review(site_id):
    """Crea una nueva reseña para un sitio específico."""
    try:
        # Verificar autenticación
        user, auth_error = require_auth()
        if auth_error:
            return auth_error

        public_user_id = user["public_user_id"]

        # Verificar que el sitio existe
        site_data = get_site_by_id(site_id)
        if not site_data:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        # Validar datos usando schema
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

        # Crear reseña
        try:
            new_review = create_review(site_id, review_data, public_user_id)
        except ValueError as e:
            return (
                jsonify(
                    {
                        "error": {
                            "code": "conflict",
                            "message": str(e)
                        }
                    }
                ),
                409,
            )

        # Serializar respuesta
        response_schema = ReviewResponseSchema()
        return jsonify(response_schema.dump(new_review)), 201

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


@bp.route("/<int:site_id>/reviews/<int:review_id>", methods=["GET"])
def get_site_review(site_id, review_id):
    """Obtiene una reseña específica por ID."""
    try:
        # TODO: Implementar autenticación JWT cuando esté disponible
        # Placeholder: permitir acceso sin autenticación por ahora

        # Verificar que el sitio existe
        site_data = get_site_by_id(site_id)
        if not site_data:
            return (
                jsonify({"error": {"code": "not_found", "message": "Site not found"}}),
                404,
            )

        # Obtener reseña (incluir pendientes para que el usuario vea su propia reseña)
        review_data = get_review_by_id(review_id, site_id, include_pending=True)

        if not review_data:
            return (
                jsonify(
                    {"error": {"code": "not_found", "message": "Review not found"}}
                ),
                404,
            )

        # Serializar respuesta
        response_schema = ReviewResponseSchema()
        return jsonify(response_schema.dump(review_data))

    except Exception as e:
        print(f"ERROR en get_site_review: {str(e)}")
        import traceback

        traceback.print_exc()
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


@bp.route("/<int:site_id>/reviews/<int:review_id>", methods=["PUT"])
def update_site_review(site_id, review_id):
    """Actualiza una reseña específica."""
    try:
        # Verificar autenticación
        user, auth_error = require_auth()
        if auth_error:
            return auth_error

        public_user_id = user["public_user_id"]

        # Validar datos usando schema
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


@bp.route("/<int:site_id>/reviews/<int:review_id>", methods=["DELETE"])
def delete_site_review(site_id, review_id):
    """Elimina una reseña específica por ID."""
    try:
        # Verificar autenticación
        user, auth_error = require_auth()
        if auth_error:
            return auth_error

        public_user_id = user["public_user_id"]

        # Eliminar reseña (con validación de usuario)
        success = delete_review(review_id, site_id, public_user_id)

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
