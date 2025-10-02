from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime

bp = Blueprint('busqueda_avanzada', __name__, url_prefix='/busqueda')

# MOCK: lista de sitios históricos simulados
MOCK_SITIOS = [
    {"id": 1, "nombre": "Museo X", "ciudad": "La Plata", "provincia": "Buenos Aires", "estado": "Bueno", "fecha_registro": "2024-01-15", "visibilidad": True, "tags":[1,2], "Descripción": "Un museo histórico con muchas exhibiciones."},
    {"id": 2, "nombre": "Iglesia Y", "ciudad": "Quilmes", "provincia": "Buenos Aires", "estado": "Regular", "fecha_registro": "2023-10-10", "visibilidad": False, "tags":[2], "Descripción": "Una iglesia con arquitectura colonial."},
    {"id": 3, "nombre": "Museo T", "ciudad": "San Miguel de Tucumán", "provincia": "Tucumán", "estado": "Bueno", "fecha_registro": "2023-07-12", "visibilidad": True, "tags":[1], "Descripción": "Museo dedicado a la independencia argentina."},
    {"id": 4, "nombre": "Iglesia U", "ciudad": "Salta", "provincia": "Salta", "estado": "Regular", "fecha_registro": "2022-11-03", "visibilidad": True, "tags":[2], "Descripción": "Iglesia colonial con retablos dorados."},
    {"id": 5, "nombre": "Plaza V", "ciudad": "San Juan", "provincia": "San Juan", "estado": "Malo", "fecha_registro": "2021-06-18", "visibilidad": False, "tags":[3], "Descripción": "Plaza central con esculturas patrias."},
    {"id": 6, "nombre": "Museo W", "ciudad": "Córdoba", "provincia": "Córdoba", "estado": "Bueno", "fecha_registro": "2024-03-22", "visibilidad": True, "tags":[1,2], "Descripción": "Museo de arte religioso y moderno."},
    {"id": 7, "nombre": "Iglesia X", "ciudad": "San Luis", "provincia": "San Luis", "estado": "Regular", "fecha_registro": "2023-08-09", "visibilidad": True, "tags":[2], "Descripción": "Iglesia con vitrales franceses."},
    {"id": 8, "nombre": "Plaza Y", "ciudad": "Resistencia", "provincia": "Chaco", "estado": "Malo", "fecha_registro": "2022-04-30", "visibilidad": False, "tags":[3], "Descripción": "Plaza con esculturas urbanas."},
    {"id": 9, "nombre": "Museo Z", "ciudad": "Mendoza", "provincia": "Mendoza", "estado": "Bueno", "fecha_registro": "2024-05-15", "visibilidad": True, "tags":[1], "Descripción": "Museo de historia regional."},
    {"id": 10, "nombre": "Iglesia AA", "ciudad": "San Rafael", "provincia": "Mendoza", "estado": "Regular", "fecha_registro": "2023-01-25", "visibilidad": True, "tags":[2], "Descripción": "Iglesia con arquitectura neogótica."},
    {"id": 11, "nombre": "Plaza AB", "ciudad": "Neuquén", "provincia": "Neuquén", "estado": "Malo", "fecha_registro": "2021-12-10", "visibilidad": False, "tags":[3], "Descripción": "Plaza con fuente iluminada."},
    {"id": 12, "nombre": "Museo AC", "ciudad": "Bariloche", "provincia": "Río Negro", "estado": "Bueno", "fecha_registro": "2024-06-20", "visibilidad": True, "tags":[1,3], "Descripción": "Museo de ciencias naturales y glaciares."},
    {"id": 13, "nombre": "Iglesia AD", "ciudad": "Trelew", "provincia": "Chubut", "estado": "Regular", "fecha_registro": "2023-03-14", "visibilidad": True, "tags":[2], "Descripción": "Iglesia galesa con historia migrante."},
    {"id": 14, "nombre": "Plaza AE", "ciudad": "Rawson", "provincia": "Chubut", "estado": "Malo", "fecha_registro": "2022-02-28", "visibilidad": False, "tags":[3], "Descripción": "Plaza con monumentos navales."},
    {"id": 15, "nombre": "Museo AF", "ciudad": "Santa Rosa", "provincia": "La Pampa", "estado": "Bueno", "fecha_registro": "2024-01-05", "visibilidad": True, "tags":[1], "Descripción": "Museo de historia pampeana."},
    {"id": 16, "nombre": "Iglesia AG", "ciudad": "Formosa", "provincia": "Formosa", "estado": "Regular", "fecha_registro": "2023-07-07", "visibilidad": True, "tags":[2], "Descripción": "Iglesia con frescos indígenas."},
    {"id": 17, "nombre": "Plaza AH", "ciudad": "Posadas", "provincia": "Misiones", "estado": "Malo", "fecha_registro": "2022-10-10", "visibilidad": False, "tags":[3], "Descripción": "Plaza con vegetación tropical."},
    {"id": 18, "nombre": "Museo AI", "ciudad": "Corrientes", "provincia": "Corrientes", "estado": "Bueno", "fecha_registro": "2024-02-14", "visibilidad": True, "tags":[1], "Descripción": "Museo de carnaval y cultura guaraní."},
    {"id": 19, "nombre": "Iglesia AJ", "ciudad": "Paraná", "provincia": "Entre Ríos", "estado": "Regular", "fecha_registro": "2023-05-30", "visibilidad": True, "tags":[2], "Descripción": "Iglesia con campanario de madera."},
    {"id": 20, "nombre": "Plaza AK", "ciudad": "Concordia", "provincia": "Entre Ríos", "estado": "Malo", "fecha_registro": "2022-03-03", "visibilidad": False, "tags":[3], "Descripción": "Plaza con esculturas de artistas locales."},
    {"id": 21, "nombre": "Museo AL", "ciudad": "San Fernando del Valle", "provincia": "Catamarca", "estado": "Bueno", "fecha_registro": "2024-04-01", "visibilidad": True, "tags":[1], "Descripción": "Museo arqueológico de culturas prehispánicas."},
    {"id": 22, "nombre": "Iglesia AM", "ciudad": "La Rioja", "provincia": "La Rioja", "estado": "Regular", "fecha_registro": "2023-06-06", "visibilidad": True, "tags":[2], "Descripción": "Iglesia con fachada de adobe."},
    {"id": 23, "nombre": "Plaza AN", "ciudad": "Santiago del Estero", "provincia": "Santiago del Estero", "estado": "Malo", "fecha_registro": "2021-09-09", "visibilidad": False, "tags":[3], "Descripción": "Plaza con historia colonial y mercado."},
    {"id": 24, "nombre": "Museo AO", "ciudad": "San Salvador de Jujuy", "provincia": "Jujuy", "estado": "Bueno", "fecha_registro": "2024-07-07", "visibilidad": True, "tags":[1,2], "Descripción": "Museo de textiles andinos."},
    {"id": 25, "nombre": "Iglesia AP", "ciudad": "Villa María", "provincia": "Córdoba", "estado": "Regular", "fecha_registro": "2023-02-02", "visibilidad": True, "tags":[2], "Descripción": "Iglesia con arquitectura moderna."},
    {"id": 26, "nombre": "Plaza AQ", "ciudad": "Rafaela", "provincia": "Santa Fe", "estado": "Malo", "fecha_registro": "2022-01-01", "visibilidad": False, "tags":[3], "Descripción": "Plaza con anfiteatro y feria artesanal."},
    {"id": 27, "nombre": "Museo AR", "ciudad": "Rosario", "provincia": "Santa Fe", "estado": "Bueno", "fecha_registro": "2024-08-08", "visibilidad": True, "tags":[1], "Descripción": "Museo del monumento a la bandera."},
    {"id": 28, "nombre": "Iglesia AS", "ciudad": "San Nicolás", "provincia": "Buenos Aires", "estado": "Regular", "fecha_registro": "2023-11-11", "visibilidad": True, "tags":[2], "Descripción": "Iglesia con vitrales coloridos."},
    {"id": 29, "nombre": "Plaza Z", "ciudad": "La Plata", "provincia": "Buenos Aires", "estado": "Malo", "fecha_registro": "2022-05-20", "visibilidad": True, "tags":[1,3], "Descripción": "Una plaza con mucha historia."},
    {"id": 30, "nombre": "Museo AT", "ciudad": "Villa Carlos Paz", "provincia": "Córdoba", "estado": "Bueno", "fecha_registro": "2024-09-12", "visibilidad": True, "tags":[1,2], "Descripción": "Museo interactivo sobre la historia del turismo en las sierras."}
]

