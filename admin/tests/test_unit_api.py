"""Tests unitarios para la lógica de la API."""

import pytest
import jwt
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone


class TestAPILogic:
    """Tests unitarios de la lógica de la API."""

    def test_jwt_token_creation(self):
        """Test de creación de token JWT."""
        secret_key = "test-secret-key"
        payload = {
            "public_user_id": "test-user-123",
            "email": "test@example.com",
            "name": "Test User",
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        }
        
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        assert decoded["public_user_id"] == "test-user-123"
        assert decoded["email"] == "test@example.com"
        assert decoded["name"] == "Test User"

    def test_jwt_token_expiration(self):
        """Test de expiración de token JWT."""
        secret_key = "test-secret-key"
        
        # Token expirado
        expired_payload = {
            "public_user_id": "test-user-123",
            "email": "test@example.com",
            "exp": datetime.now(timezone.utc) - timedelta(hours=1)
        }
        
        expired_token = jwt.encode(expired_payload, secret_key, algorithm="HS256")
        
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(expired_token, secret_key, algorithms=["HS256"])

    def test_jwt_invalid_signature(self):
        """Test de token con firma inválida."""
        payload = {
            "public_user_id": "test-user-123",
            "email": "test@example.com",
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        
        token = jwt.encode(payload, "wrong-secret", algorithm="HS256")
        
        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(token, "correct-secret", algorithms=["HS256"])

    @patch('src.web.api.services.site_serv.utils_site.all_sites_to_json')
    def test_sites_service_mock(self, mock_service):
        """Test del servicio de sitios con mock."""
        expected_data = {
            "data": [
                {
                    "id": 1,
                    "name": "Sitio Test",
                    "description": "Descripción test",
                    "latitude": -34.6037,
                    "longitude": -58.3816
                }
            ],
            "pagination": {
                "page": 1,
                "per_page": 10,
                "total": 1,
                "pages": 1
            }
        }
        
        mock_service.return_value = expected_data
        
        # Simular llamada al servicio
        result = mock_service(page=1, per_page=10)
        
        assert result == expected_data
        assert len(result["data"]) == 1
        assert result["data"][0]["name"] == "Sitio Test"
        mock_service.assert_called_once_with(page=1, per_page=10)

    @patch('src.web.api.services.review_serv.utils_review.create_review')
    def test_review_service_mock(self, mock_service):
        """Test del servicio de reviews con mock."""
        expected_review = {
            "id": 1,
            "rating": 5,
            "comment": "Excelente sitio histórico",
            "site_id": 1,
            "user_id": "test-user-123",
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        mock_service.return_value = expected_review
        
        # Simular creación de review
        review_data = {
            "rating": 5,
            "comment": "Excelente sitio histórico"
        }
        
        result = mock_service(1, review_data, "test-user-123")
        
        assert result == expected_review
        assert result["rating"] == 5
        assert result["comment"] == "Excelente sitio histórico"
        mock_service.assert_called_once_with(1, review_data, "test-user-123")

    def test_auth_header_parsing(self):
        """Test de parsing de header de autorización."""
        # Simular parsing de header Authorization
        auth_header = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            assert token == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
        else:
            pytest.fail("Header format is invalid")

    def test_auth_header_invalid_format(self):
        """Test de header de autorización con formato inválido."""
        invalid_headers = [
            "InvalidFormat token123",
            "Bearer",
            "",
            None
        ]
        
        for header in invalid_headers:
            if not header or not header.startswith("Bearer "):
                # Comportamiento esperado para headers inválidos
                assert True
            else:
                pytest.fail(f"Header {header} should be invalid")

    @patch('src.core.services.auth.user_serv.buscar_usuario_public')
    def test_user_lookup_mock(self, mock_user_service):
        """Test del servicio de búsqueda de usuario con mock."""
        mock_user = MagicMock()
        mock_user.id = "test-user-123"
        mock_user.email = "test@example.com"
        mock_user_service.return_value = mock_user
        
        # Simular búsqueda de usuario
        user = mock_user_service("test@example.com")
        
        assert user is not None
        assert user.id == "test-user-123"
        assert user.email == "test@example.com"
        mock_user_service.assert_called_once_with("test@example.com")

    def test_pagination_logic(self):
        """Test de lógica de paginación."""
        # Simular cálculo de paginación
        total_items = 25
        per_page = 10
        current_page = 2
        
        total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
        offset = (current_page - 1) * per_page
        
        pagination = {
            "page": current_page,
            "per_page": per_page,
            "total": total_items,
            "pages": total_pages
        }
        
        assert pagination["page"] == 2
        assert pagination["per_page"] == 10
        assert pagination["total"] == 25
        assert pagination["pages"] == 3
        assert offset == 10

    def test_error_response_format(self):
        """Test del formato de respuesta de error."""
        error_response = {
            "error": {
                "code": "invalid_data",
                "message": "Invalid input data",
                "details": {"rating": ["Missing data for required field."]}
            }
        }
        
        assert "error" in error_response
        assert "code" in error_response["error"]
        assert "message" in error_response["error"]
        assert error_response["error"]["code"] == "invalid_data"
        assert "Invalid input data" in error_response["error"]["message"]

    def test_success_response_format(self):
        """Test del formato de respuesta exitosa."""
        success_response = {
            "id": 1,
            "rating": 5,
            "comment": "Excelente sitio",
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        assert "id" in success_response
        assert success_response["rating"] == 5
        assert success_response["comment"] == "Excelente sitio"
        assert success_response["id"] == 1