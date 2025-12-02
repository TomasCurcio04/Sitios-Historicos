from flask import Blueprint, redirect, url_for, session, render_template, request
from src.core.services.auth.user_serv import buscar_usuario_public, crear_user_public
from src.web.oauth import oauth
from flask import current_app
import jwt


bp = Blueprint("google_auth", __name__, url_prefix="/google")

@bp.route("/login")
def login():
    next_url = request.args.get('next') or request.referrer or '/'

    redirect_uri = url_for("google_auth.auth", _external=True)
    print("Redirect URI:", url_for("google_auth.auth", _external=True))
    return oauth.google.authorize_redirect(
        redirect_uri,
        prompt="select_account",
        state=next_url
    )

@bp.route("/login/callback")
def auth():
    token = oauth.google.authorize_access_token()
    userinfo = token["userinfo"]
    email = userinfo.get("email")

    user = buscar_usuario_public(email)
    if not user:
        crear_user_public(
            google_id = userinfo.get("sub"),
            email=userinfo.get("email"),
            name = userinfo.get("name"),
            picture = userinfo.get("picture")
        )
    
    playload = {
        "public_user_id": userinfo.get("sub"),
        "email": userinfo.get("email"),
        "name": userinfo.get("name"),
        "picture": userinfo.get("picture")
    }
    jwt_token = jwt.encode(playload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

    next_url = request.args.get('state') or '/'
    separator = '&' if '?' in next_url else '?'
    return redirect(f"{next_url}{separator}auth_token={jwt_token}")
    
@bp.route("/logout")
def logout():
    next_url = request.args.get("next", "/")
    return redirect(next_url)