TAGS = [
    {"id": 1, "nombre": "Histórico"},
    {"id": 2, "nombre": "Cultural"},
    {"id": 3, "nombre": "Turístico"},
]


def parse_date(s):
    # Convierte string YYYY-MM-DD a datetime.date
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except:
        return None



@bp.get('/')
def index():
    # Leer parámetros
    ciudad = request.args.get("ciudad", "").strip()
    provincia = request.args.get("provincia", "").strip()
    estado = request.args.get("estado", "").strip()
    visibilidad = request.args.get("visibilidad")
    busqueda_texto = request.args.get("busqueda_texto", "").strip()
    tags = [int(t) for t in request.args.getlist("tags") if t.isdigit()]
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 25))
    sort = request.args.get("sort", "fecha_registro")
    order = request.args.get("order", "desc")
    fecha_desde = parse_date(request.args.get("fecha_desde"))
    fecha_hasta = parse_date(request.args.get("fecha_hasta"))
    
    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        flash("El rango de fechas es inválido: 'Desde' no puede ser mayor que 'Hasta'.", "error")
        return redirect(url_for("busqueda_avanzada.index"))

    # Convertir fechas del mock a datetime una sola vez
    for r in MOCK_SITIOS:
        if "_fecha_dt" not in r:
            r["_fecha_dt"] = parse_date(r["fecha_registro"])

    # Filtrado
    def filtro(r):
        if ciudad and r["ciudad"].lower() != ciudad.lower():
            return False
        if provincia and r["provincia"].lower() != provincia.lower():
            return False
        if estado and r["estado"].lower() != estado.lower():
            return False
        if tags and not any(t in r["tags"] for t in tags):
            return False
        if visibilidad == "true" and not r["visibilidad"]:
            return False
        if visibilidad == "false" and r["visibilidad"]:
            return False
        if fecha_desde and r["_fecha_dt"] < fecha_desde:
            return False
        if fecha_hasta and r["_fecha_dt"] > fecha_hasta:
            return False
        if busqueda_texto and busqueda_texto.lower() not in r["nombre"].lower() and busqueda_texto.lower() not in r["Descripción"].lower():
            return False
        return True

    filtered = list(filter(filtro, MOCK_SITIOS))

    # Ordenamiento
    if sort in ("nombre", "fecha_registro", "ciudad"):
        filtered.sort(
            key=lambda r: r[sort].lower() if isinstance(r[sort], str) else r[sort],
            reverse=(order=="desc")
        )

    # Paginación
    total_results = len(filtered)
    total_pages = (total_results + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_items = filtered[start:end]

    return render_template( "busqueda/index.html", 
        results=page_items,
        tags=TAGS,
        ciudad=ciudad,
        provincia=provincia,
        estado=estado,
        selected_tags=tags,
        visibilidad=visibilidad,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        busqueda_texto=busqueda_texto,
        page=page,
        per_page=per_page,
        total_pages=total_pages, 
        sort=sort, 
        order=order,
        total_results=total_results,
        request=request )