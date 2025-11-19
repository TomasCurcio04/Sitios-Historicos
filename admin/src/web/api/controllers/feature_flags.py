"""Controlador de feature flags para la API"""

from flask import Blueprint, jsonify
from src.core.services.auth.feature_flag_serv import get_feature_flag

bp = Blueprint("api_feature_flags", __name__, url_prefix="/api/feature-flags")


@bp.route("/portal-status", methods=["GET"])
def get_portal_status():
    """Obtiene el estado del portal público."""
    try:
        portal_flag = get_feature_flag("portal_maintenance_mode")
        
        if not portal_flag:
            return jsonify({
                "enabled": True,
                "maintenance_message": None
            })
        
        return jsonify({
            "enabled": not portal_flag.enabled,  # Invertido: si maintenance está activo, portal está deshabilitado
            "maintenance_message": portal_flag.maintenance_message if portal_flag.enabled else None
        })
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500


@bp.route("/reviews-status", methods=["GET"])
def get_reviews_status():
    """Obtiene el estado de las reseñas."""
    try:
        reviews_flag = get_feature_flag("reviews_enabled")
        
        if not reviews_flag:
            return jsonify({"enabled": True})
        
        return jsonify({"enabled": reviews_flag.enabled})
        
    except Exception as e:
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500