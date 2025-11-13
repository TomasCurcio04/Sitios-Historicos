"""Controlador de sitios de la API"""

import json
from flask import Blueprint, Response, request
from api.services.site_serv.utils_site import all_sites_to_json

bp = Blueprint("api_sites", __name__, url_prefix="/api/sites")


@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def all_sites():
    """Retorna sitios con filtros."""
    # Obtener parámetros de la URL
    params = {
        'name': request.args.get('name'),
        'description': request.args.get('description'),
        'city': request.args.get('city'),
        'province': request.args.get('province'),
        'tags': request.args.get('tags'),
        'order_by': request.args.get('order_by'),
        'lat': float(request.args.get('lat')) if request.args.get('lat') else None,
        'long': float(request.args.get('long')) if request.args.get('long') else None,
        'radius': float(request.args.get('radius')) if request.args.get('radius') else None,
        'page': int(request.args.get('page', 1)),
        'per_page': min(int(request.args.get('per_page', 20)), 100)
    }
    
    sites = all_sites_to_json(**params)
    json_str = json.dumps(sites, ensure_ascii=False)
    return Response(json_str, mimetype='application/json')
