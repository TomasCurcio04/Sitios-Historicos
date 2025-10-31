# src/core/site_history_serv/__init__.py

"""
Capa de Servicio para gestionar la lógica de negocio
del historial de sitios (SiteHistory).
"""
from src.core.database import db # O desde donde importes tu sesión de DB
from src.core.entity.site_history import SiteHistory
from src.core.entity.site import Site
from src.core.entity.state import State
from src.core.entity.category import Category
from src.core.entity.tag import Tag


class SiteHistoryService:
    """Encapsula la lógica para crear registros de historial."""

    @staticmethod
    def register_creation(db_session, *, site: Site, user_id: int):
        """Crea un registro de historial para la creación de un sitio.
        
        Args:
            db_session: Sesión de base de datos
            site: Sitio creado
            user_id: ID del usuario que creó el sitio
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
        """Crea un registro de historial para la actualización de un sitio.
        
        Args:
            db_session: Sesión de base de datos
            site_id: ID del sitio actualizado
            user_id: ID del usuario que actualizó el sitio
            changes: Lista de cambios realizados
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
        """Crea un registro de historial para la eliminación de un sitio.
        
        Args:
            db_session: Sesión de base de datos
            site: Sitio a eliminar
            user_id: ID del usuario que eliminó el sitio
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

    @staticmethod
    def detect_changes(db_session, *, site_actual: Site, nuevos_datos: dict, nuevas_tags: list[Tag]) -> list[str]:
        """Compara el sitio actual con los nuevos datos y devuelve una lista de cambios detectados."""
        cambios_detectados = []

        if site_actual.name != nuevos_datos.get("name"):
            cambios_detectados.append(f"Nombre: '{site_actual.name}' → '{nuevos_datos.get('name')}'")

        if site_actual.short_description != nuevos_datos.get("short_description"):
            cambios_detectados.append("Descripción breve modificada")

        if site_actual.full_description != nuevos_datos.get("full_description"):
            cambios_detectados.append("Descripción completa modificada")

        if site_actual.city != nuevos_datos.get("city"):
            cambios_detectados.append(f"Ciudad: '{site_actual.city}' → '{nuevos_datos.get('city')}'")

        if site_actual.state != nuevos_datos.get("state"):
            estado_viejo = db_session.get(State, site_actual.state)
            estado_nuevo = db_session.get(State, nuevos_datos.get("state"))
            cambios_detectados.append(
                f"Provincia: '{estado_viejo.name if estado_viejo else 'N/A'}' → '{estado_nuevo.name if estado_nuevo else 'N/A'}'"
            )

        lat_nueva = float(nuevos_datos.get("latitude")) if nuevos_datos.get("latitude") else None
        if (site_actual.latitude and float(site_actual.latitude)) != lat_nueva:
            cambios_detectados.append(f"Latitud: {site_actual.latitude} → {lat_nueva}")

        lon_nueva = float(nuevos_datos.get("longitude")) if nuevos_datos.get("longitude") else None
        if (site_actual.longitude and float(site_actual.longitude)) != lon_nueva:
            cambios_detectados.append(f"Longitud: {site_actual.longitude} → {lon_nueva}")

        if site_actual.conservation_state != nuevos_datos.get("conservation_state"):
            cambios_detectados.append(
                f"Estado conservación: '{site_actual.conservation_state or 'N/A'}' → '{nuevos_datos.get('conservation_state') or 'N/A'}'"
            )

        if site_actual.inauguration_year != nuevos_datos.get("inauguration_year"):
            cambios_detectados.append(
                f"Año inauguración: {site_actual.inauguration_year or 'N/A'} → {nuevos_datos.get('inauguration_year') or 'N/A'}"
            )

        if site_actual.category != nuevos_datos.get("category"):
            cat_vieja = db_session.get(Category, site_actual.category)
            cat_nueva = db_session.get(Category, nuevos_datos.get("category"))
            cambios_detectados.append(
                f"Categoría: '{cat_vieja.name if cat_vieja else 'N/A'}' → '{cat_nueva.name if cat_nueva else 'N/A'}'"
            )

        if site_actual.is_visible != nuevos_datos.get("is_visible"):
            cambios_detectados.append(
                f"Visibilidad: {'Visible' if site_actual.is_visible else 'Oculto'} → {'Visible' if nuevos_datos.get('is_visible') else 'Oculto'}"
            )

        # Comparar etiquetas
        tags_actuales = set([tag.id_tag for tag in site_actual.tag])
        tags_nuevos = set([tag.id_tag for tag in nuevas_tags])

        if tags_actuales != tags_nuevos:
            tags_agregados = tags_nuevos - tags_actuales
            tags_eliminados = tags_actuales - tags_nuevos

            if tags_agregados:
                nombres = [db_session.get(Tag, tid).name for tid in tags_agregados]
                cambios_detectados.append(f"Etiquetas agregadas: {', '.join(nombres)}")

            if tags_eliminados:
                nombres = [db_session.get(Tag, tid).name for tid in tags_eliminados]
                cambios_detectados.append(f"Etiquetas eliminadas: {', '.join(nombres)}")

        return cambios_detectados

