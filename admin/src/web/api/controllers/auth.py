"""Controlador de autenticación para la API"""

from flask import Blueprint, jsonify, session, current_app, request, redirect, url_for
import jwt
from datetime import datetime, timedelta
from src.core.services.auth.user_serv import buscar_usuario_public, crear_user_public
from src.web.oauth import oauth

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


@bp.route("/google/login")
def google_login():
    """Iniciar login con Google."""
    session['next'] = request.args.get('next') or request.referrer
    redirect_uri = url_for("api_auth.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route("/google/callback")
def google_callback():
    """Callback de Google OAuth."""
    token = oauth.google.authorize_access_token()
    userinfo = token["userinfo"]
    email = userinfo.get("email")

    user = buscar_usuario_public(email)
    if not user:
        crear_user_public(
            google_id=userinfo.get("sub"),
            email=userinfo.get("email"),
            name=userinfo.get("name"),
            picture=userinfo.get("picture")
        )
    
    session['user'] = {
        "id": userinfo.get("sub"),
        "email": userinfo.get("email"),
        "name": userinfo.get("name"),
        "picture": userinfo.get("picture"),
        "type": "google"
    }
    
    next_url = session.get('next') or '/'
    return redirect(next_url)


@bp.route("/google/logout")
def google_logout():
    """Logout de Google."""
    session.pop("user", None)
    next_url = request.args.get("next", "/")
    return redirect(next_url)


@bp.route("/google/status")
def google_status():
    """Estado de autenticación."""
    user = session.get("user")
    return jsonify({"logged_in": bool(user), "user": user})
