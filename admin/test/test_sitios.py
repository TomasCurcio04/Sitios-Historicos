"""
Pruebas completas para el módulo de sitios históricos.
Soporta modo JSON y Base de Datos.
Incluye: crear, listar, actualizar, asignar, y eliminar.
"""

from src.core.board.repository import (
    list_sites, create_site, get_site, update_site, delete_site,
    list_categories, create_category,
    list_states, create_state,
    list_tags, create_tag,
    assign_category_to_site, assign_state_to_site, assign_tag_to_site,
    assign_user,
    USE_JSON
)

print("=== INICIO DE PRUEBAS ===")
print(f"Fuente de datos: {'JSON' if USE_JSON else 'Base de Datos'}")

# ----------------------------
# Crear categoría y estado
# ----------------------------
category_data = {"name": "Monumento Histórico"}
state_data = {"name": "Buenos Aires"}

cat = create_category(**category_data) if not USE_JSON else category_data
state = create_state(**state_data) if not USE_JSON else state_data

# Obtener ID de manera segura según la fuente de datos
if USE_JSON:
    category_id = cat.get("id", 1)  # default 1 si JSON no tiene ID
    state_id = state.get("id", 1)
else:
    category_id = getattr(cat, "id")
    state_id = getattr(state, "id")

print("Categoría y Estado creados.")

# ----------------------------
# Crear un sitio histórico
# ----------------------------
site_data = {
    "name": "Museo Histórico",
    "short_description": "Museo antiguo",
    "full_description": "Museo dedicado a la historia local.",
    "city": "La Plata",
    "province": "Buenos Aires",
    "conservation_state": "Bueno",
    "inauguration_year": 1920,
    "category": category_id,
    "state": state_id,
    "latitude": -34.9214,
    "longitude": -57.9544,
    "is_visible": True,
    "created_by": 1  # usuario de prueba
}

site = create_site(site_data) if USE_JSON else create_site(site_data)
print(f"Sitio creado: {site['name'] if USE_JSON else site.name}")

# ----------------------------
# Listar sitios
# ----------------------------
sites = list_sites()
print(f"Cantidad de sitios: {len(sites)}")

# ----------------------------
# Actualizar sitio (parcial)
# ----------------------------
update_data = {"short_description": "Museo histórico renovado"}
site_id = site["id"] if USE_JSON else site.id
updated_site = update_site(site_id, update_data)
print(f"Sitio actualizado: {updated_site['short_description'] if USE_JSON else updated_site.short_description}")

# ----------------------------
# Asignar categoría y estado
# ----------------------------
assign_category_to_site(cat, site)
assign_state_to_site(state, site)
print("Categoría y Estado asignados correctamente.")

# ----------------------------
# Crear y asignar etiqueta
# ----------------------------
tag_data = {"name": "Cultural"}
tag = create_tag(**tag_data) if not USE_JSON else tag_data
assign_tag_to_site(tag, site)
print("Etiqueta asignada correctamente.")

# ----------------------------
# Asignar usuario
# ----------------------------
user_data = {"id": 1, "name": "Usuario Test"}
assign_user(site, user_data)
print("Usuario asignado correctamente.")

# ----------------------------
# Leer sitio específico
# ----------------------------
fetched_site = get_site(site_id)
print(f"Sitio recuperado: {fetched_site['name'] if USE_JSON else fetched_site.name}")

# ----------------------------
# Eliminar sitio
# ----------------------------
deleted = delete_site(site_id)
print(f"Sitio eliminado correctamente: {deleted}")

# ----------------------------
# Listar sitios finales
# ----------------------------
final_sites = list_sites()
print(f"Cantidad de sitios finales: {len(final_sites)}")

print("=== FIN DE PRUEBAS ===")