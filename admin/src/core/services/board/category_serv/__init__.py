"""Capa de servicios de categorias"""

from src.core.database import db
from src.core.entity.category import Category


def list_all_categories():
    """
    Lista todas las categorias existentes
    Args: None
    Return: List(Category)
    """
    return db.session.query(Category).all()


def get_category_by_id(category_id):
    """
    Obtiene una categoria por su id
    Args:
        category_id (int): id de la categoria
    Return: Category
    """
    return db.session.query(Category).get(category_id) or None
