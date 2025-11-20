"""Controlador de autenticación para la API"""

from flask import Blueprint, jsonify, session, current_app, request
import jwt
from datetime import datetime, timedelta

bp = Blueprint("api_auth", __name__, url_prefix="/api/auth")


@bp.route("/token", methods=["POST"])
def get_token():
    """Obtiene token JWT desde sesión de Google OAuth."""
    print("🔑 [TOKEN] Iniciando get_token")
    print(f"🔑 [TOKEN] Request method: {request.method}")
    print(f"🔑 [TOKEN] Request headers: {dict(request.headers)}")

    user = session.get("user")
    print(f"🔑 [TOKEN] Session user: {user}")
    print(f"🔑 [TOKEN] Session keys: {list(session.keys())}")

    if not user:
        print("❌ [TOKEN] No user in session")
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

    print(f"🔑 [TOKEN] User ID: {user.get('id')}")
    print(f"🔑 [TOKEN] User email: {user.get('email')}")
    print(f"🔑 [TOKEN] User name: {user.get('name')}")

    payload = {
        "public_user_id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    print(f"🔑 [TOKEN] JWT payload: {payload}")

    jwt_secret = current_app.config["JWT_SECRET_KEY"]
    print(f"🔑 [TOKEN] JWT_SECRET_KEY exists: {bool(jwt_secret)}")
    print(f"🔑 [TOKEN] JWT_SECRET_KEY length: {len(jwt_secret) if jwt_secret else 0}")

    try:
        token = jwt.encode(payload, jwt_secret, algorithm="HS256")
        print(f"🔑 [TOKEN] Token generated successfully")
        print(f"🔑 [TOKEN] Token length: {len(token)}")
        print(f"🔑 [TOKEN] Token preview: {token[:50]}...")

        response_data = {"access_token": token, "token_type": "Bearer"}
        print(f"🔑 [TOKEN] Response data: {response_data}")

        return jsonify(response_data)
    except Exception as e:
        print(f"❌ [TOKEN] Error generating token: {str(e)}")
        print(f"❌ [TOKEN] Error type: {type(e)}")
        return (
            jsonify({"error": {"code": "token_generation_error", "message": str(e)}}),
            500,
        )
