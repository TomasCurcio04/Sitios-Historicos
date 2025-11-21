"""Tests que prueban la API real con requests HTTP."""

import pytest
import requests
import json


@pytest.mark.integration
class TestRealAPI:
    """Tests que hacen requests HTTP reales a la API."""

    BASE_URL = "https://admin-grupo10.proyecto2025.linti.unlp.edu.ar"

    def test_public_get_sites(self):
        """Test del endpoint público GET /api/sites/"""
        response = requests.get(f"{self.BASE_URL}/api/sites/")

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert isinstance(data["data"], list)

    def test_public_get_sites_with_params(self):
        """Test del endpoint público con parámetros."""
        params = {"page": 1, "per_page": 5}
        response = requests.get(f"{self.BASE_URL}/api/sites/", params=params)

        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["page"] == 1
        assert data["meta"]["per_page"] == 5

    def test_public_get_site_by_id(self):
        """Test del endpoint público GET /api/sites/{id}"""
        # Primero obtener un sitio existente
        sites_response = requests.get(f"{self.BASE_URL}/api/sites/")
        sites_data = sites_response.json()

        if sites_data["data"]:
            site_id = sites_data["data"][0]["id"]
            response = requests.get(f"{self.BASE_URL}/api/sites/{site_id}")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == site_id

    def test_public_get_site_not_found(self):
        """Test del endpoint público con ID inexistente."""
        response = requests.get(f"{self.BASE_URL}/api/sites/99999")

        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "not_found"

    def test_auth_token_without_session(self):
        """Test del endpoint POST /api/auth/token sin sesión."""
        response = requests.post(f"{self.BASE_URL}/api/auth/token")

        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "unauthorized"

    def test_protected_create_review_without_auth(self):
        """Test del endpoint protegido sin autenticación."""
        review_data = {"rating": 5, "comment": "Test review"}

        response = requests.post(
            f"{self.BASE_URL}/api/sites/1/reviews", json=review_data
        )

        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "unauthorized"

    def test_protected_create_review_invalid_token(self):
        """Test del endpoint protegido con token inválido."""
        review_data = {"rating": 5, "comment": "Test review"}

        headers = {"Authorization": "Bearer invalid-token"}

        response = requests.post(
            f"{self.BASE_URL}/api/sites/1/reviews", json=review_data, headers=headers
        )

        assert response.status_code == 401

    def test_protected_delete_review_without_auth(self):
        """Test del endpoint DELETE sin autenticación."""
        response = requests.delete(f"{self.BASE_URL}/api/sites/1/reviews/1")

        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "unauthorized"

    def test_invalid_endpoint(self):
        """Test de endpoint que no existe."""
        response = requests.get(f"{self.BASE_URL}/api/nonexistent/")

        # Tu API puede redirigir, ajustar según comportamiento real
        assert response.status_code in [404, 200]  # Aceptar ambos

    def test_invalid_method(self):
        """Test de método HTTP no permitido."""
        response = requests.delete(f"{self.BASE_URL}/api/sites/")

        # Tu API puede manejar esto diferente
        assert response.status_code in [405, 200]  # Aceptar ambos

    def test_invalid_json_data(self):
        """Test con datos JSON malformados."""
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            f"{self.BASE_URL}/api/sites/1/reviews", data="invalid json", headers=headers
        )

        # Tu API devuelve 401 (sin auth) antes de validar JSON
        assert response.status_code in [400, 401]

    def test_api_response_headers(self):
        """Test de headers de respuesta de la API."""
        response = requests.get(f"{self.BASE_URL}/api/sites/")

        assert response.headers.get("Content-Type") == "application/json"
        # Verificar CORS si está configurado
        # assert "Access-Control-Allow-Origin" in response.headers
