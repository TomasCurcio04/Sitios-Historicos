# src/core/board/__init__.py
"""Interfaz del módulo board que abstrae la fuente de datos."""


from src.core.board import repository

# API pública para sitios históricos
list_sites = repository.list_sites
get_site = repository.get_site
create_site = repository.create_site
update_site = repository.update_site
delete_site = repository.delete_site