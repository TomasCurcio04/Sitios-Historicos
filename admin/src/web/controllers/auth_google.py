import base64
from flask import Blueprint, json, make_response, redirect, url_for, session, render_template, request
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

    user_cookie = {
        "id": userinfo.get("sub"),
        "email": userinfo.get("email"),
        "name": userinfo.get("name"),
        "picture": userinfo.get("picture")
    }
    
    next_url = request.args.get('state') or '/'
    res = make_response(redirect(next_url))
    
    res.set_cookie(
        'user_info',
        value=base64.b64encode(json.dumps(user_cookie).encode()).decode(),
        httponly=True,
        secure=True,  
        samesite='Lax',
        max_age=60*30
    )

    return res

@bp.route("/logout")
def logout():
    next_url = request.args.get("next", "/")
    resp = make_response(redirect(next_url))
    resp.delete_cookie('user_info')
    return resp
