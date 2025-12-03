"""Google OAuth2 Authentication Controller"""

from flask import Blueprint, redirect, url_for, session, render_template, request
from src.core.services.auth.user_serv import buscar_usuario_public, crear_user_public
from src.web.oauth import oauth


bp = Blueprint("google_auth", __name__, url_prefix="/google")


# Prueba despues de agregar google_id
@bp.route("/login")
def login():
    """Iniciar el flujo de autenticación de Google OAuth2.
    Args:
        None
    Returns:
        Redirige al usuario a la página de autorización de Google OAuth2.
    """
    session["next"] = request.args.get("next") or request.referrer
    redirect_uri = url_for("google_auth.auth", _external=True)

    print("Redirect URI:", url_for("google_auth.auth", _external=True))
    return oauth.google.authorize_redirect(redirect_uri, prompt="select_account")


@bp.route("/login/callback")
def auth():
    """Manejar el callback de Google OAuth2.
    Args:
        None
    Returns:
        Redirige al usuario a la URL original después de la autenticación.
    """
    token = oauth.google.authorize_access_token()
    userinfo = token["userinfo"]
    email = userinfo.get("email")

    user = buscar_usuario_public(email)
    if not user:
        crear_user_public(
            google_id=userinfo.get("sub"),
            email=userinfo.get("email"),
            name=userinfo.get("name"),
            picture=userinfo.get("picture"),
        )

    session["user"] = {
        "id": userinfo.get("sub"),
        "email": userinfo.get("email"),
        "name": userinfo.get("name"),
        "picture": userinfo.get("picture"),
        "type": "google",
    }
    next_url = session.get("next") or "/"
    return redirect(next_url)


@bp.route("/logout")
def logout():
    """Cerrar la sesión del usuario.
    Args:
        None
    Returns:
        Redirige al usuario a la página de inicio después de cerrar sesión.
    """
    session.pop("user", None)
    next_url = request.args.get("next", "/")
    return redirect(next_url)


@bp.route("/status")
def status():
    """Verificar el estado de autenticación del usuario.
    Args:
        None
    Returns:
        Un diccionario que indica si el usuario está autenticado y su información.
    """
    user = session.get("user")
    return {"logged_in": bool(user), "user": user}
