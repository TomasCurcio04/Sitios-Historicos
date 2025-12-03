"""Controlador de búsqueda estilo ZonaProp"""

from flask import Blueprint, request, jsonify
from src.web.api.services.search_basic import (
    search_sites_nearby_basic,
    search_sites_by_filters,
    site_to_search_result,
)

bp = Blueprint("api_search", __name__, url_prefix="/api/search")


@bp.route("/nearby", methods=["GET"])
def search_nearby():
    """Búsqueda por proximidad geográfica"""
    try:
        # Parámetros requeridos
        lat = float(request.args.get("lat"))
        lng = float(request.args.get("lng"))
        radius = float(request.args.get("radius", 10))  # Default 10km

        # Filtros opcionales
        filters = {
            "city": request.args.get("city"),
            "category_id": request.args.get("category_id", type=int),
            "state_id": request.args.get("state_id", type=int),
            "conservation_state": request.args.get("conservation_state"),
            "year_from": request.args.get("year_from", type=int),
            "year_to": request.args.get("year_to", type=int),
        }

        # Limpiar filtros vacíos
        filters = {k: v for k, v in filters.items() if v is not None}

        sites = search_sites_nearby_basic(lat, lng, radius, filters)
        results = [site_to_search_result(site) for site in sites]

        return jsonify({"success": True, "count": len(results), "results": results})

    except (TypeError, ValueError) as e:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Parámetros inválidos. Se requieren lat y lng.",
                }
            ),
            400,
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/filter", methods=["GET"])
def search_by_filters():
    """Búsqueda por filtros sin coordenadas"""
    try:
        filters = {
            "text": request.args.get("q"),  # Búsqueda de texto general
            "city": request.args.get("city"),
            "category_id": request.args.get("category_id", type=int),
            "state_id": request.args.get("state_id", type=int),
            "conservation_state": request.args.get("conservation_state"),
            "year_from": request.args.get("year_from", type=int),
            "year_to": request.args.get("year_to", type=int),
        }

        # Limpiar filtros vacíos
        filters = {k: v for k, v in filters.items() if v is not None}

        sites = search_sites_by_filters(filters)
        results = [site_to_search_result(site) for site in sites]

        return jsonify({"success": True, "count": len(results), "results": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@bp.route("/autocomplete/cities", methods=["GET"])
def autocomplete_cities():
    """Autocompletado de ciudades"""
    try:
        from src.core.database import db
        from src.core.entity.site import Site

        query = request.args.get("q", "").strip()

        if len(query) < 2:
            return jsonify([])

        cities = (
            db.session.query(Site.city)
            .filter(Site.city.ilike(f"%{query}%"))
            .distinct()
            .limit(10)
            .all()
        )

        return jsonify([city[0] for city in cities if city[0]])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
