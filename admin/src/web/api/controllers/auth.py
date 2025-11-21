"""Controlador de autenticación para la API"""

from flask import Blueprint, jsonify, session, current_app, request
import jwt
from datetime import datetime, timedelta

bp = Blueprint("api_auth", __name__, url_prefix="/api/auth")


@bp.route("/token", methods=["POST"])
def get_token():
    """Obtiene token JWT desde sesión de Google OAuth."""
    user = session.get("user")
    if not user:
        return (
            jsonify(
                {
                    "error": {
                        "code": "unauthorized",
                        "message": "No authenticated session found",
                    }
                }
            ),
            401,
        )

    payload = {
        "public_user_id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

    return jsonify({"access_token": token, "token_type": "Bearer"})
