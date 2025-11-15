"""Controlador de sitios de la API"""

import json
from flask import Blueprint, Response, request, jsonify
from api.services.site_serv.utils_site import all_sites_to_json

bp = Blueprint("api_sites", __name__, url_prefix="/api/sites")


@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def all_sites():
    """Retorna sitios con filtros."""
    try:
        # Validar y obtener parámetros
        params = {}
        
        # Parámetros de texto
        params['name'] = request.args.get('name')
        params['description'] = request.args.get('description')
        params['city'] = request.args.get('city')
        params['province'] = request.args.get('province')
        params['tags'] = request.args.get('tags')
        params['order_by'] = request.args.get('order_by')
        params['conservation_state'] = request.args.get('conservation_state')
        params['search'] = request.args.get('search')  # Búsqueda general por texto
        
        # Validar coordenadas
        errors = {}
        if request.args.get('lat'):
            try:
                lat = float(request.args.get('lat'))
                if not -90 <= lat <= 90:
                    errors['lat'] = ['Must be a valid latitude']
                else:
                    params['lat'] = lat
            except ValueError:
                errors['lat'] = ['Must be a valid latitude']
        
        if request.args.get('long'):
            try:
                long = float(request.args.get('long'))
                if not -180 <= long <= 180:
                    errors['long'] = ['Must be a valid longitude']
                else:
                    params['long'] = long
            except ValueError:
                errors['long'] = ['Must be a valid longitude']
        
        if request.args.get('radius'):
            try:
                params['radius'] = float(request.args.get('radius'))
            except ValueError:
                errors['radius'] = ['Must be a valid number']
        
        # Validar paginación
        try:
            params['page'] = int(request.args.get('page', 1))
            if params['page'] < 1:
                errors['page'] = ['Must be at least 1']
        except ValueError:
            errors['page'] = ['Must be a valid number']
        
        try:
            per_page = int(request.args.get('per_page', 20))
            if not 1 <= per_page <= 100:
                errors['per_page'] = ['Must be between 1 and 100']
            else:
                params['per_page'] = per_page
        except ValueError:
            errors['per_page'] = ['Must be between 1 and 100']
        
        # Validar order_by
        valid_orders = ['rating-5-1', 'rating-1-5', 'latest', 'oldest', 'name-asc', 'name-desc']
        if params['order_by'] and params['order_by'] not in valid_orders:
            errors['order_by'] = [f'Must be one of: {", ".join(valid_orders)}']
        
        if errors:
            return jsonify({
                "error": {
                    "code": "invalid_query",
                    "message": "Parameter validation failed",
                    "details": errors
                }
            }), 400
        
        sites = all_sites_to_json(**params)
        return jsonify(sites)
        
    except Exception as e:
        # Log temporal para debuggear
        print(f"Error en API sites: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "error": {
                "code": "server_error",
                "message": "An unexpected error occurred"
            }
        }), 500
