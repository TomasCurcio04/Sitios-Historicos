import csv
import io
from datetime import datetime

from src.core.services.board.tag_serv import listar_tags_por_id
from src.core.services.board.busqueda_avanzada_serv import buscar_sites, ordenar_lista
from src.core.services.board.sites import obtener_sitio_id

def exportar_sites_csv(filtros=None,sort=None,order="asc"):
    """Exporta sitios a un archivo CSV según los filtros y orden especificados.

    Args:
        filtros (dict, optional): Diccionario con los filtros de búsqueda. Defaults to None.
        sort (str, optional): Campo por el cual ordenar. Defaults to None.
        order (str, optional): Orden de la ordenación ('asc' o 'desc'). Defaults to "asc".

    Returns:
        str: Contenido del archivo CSV como cadena.
    """
    filtros = filtros or {}

    sitios = buscar_sites(filtros)
    
    # Ordenar sitios si se especifica
    if sort:
        sitios = ordenar_lista(sitios, sort, order)

    # Crear archivo CSV en memoria
    output = io.StringIO()
    output.write("\ufeff") 

    writer = csv.writer(output, delimiter=",", quoting=csv.QUOTE_ALL)

    # Escribir encabezados
    writer.writerow([
        "ID",
        "Nombre",
        "Descripcion breve",
        "Ciudad",
        "Provincia",
        "Estado de Conservación",
        "Fecha de Registro",
        "Latitud",
        "Longitud",
        "Tags",
    ])

    # Escribir datos de los sitios
    for site in sitios:
        
        site_db = obtener_sitio_id(site.get("id"))
        tag_ids = site.get("tags", [])
        nombres_tags = listar_tags_por_id(set(tag_ids)) if tag_ids else []
        tags = " | ".join(nombres_tags)

        writer.writerow([
            site.get("id", ""),
            site.get("name", ""),
            site_db.short_description if site_db else "",
            site.get("city", ""),
            site.get("state", ""),
            site.get("conservation_state", ""),
            site.get("date_registered", ""),
            site_db.latitude if site_db else "",
            site_db.longitude if site_db else "",
            tags,
        ])

    output.seek(0)

    nombre_archivo = f"sitios_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

    return output.getvalue(), nombre_archivo