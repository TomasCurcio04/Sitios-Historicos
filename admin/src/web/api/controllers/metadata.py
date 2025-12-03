"""Controlador de metadatos para la API"""

from flask import Blueprint, jsonify
from src.core.database import db
from src.core.entity.state import State
from src.core.entity.tag import Tag
from src.core.entity.category import Category

bp = Blueprint("api_metadata", __name__, url_prefix="/api/metadata")


@bp.route("/states", methods=["GET"])
def get_states():
    """Obtiene todos los estados/provincias disponibles."""
    try:
        states = db.session.query(State).order_by(State.name).all()

        data = [{"id": state.id_state, "name": state.name} for state in states]

        return jsonify(data)

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp.route("/tags", methods=["GET"])
def get_tags():
    """Obtiene todos los tags disponibles."""
    try:
        tags = db.session.query(Tag).order_by(Tag.name).all()

        data = [{"id": tag.id_tag, "name": tag.name} for tag in tags]

        return jsonify(data)

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )


@bp.route("/categories", methods=["GET"])
def get_categories():
    """Obtiene todas las categorías disponibles."""
    try:
        categories = db.session.query(Category).order_by(Category.name).all()

        data = [
            {"id": category.id_category, "name": category.name}
            for category in categories
        ]

        return jsonify(data)

    except Exception as e:
        return (
            jsonify(
                {
                    "error": {
                        "code": "server_error",
                        "message": "An unexpected error occurred",
                    }
                }
            ),
            500,
        )
