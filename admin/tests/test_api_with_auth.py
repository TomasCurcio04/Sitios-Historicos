"""Tests de la API con autenticación real."""

import pytest
import requests
import json


@pytest.mark.integration
class TestAPIWithAuth:
    """Tests que requieren autenticación real."""
    
    BASE_URL = "https://admin-grupo10.proyecto2025.linti.unlp.edu.ar"
    
    @pytest.fixture
    def auth_token(self):
        """Fixture para obtener token de autenticación real."""
        # Este test requiere que tengas una sesión activa
        # Puedes modificar esto según tu flujo de autenticación
        
        # Opción 1: Si tienes un endpoint de login
        # login_data = {"email": "test@example.com", "password": "password"}
        # login_response = requests.post(f"{self.BASE_URL}/api/login", json=login_data)
        # return login_response.json()["access_token"]
        
        # Opción 2: Token hardcodeado para tests (no recomendado para producción)
        # return "your-test-token-here"
        
        # Opción 3: Saltar si no hay token
        pytest.skip("Requiere token de autenticación real")
    
    def test_create_review_with_auth(self, auth_token):
        """Test de creación de review con autenticación."""
        # Primero obtener un sitio existente
        sites_response = requests.get(f"{self.BASE_URL}/api/sites/")
        sites_data = sites_response.json()
        
        if not sites_data["data"]:
            pytest.skip("No hay sitios disponibles para testear")
        
        site_id = sites_data["data"][0]["id"]
        
        review_data = {
            "rating": 5,
            "comment": "Excelente sitio histórico - test automatizado"
        }
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = requests.post(
            f"{self.BASE_URL}/api/sites/{site_id}/reviews",
            json=review_data,
            headers=headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["rating"] == 5
        assert "test automatizado" in data["comment"]
        
        return data["id"]  # Para cleanup si es necesario
    
    def test_create_review_invalid_data(self, auth_token):
        """Test de creación de review con datos inválidos."""
        invalid_data = {
            "rating": "invalid",  # Debe ser número
            "comment": "x" * 1000  # Muy largo
        }
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = requests.post(
            f"{self.BASE_URL}/api/sites/1/reviews",
            json=invalid_data,
            headers=headers
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "invalid_data"
    
    def test_create_review_site_not_found(self, auth_token):
        """Test de creación de review para sitio inexistente."""
        review_data = {
            "rating": 4,
            "comment": "Review para sitio inexistente"
        }
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        response = requests.post(
            f"{self.BASE_URL}/api/sites/99999/reviews",
            json=review_data,
            headers=headers
        )
        
        assert response.status_code == 404
        data = response.json()
        assert data["error"]["code"] == "not_found"
    
    def test_delete_review_with_auth(self, auth_token):
        """Test de eliminación de review con autenticación."""
        # Primero crear una review para eliminar
        sites_response = requests.get(f"{self.BASE_URL}/api/sites/")
        sites_data = sites_response.json()
        
        if not sites_data["data"]:
            pytest.skip("No hay sitios disponibles")
        
        site_id = sites_data["data"][0]["id"]
        
        # Crear review
        review_data = {
            "rating": 3,
            "comment": "Review temporal para eliminar"
        }
        
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        create_response = requests.post(
            f"{self.BASE_URL}/api/sites/{site_id}/reviews",
            json=review_data,
            headers=headers
        )
        
        if create_response.status_code == 201:
            review_id = create_response.json()["id"]
            
            # Eliminar review
            delete_response = requests.delete(
                f"{self.BASE_URL}/api/sites/{site_id}/reviews/{review_id}",
                headers=headers
            )
            
            assert delete_response.status_code == 204
    
    def test_get_reviews_for_site(self):
        """Test de obtener reviews de un sitio."""
        # Obtener un sitio existente
        sites_response = requests.get(f"{self.BASE_URL}/api/sites/")
        sites_data = sites_response.json()
        
        if not sites_data["data"]:
            pytest.skip("No hay sitios disponibles")
        
        site_id = sites_data["data"][0]["id"]
        
        response = requests.get(f"{self.BASE_URL}/api/sites/{site_id}/reviews")
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)