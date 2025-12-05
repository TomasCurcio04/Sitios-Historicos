# src/core/site_history_serv/__init__.py

"""
Capa de Servicio para gestionar la lógica de negocio
del historial de sitios (SiteHistory).
"""
from src.core.database import db  # O desde donde importes tu sesión de DB
from src.core.entity.site_history import SiteHistory
from src.core.entity.site import Site
from src.core.entity.state import State
from src.core.entity.category import Category
from src.core.entity.tag import Tag
from src.core.services.board.category_serv import get_category_by_id
from src.core.services.board.tag_serv import listar_tags_por_id


def register_modify(site, user_id, action_type, action_detail):
    """Crea un registro de historial del sitio modificado.

    Args:
        site (Site): Sitio afectado
        user_id (int): ID del usuario que realizó la acción.
        action_type (str): Tipo de acción realizada. Puede ser "CREATE", "UPDATE" o "DELETE".

    Returns:
        None
    """
    new_history = SiteHistory(
        id_site=site.id_site,
        id_user=user_id,
        action_type=action_type,
        action_detail=action_detail,
    )
    db.session.add(new_history)
    db.session.commit()


def detect_changes(site, nuevos_datos, nuevas_tags):
    """Compara el sitio actual con los nuevos datos y devuelve una lista de cambios detectados.

    Args:
        site (Site): Objeto Site con los datos actuales.
        nuevos_datos (dict): Diccionario con los nuevos valores a comparar.
        nuevas_tags (list[Tag]): Lista de Tag que se quieren asignar.

    Nota: Diccionario nuevos_datos:
        "name"
        "short_description"
        "full_description"
        "city"
        "state"
        "latitude"
        "longitude"
        "conservation_state"
        "inauguration_year"
        "category"
        "is_visible"
    Returns:
        list[str]: Lista de strings describiendo cada campo con cambios detectado.
    """
    cambios_detectados = []

    if site.name != nuevos_datos.get("name"):
        cambios_detectados.append(
            f"Nombre: '{site.name}' -> '{nuevos_datos.get("name")}'"
        )

    if site.short_description != nuevos_datos.get("short_description"):
        cambios_detectados.append(
            f"Descripción breve: '{site.short_description}' -> "
            f"'{nuevos_datos.get("short_description")}'"
        )

    if site.full_description != nuevos_datos.get("full_description"):
        cambios_detectados.append(
            f"Descripción completa: '{site.full_description}' -> "
            f"'{nuevos_datos.get("full_description")}'"
        )

    if site.city != nuevos_datos.get("city"):
        cambios_detectados.append(
            f"Ciudad: '{site.city}' -> '{nuevos_datos.get("city")}'"
        )

    if site.state != nuevos_datos.get("state"):
        cambios_detectados.append(
            f"Provincia: '{site.state}' -> '{nuevos_datos.get("state")}'"
        )

    lat_nueva = (
        float(nuevos_datos.get("latitude")) if nuevos_datos.get("latitude") else None
    )
    if (site.latitude and float(site.latitude)) != lat_nueva:
        cambios_detectados.append(f"Latitud: {site.latitude} → {lat_nueva}")

    lon_nueva = (
        float(nuevos_datos.get("longitude")) if nuevos_datos.get("longitude") else None
    )
    if (site.longitude and float(site.longitude)) != lon_nueva:
        cambios_detectados.append(f"Longitud: {site.longitude} → {lon_nueva}")

    if site.conservation_state != nuevos_datos.get("conservation_state"):
        cambios_detectados.append(
            f"Estado conservación: '{site.conservation_state or 'N/A'}' → "
            f"'{nuevos_datos.get('conservation_state') or 'N/A'}'"
        )

    if site.inauguration_year != nuevos_datos.get("inauguration_year"):
        cambios_detectados.append(
            f"Año inauguración: {site.inauguration_year or 'N/A'} → "
            f"{nuevos_datos.get('inauguration_year') or 'N/A'}"
        )

    if site.category != nuevos_datos.get("category"):
        cat_vieja = get_category_by_id(site.category)
        cat_nueva = get_category_by_id(nuevos_datos.get("category"))
        cambios_detectados.append(
            f"Categoría: '{cat_vieja.name if cat_vieja else 'N/A'}' → "
            f"'{cat_nueva.name if cat_nueva else 'N/A'}'"
        )

    if site.is_visible != nuevos_datos.get("is_visible"):
        cambios_detectados.append(
            f"Visibilidad: {is_visible(site.is_visible)} → "
            f"{is_visible(nuevos_datos.get('is_visible'))}"
        )

    # Comparar etiquetas
    tags_actuales = {tag.id_tag for tag in site.tag}
    tags_nuevos = {tag.id_tag for tag in nuevas_tags}

    if tags_actuales != tags_nuevos:
        tags_agregados = tags_nuevos - tags_actuales
        tags_eliminados = tags_actuales - tags_nuevos

        if tags_agregados:
            nombres = listar_tags_por_id(tags_agregados)
            cambios_detectados.append(f"Etiquetas agregadas: {', '.join(nombres)}")

        if tags_eliminados:
            nombres = listar_tags_por_id(tags_eliminados)
            cambios_detectados.append(f"Etiquetas eliminadas: {', '.join(nombres)}")

    return cambios_detectados


def is_visible(booleano):
    """Funcion auxiliar para transformar true en Visible y false en Oculto
    Args: booleano(boolean)
    Returns: string"""

    return "Visible" if booleano else "Oculto"


def obtener_historial_sitios(site_id, sort_by='date', order='desc'):
    """Obtiene el historial de modificaciones de un sitio específico.
    Args:
        site_id (int): ID del sitio.
        sort_by (str): Campo por el cual ordenar ('date', 'action', 'user').
        order (str): Orden ('asc' o 'desc').
    Returns:
        list[SiteHistory]: Lista de objetos SiteHistory ordenados.
    """
    from src.core.entity.users import Users
    
    query = db.session.query(SiteHistory).filter_by(id_site=site_id)
    
    # Aplicar ordenamiento
    if sort_by == 'action':
        order_field = SiteHistory.action_type
    elif sort_by == 'user':
        query = query.join(Users)
        order_field = Users.email
    else:  # default: date
        order_field = SiteHistory.date_action
    
    if order == 'asc':
        query = query.order_by(order_field.asc())
    else:
        query = query.order_by(order_field.desc())
    
    return query.all()
