"""Controlador para endpoints del usuario autenticado (/me)"""

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.web.schemas.sites import SiteQuerySchema, SitesListResponseSchema
from src.core.services.board.site_favorites import get_user_favorites
from src.web.api.services.site_serv.utils_site import site_to_dict
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

        # Obtener reseñas del usuario
        from src.core.entity.review import Review
        from src.core.database import db

        query = (
            db.session.query(Review)
            .filter(Review.id_public_user == public_user_id)
            .order_by(Review.date_created.desc())
        )

        # Paginación
        page = params.get("page", 1)
        per_page = params.get("per_page", 20)
        total = query.count()
        reviews = query.offset((page - 1) * per_page).limit(per_page).all()

        # Convertir a formato API
        from src.web.api.services.review_serv.utils_review import review_to_dict

        reviews_data = [review_to_dict(review, None) for review in reviews]

        # Agregar información del sitio y estado
        for i, review in enumerate(reviews):
            reviews_data[i]["status"] = review.status.value
            reviews_data[i]["site_name"] = (
                review.site_rel.name if review.site_rel else None
            )

        response_data = {
            "data": reviews_data,
            "meta": {"page": page, "per_page": per_page, "total": total},
        }

        return jsonify(response_data)

    except Exception as e:
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

    except Exception as e:
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
