# API Documentation - Sitios Históricos

## Base URL
- **Desarrollo**: `http://localhost:5000`
- **Producción**: `https://grupo10.proyecto2025.linti.edu.ar`

## Autenticación

### Obtener Token JWT
```http
POST /api/auth/token
```
**Descripción**: Obtiene un token JWT desde una sesión autenticada de Google OAuth.

**Respuesta exitosa (200)**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer"
}
```

**Uso del token**: Incluir en el header `Authorization: Bearer <token>`

---

## Sitios Históricos

### Listar Sitios
```http
GET /api/sites/
```
**Descripción**: Obtiene una lista paginada de sitios históricos con filtros opcionales.

**Parámetros de consulta**:
- `page` (int): Número de página (default: 1)
- `per_page` (int): Elementos por página (default: 20, max: 100)
- `name` (string): Filtrar por nombre del sitio
- `description` (string): Filtrar por descripción
- `city` (string): Filtrar por ciudad
- `province` (string): Filtrar por provincia
- `tags` (string): Filtrar por tags (separados por coma)
- `conservation_state` (string): Estado de conservación
- `search` (string): Búsqueda general por nombre y descripción
- `order_by` (string): Ordenamiento. Opciones:
  - `latest`: Más recientes primero
  - `oldest`: Más antiguos primero
  - `rating-5-1`: Por rating descendente (5 a 1)
  - `rating-1-5`: Por rating ascendente (1 a 5)
  - `name-asc`: Por nombre A-Z
  - `name-desc`: Por nombre Z-A
- `lat` (float): Latitud para búsqueda geoespacial
- `long` (float): Longitud para búsqueda geoespacial
- `radius` (float): Radio en millas para búsqueda geoespacial

**Respuesta exitosa (200)**:
```json
{
  "data": [
    {
      "id": 1,
      "name": "Casa Rosada",
      "description": "Sede del gobierno argentino",
      "latitude": -34.6083,
      "longitude": -58.3712,
      "address": "Balcarce 50",
      "city": "Buenos Aires",
      "category": {
        "id": 1,
        "name": "Edificio Gubernamental"
      },
      "state": {
        "id": 1,
        "name": "Buenos Aires"
      },
      "conservation_state": "Excelente",
      "construction_year": 1873,
      "images": ["url1.jpg", "url2.jpg"],
      "average_rating": 4.5,
      "reviews_count": 25
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150
  }
}
```

### Obtener Sitio por ID
```http
GET /api/sites/{site_id}
```
**Descripción**: Obtiene los detalles completos de un sitio específico.

**Respuesta exitosa (200)**:
```json
{
  "id": 1,
  "name": "Casa Rosada",
  "description": "Descripción detallada del sitio...",
  "latitude": -34.6083,
  "longitude": -58.3712,
  "address": "Balcarce 50",
  "city": "Buenos Aires",
  "category": {
    "id": 1,
    "name": "Edificio Gubernamental"
  },
  "state": {
    "id": 1,
    "name": "Buenos Aires"
  },
  "conservation_state": "Excelente",
  "construction_year": 1873,
  "images": ["url1.jpg", "url2.jpg"],
  "average_rating": 4.5,
  "reviews_count": 25
}
```

### Crear Sitio
```http
POST /api/sites/
```
**Descripción**: Crea un nuevo sitio histórico (requiere autenticación).

**Headers requeridos**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body**:
```json
{
  "name": "Nuevo Sitio Histórico",
  "description": "Descripción del sitio",
  "latitude": -34.6083,
  "longitude": -58.3712,
  "address": "Dirección completa",
  "city": "Ciudad",
  "category_id": 1,
  "state_id": 1,
  "conservation_state": "Bueno",
  "construction_year": 1900
}
```

**Respuesta exitosa (201)**:
```json
{
  "id": 123,
  "name": "Nuevo Sitio Histórico",
  "user_id": 456,
  // ... resto de campos del sitio
}
```

---

## Reseñas

### Obtener Reseñas de un Sitio
```http
GET /api/sites/{site_id}/reviews
```
**Descripción**: Obtiene las reseñas de un sitio específico.

**Parámetros de consulta**:
- `page` (int): Número de página
- `per_page` (int): Elementos por página

**Respuesta exitosa (200)**:
```json
{
  "data": [
    {
      "id": 1,
      "rating": 5,
      "comment": "Excelente lugar histórico",
      "user_name": "Juan Pérez",
      "created_at": "2024-01-15T10:30:00Z",
      "site_id": 1
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 25
  }
}
```

### Crear Reseña
```http
POST /api/sites/{site_id}/reviews
```
**Descripción**: Crea una nueva reseña para un sitio (requiere autenticación).

**Headers requeridos**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body**:
```json
{
  "rating": 5,
  "comment": "Excelente lugar para visitar"
}
```

**Respuesta exitosa (201)**:
```json
{
  "id": 123,
  "rating": 5,
  "comment": "Excelente lugar para visitar",
  "user_name": "Usuario Actual",
  "created_at": "2024-01-15T10:30:00Z",
  "site_id": 1
}
```

### Obtener Reseña Específica
```http
GET /api/sites/{site_id}/reviews/{review_id}
```

### Eliminar Reseña
```http
DELETE /api/sites/{site_id}/reviews/{review_id}
```
**Descripción**: Elimina una reseña (requiere autenticación y ser el autor).

**Respuesta exitosa (204)**: Sin contenido

---

## Favoritos

### Alternar Favorito
```http
PUT /api/sites/{site_id}/favorite
```
**Descripción**: Agrega o quita un sitio de favoritos (requiere autenticación).

**Headers requeridos**:
```
Authorization: Bearer <token>
```

**Respuesta exitosa (204)**: Sin contenido

### Obtener Mis Reseñas
```http
GET /api/me/reviews
```
**Descripción**: Lista todas las reseñas del usuario autenticado (aprobadas, pendientes, rechazadas).

**Headers requeridos**:
```
Authorization: Bearer <token>
```

**Parámetros de consulta**:
- `page` (int): Número de página
- `per_page` (int): Elementos por página

**Respuesta exitosa (200)**:
```json
{
  "data": [
    {
      "id": 1,
      "site_id": 5,
      "site_name": "Casa Rosada",
      "rating": 5,
      "comment": "Excelente lugar histórico",
      "status": "APROBADA",
      "inserted_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "site_id": 3,
      "site_name": "Cabildo",
      "rating": 4,
      "comment": "Muy interesante",
      "status": "PENDIENTE",
      "inserted_at": "2024-01-14T15:20:00Z",
      "updated_at": "2024-01-14T15:20:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 15
  }
}
```

### Obtener Mis Favoritos
```http
GET /api/me/favorites
```
**Descripción**: Lista los sitios favoritos del usuario autenticado.

**Headers requeridos**:
```
Authorization: Bearer <token>
```

**Parámetros de consulta**:
- `page` (int): Número de página
- `per_page` (int): Elementos por página

**Respuesta exitosa (200)**:
```json
{
  "data": [
    {
      "id": 1,
      "name": "Casa Rosada",
      // ... resto de campos del sitio
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 5
  }
}
```

---

## Búsqueda

### Búsqueda por Proximidad
```http
GET /api/search/nearby
```
**Descripción**: Busca sitios cercanos a una ubicación específica.

**Parámetros requeridos**:
- `lat` (float): Latitud
- `lng` (float): Longitud

**Parámetros opcionales**:
- `radius` (float): Radio en km (default: 10)
- `city` (string): Filtrar por ciudad
- `category_id` (int): Filtrar por categoría
- `state_id` (int): Filtrar por estado
- `conservation_state` (string): Filtrar por estado de conservación
- `year_from` (int): Año desde
- `year_to` (int): Año hasta

**Ejemplo**:
```
GET /api/search/nearby?lat=-34.6083&lng=-58.3712&radius=5&category_id=1
```

**Respuesta exitosa (200)**:
```json
{
  "success": true,
  "count": 10,
  "results": [
    {
      "id": 1,
      "name": "Casa Rosada",
      "latitude": -34.6083,
      "longitude": -58.3712,
      "distance_km": 0.5,
      "category": "Edificio Gubernamental",
      "average_rating": 4.5
    }
  ]
}
```

### Búsqueda por Filtros
```http
GET /api/search/filter
```
**Descripción**: Busca sitios usando filtros sin coordenadas geográficas.

**Parámetros opcionales**:
- `q` (string): Búsqueda de texto general
- `city` (string): Ciudad
- `category_id` (int): ID de categoría
- `state_id` (int): ID de estado
- `conservation_state` (string): Estado de conservación
- `year_from` (int): Año desde
- `year_to` (int): Año hasta

**Ejemplo**:
```
GET /api/search/filter?q=casa&city=Buenos Aires&category_id=1
```

### Autocompletado de Ciudades
```http
GET /api/search/autocomplete/cities
```
**Descripción**: Obtiene sugerencias de ciudades para autocompletado.

**Parámetros**:
- `q` (string): Texto a buscar (mínimo 2 caracteres)

**Respuesta exitosa (200)**:
```json
[
  "Buenos Aires",
  "Buenos Aires (Provincia)",
  "Buena Vista"
]
```

---

## Metadatos

### Obtener Estados/Provincias
```http
GET /api/metadata/states
```
**Descripción**: Obtiene todos los estados/provincias disponibles para filtros y formularios.

**Respuesta exitosa (200)**:
```json
[
  {"id": 1, "name": "Buenos Aires"},
  {"id": 2, "name": "Córdoba"},
  {"id": 3, "name": "Santa Fe"}
]
```

### Obtener Tags
```http
GET /api/metadata/tags
```
**Descripción**: Obtiene todos los tags disponibles para filtros y multiselect.

**Respuesta exitosa (200)**:
```json
[
  {"id": 1, "name": "Histórico"},
  {"id": 2, "name": "Colonial"},
  {"id": 3, "name": "Arquitectura"}
]
```

### Obtener Categorías
```http
GET /api/metadata/categories
```
**Descripción**: Obtiene todas las categorías disponibles para clasificación.

**Respuesta exitosa (200)**:
```json
[
  {"id": 1, "name": "Edificio Gubernamental"},
  {"id": 2, "name": "Museo"},
  {"id": 3, "name": "Iglesia"}
]
```

---

## Códigos de Error

### Errores Comunes

**400 Bad Request**:
```json
{
  "error": {
    "code": "invalid_data",
    "message": "Invalid input data",
    "details": {
      "field_name": ["Error específico del campo"]
    }
  }
}
```

**401 Unauthorized**:
```json
{
  "error": {
    "code": "unauthorized",
    "message": "No authenticated session found"
  }
}
```

**404 Not Found**:
```json
{
  "error": {
    "code": "not_found",
    "message": "Site not found"
  }
}
```

**500 Internal Server Error**:
```json
{
  "error": {
    "code": "server_error",
    "message": "An unexpected error occurred"
  }
}
```

---

## Ejemplos de Uso

### Flujo Completo de Autenticación y Uso

1. **Autenticarse con Google OAuth** (en el frontend web)
2. **Obtener token JWT**:
```javascript
const response = await fetch('/api/auth/token', {
  method: 'POST',
  credentials: 'include'
});
const { access_token } = await response.json();
```

3. **Usar la API con el token**:
```javascript
const sitesResponse = await fetch('/api/sites/', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});
const sites = await sitesResponse.json();
```

### Crear un Sitio y Agregar Reseña

```javascript
// 1. Crear sitio
const newSite = await fetch('/api/sites/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: "Museo Nacional",
    description: "Importante museo histórico",
    latitude: -34.6118,
    longitude: -58.3960,
    address: "Av. Las Heras 2555",
    city: "Buenos Aires",
    category_id: 2,
    state_id: 1,
    conservation_state: "Excelente",
    construction_year: 1889
  })
});

const site = await newSite.json();

// 2. Agregar reseña
const review = await fetch(`/api/sites/${site.id}/reviews`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    rating: 5,
    comment: "Excelente museo con gran valor histórico"
  })
});
```

### Búsqueda Geolocalizada

```javascript
// Obtener ubicación del usuario
navigator.geolocation.getCurrentPosition(async (position) => {
  const { latitude, longitude } = position.coords;
  
  // Buscar sitios cercanos
  const response = await fetch(
    `/api/search/nearby?lat=${latitude}&lng=${longitude}&radius=10`
  );
  const { results } = await response.json();
  
  console.log(`Encontrados ${results.length} sitios cercanos`);
});
```

---

## Notas Importantes

1. **CORS**: La API está configurada para aceptar requests desde el frontend en desarrollo y producción.

2. **Paginación**: Todos los endpoints que retornan listas incluyen metadatos de paginación.

3. **Validación**: Todos los inputs son validados usando esquemas Marshmallow.

4. **Autenticación**: Los endpoints que requieren autenticación están claramente marcados.

5. **Rate Limiting**: No implementado actualmente, pero recomendado para producción.

6. **Versionado**: La API actual es v1 implícita. Para futuras versiones, considerar `/api/v2/`.