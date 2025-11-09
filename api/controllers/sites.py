"""Controlador de sitios de la API"""

from flask import Blueprint, jsonify
from api.services.site_serv import all_sites_to_json

bp = Blueprint("api_sites", __name__, url_prefix="/api/sites")


@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def all_sites():
    """Retorna todos los sitios."""
    # Respuesta temporal para probar que funciona
    sites = all_sites_to_json()
    print(sites)
    return (
        sites,
        200,
    )
