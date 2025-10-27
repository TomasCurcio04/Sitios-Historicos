# src/core/board/board.py
"""Interfaz del módulo board que abstrae la fuente de datos."""

from src.core.board import list_sites, get_site, create_site, update_site, delete_site

# Re-exportar funciones
__all__ = ['list_sites', 'get_site', 'create_site', 'update_site', 'delete_site']