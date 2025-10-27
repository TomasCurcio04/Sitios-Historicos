# src/core/site_history_serv/__init__.py

"""
Capa de Servicio para gestionar la lógica de negocio
del historial de sitios (SiteHistory).
"""
from src.core.database import db # O desde donde importes tu sesión de DB
from src.core.entity.site_history import SiteHistory
from src.core.entity.site import Site
from src.core.entity.state import State


class SiteHistoryService:
    """Encapsula la lógica para crear registros de historial."""

    @staticmethod
    def register_creation(db_session, *, site: Site, user_id: int):
        """
        Crea un registro de historial para la CREACIÓN de un sitio.
        """
        # Esta lógica estaba antes en tu controlador
        estado = db_session.get(State, site.state)
        detalle = f"Sitio '{site.name}' creado en {site.city}, {estado.name if estado else 'N/A'}"
        
        creation_record = SiteHistory(
            id_site=site.id_site,
            id_user=user_id,
            action_type="CREATE",
            action_detail=detalle
        )
        db_session.add(creation_record)

    @staticmethod
    def register_update(db_session, *, site_id: int, user_id: int, changes: list[str]):
        """
        Crea un registro de historial para la ACTUALIZACIÓN de un sitio.
        """
        if not changes:
            return # No hacer nada si no hay cambios

        # Esta lógica estaba antes en tu controlador
        detalle_cambios = "\n".join(changes)
        update_record = SiteHistory(
            id_site=site_id,
            id_user=user_id,
            action_type="UPDATE",
            action_detail=detalle_cambios
        )
        db_session.add(update_record)

    @staticmethod
    def register_deletion(db_session, *, site: Site, user_id: int):
        """
        Crea un registro de historial para la ELIMINACIÓN de un sitio.
        """
        # Esta lógica estaba antes en tu controlador
        detalle = f"Sitio '{site.name}' eliminado (estaba en {site.city})"
        delete_record = SiteHistory(
            id_site=site.id_site,
            id_user=user_id,
            action_type="DELETE",
            action_detail=detalle
        )
        db_session.add(delete_record)