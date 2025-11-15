from flask import Blueprint, redirect, url_for, session, render_template
from admin.src.core.services.auth.user_serv import buscar_usuario_public, crear_user_public
from admin.src.web.oauth import oauth


bp = Blueprint("google_auth", __name__, url_prefix="/google")

@bp.route("/")
def google_login():
    user = session.get("user")
    return render_template("google_login.html", user=user)

@bp.route("/login")
def login():
    redirect_uri = url_for("google_auth.auth", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@bp.route("/login/callback")
def auth():
    token = oauth.google.authorize_access_token()
    userinfo = token["userinfo"]
    email = userinfo.get("email")

    print("email:", email)
    user  = buscar_usuario_public(email)
    print("user:", user)
    if not user:
        crear_user_public(
            google_id = userinfo.get("sub"),
            email=userinfo.get("email"),
            name = userinfo.get("name"),
            picture = userinfo.get("picture")
        )
    
    session['user'] = {
        "id": userinfo.get("sub"),
        "email": userinfo.get("email"),
        "name": userinfo.get("name"),
        "picture": userinfo.get("picture")
    }

    return redirect("http://localhost:5173/")
    
@bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect('/')