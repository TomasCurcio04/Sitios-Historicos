# Tests de la API

Este directorio contiene los tests automatizados para la API REST del proyecto.

## Estructura de Tests

- **`test_api_final.py`**: Tests unitarios con mocks (11 tests)
- **`test_unit_api.py`**: Tests de lógica pura (11 tests)
- **`test_real_api.py`**: Tests HTTP reales (12 tests)
- **`test_api_with_auth.py`**: Tests con autenticación real

## Tipos de Tests

### Tests Unitarios (sin servidor)
- **`test_api_final.py`**: Simula la lógica de endpoints con mocks
- **`test_unit_api.py`**: Tests de funciones y validaciones

### Tests de API Real (requiere servidor corriendo)
- **`test_real_api.py`**: Hace requests HTTP reales a la API
- **`test_api_with_auth.py`**: Tests con autenticación real

## Endpoints Testeados

### Endpoints Públicos
- `GET /api/sites/` - Consulta pública de sitios históricos
- `GET /api/sites/{id}` - Obtener detalles de un sitio específico

### Endpoints de Autenticación
- `POST /api/auth/token` - Obtener token JWT desde sesión de Google OAuth

### Endpoints Protegidos
- `POST /api/sites/{id}/reviews` - Crear nueva reseña (requiere token)
- `DELETE /api/sites/{id}/reviews/{review_id}` - Eliminar reseña (requiere token)

## Ejecutar Tests

### Instalar dependencias de test
```bash
poetry install --with test
```

### Ejecutar todos los tests
```bash
# Tests unitarios (sin servidor)
poetry run pytest tests/test_api_final.py tests/test_unit_api.py -v

# Tests de API real (requiere servidor corriendo)
poetry run pytest tests/test_real_api.py -v
```

### Ejecutar tests específicos
```bash
# Tests unitarios
poetry run pytest tests/test_api_final.py -v

# Tests de API real
poetry run pytest tests/test_real_api.py -v

# Tests con autenticación (requiere token)
poetry run pytest tests/test_api_with_auth.py -v
```

## Resultados

### Tests Unitarios (sin servidor)
```bash
# 22 passed, 0 warnings
poetry run pytest tests/test_api_final.py tests/test_unit_api.py -v
```

### Tests de API Real (con servidor)
```bash
# 12 passed - Requiere servidor en http://localhost:5000
poetry run pytest tests/test_real_api.py -v
```

### Ejecutar un test específico
```bash
poetry run pytest tests/test_api_final.py::TestAPIEndpoints::test_public_endpoint_sites_list -v
```

## Casos de Test Cubiertos

### Endpoints Públicos
- ✅ Consulta exitosa de sitios
- ✅ Consulta con filtros y paginación
- ✅ Parámetros inválidos
- ✅ Sitio por ID exitoso
- ✅ Sitio no encontrado
- ✅ Errores del servidor

### Autenticación
- ✅ Obtención exitosa de token JWT
- ✅ Sin sesión autenticada
- ✅ Sesión inválida
- ✅ Verificación de expiración de token
- ✅ Token válido en endpoints protegidos
- ✅ Token faltante
- ✅ Formato de token inválido
- ✅ Token expirado
- ✅ Firma de token inválida

### Endpoints Protegidos
- ✅ Creación exitosa de reseña
- ✅ Campos requeridos faltantes
- ✅ Tipos de datos inválidos
- ✅ Sitio no encontrado
- ✅ Usuario no encontrado en BD
- ✅ Errores del servicio
- ✅ Datos JSON faltantes/vacíos
- ✅ Eliminación exitosa de reseña
- ✅ Eliminación sin autenticación

### Integración
- ✅ Flujo completo de autenticación
- ✅ Flujo de público a protegido
- ✅ Ciclo de vida completo de reseña
- ✅ Consistencia en manejo de errores
- ✅ Consistencia en paginación
- ✅ Headers CORS
- ✅ Validación de Content-Type

## Configuración de Test

### Tests Unitarios
Los tests unitarios utilizan mocks para:
- Base de datos (no requiere BD real)
- Servicios externos
- Autenticación de usuarios
- Sesiones de Flask

### Tests de API Real
Los tests de API real requieren:
- **Servidor Flask corriendo** en `http://localhost:5000`
- Base de datos con datos de prueba
- Para tests con auth: token válido o sesión activa

### Variables de Entorno para Tests
Los tests usan configuración específica:
- `TESTING=True`
- `JWT_SECRET_KEY=test-secret-key`
- `WTF_CSRF_ENABLED=False`

## Notas Importantes

1. **Mocking**: Todos los tests usan mocks para evitar dependencias externas
2. **Aislamiento**: Cada test es independiente y no afecta a otros
3. **Cobertura**: Los tests cubren casos de éxito, error y edge cases
4. **Autenticación**: Se simula autenticación con tokens JWT válidos
5. **Datos**: Se usan datos de prueba consistentes y realistas

## Agregar Nuevos Tests

Para agregar tests para nuevos endpoints:

1. Identifica si es público o protegido
2. Agrega el test al archivo correspondiente
3. Usa los fixtures existentes (`client`, `auth_headers`, etc.)
4. Mockea las dependencias necesarias
5. Prueba casos de éxito y error

Ejemplo:
```python
@patch('src.web.api.services.nuevo_serv.funcion')
def test_nuevo_endpoint(self, mock_funcion, client, auth_headers):
    mock_funcion.return_value = {"resultado": "test"}
    
    response = client.get('/api/nuevo/', headers=auth_headers)
    
    assert response.status_code == 200
    assert response.get_json()["resultado"] == "test"
```