from flask import Blueprint, render_template

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/")
def login():
    return render_template("login.html")

@bp.get("/logout") 
def logout():
    pass

@bp.post("/authenticate")
def authenticate():
    pass