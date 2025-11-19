"""Controlador de feature flags para la API"""

from flask import Blueprint, jsonify
from src.core.services.auth.feature_flag_serv import get_feature_flag

bp = Blueprint("api_feature_flags", __name__, url_prefix="/api/feature-flags")


@bp.route("/test", methods=["GET"])
def test_endpoint():
    """Test endpoint to verify API is working."""
    response = jsonify({"status": "ok", "message": "API is working"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@bp.route("/portal-status", methods=["GET"])
def get_portal_status():
    """Obtiene el estado del portal público."""
    try:
        portal_flag = get_feature_flag("portal_maintenance_mode")

        response_data = {
            "enabled": True if not portal_flag else not portal_flag.enabled,
            "maintenance_message": (
                portal_flag.maintenance_message
                if portal_flag and portal_flag.enabled
                else None
            ),
        }

        response = jsonify(response_data)
        return response

    except Exception as e:
        error_response = jsonify(
            {
                "error": {
                    "code": "server_error",
                    "message": "An unexpected error occurred",
                }
            }
        )
        error_response.headers.add("Access-Control-Allow-Origin", "*")
        return error_response, 500


@bp.route("/reviews-status", methods=["GET"])
def get_reviews_status():
    """Obtiene el estado de las reseñas."""
    try:
        reviews_flag = get_feature_flag("reviews_enabled")

        if not reviews_flag:
            return jsonify({"enabled": True})

        return jsonify({"enabled": reviews_flag.enabled})

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
