"""Controlador de autenticación para la API"""

from datetime import datetime, timedelta
import base64
import json
from flask import Blueprint, jsonify, current_app, request
import jwt

bp = Blueprint("api_auth", __name__, url_prefix="/api/auth")


@bp.route("/token", methods=["POST"])
def get_token():
    """Obtiene token JWT desde sesión de Google OAuth."""
    user = request.cookies.get("user_info")
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

    user_data = json.loads(base64.b64decode(user).decode())

    payload = {
        "public_user_id": user_data["id"],
        "email": user_data["email"],
        "name": user_data["name"],
        "picture": user_data["picture"],
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

    return jsonify({"access_token": token, "token_type": "Bearer"})
