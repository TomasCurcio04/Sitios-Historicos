"""Controlador de reseñas de la API"""

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.reviews import ReviewQuerySchema, ReviewsListResponseSchema
from api.services.review_serv.utils_review import get_reviews_by_site

bp = Blueprint("api_reviews", __name__, url_prefix="/api/sites")


@bp.route("/<int:site_id>/reviews", methods=["GET"])
def get_site_reviews(site_id):
    """Obtiene reseñas de un sitio específico."""
    try:
        # Validar parámetros usando schema
        schema = ReviewQuerySchema()
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
        
        # Obtener reseñas
        reviews_data = get_reviews_by_site(site_id, **params)
        
        # Serializar respuesta usando schema
        response_schema = ReviewsListResponseSchema()
        return jsonify(response_schema.dump(reviews_data))
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500