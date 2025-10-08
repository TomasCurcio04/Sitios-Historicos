# tests/test_sitio_historico.py
"""Pruebas unitarias para el modelo SitioHistorico."""

import unittest
from datetime import datetime
from src.core.board.sitio_historico import SitioHistorico

class TestSitioHistorico(unittest.TestCase):
    """Testea la clase SitioHistorico y sus validaciones."""

    def setUp(self):
        """Datos base válidos para reutilizar en varios tests."""
        self.base_data = {
            "nombre": "Museo Histórico",
            "descripcion_breve": "Breve descripción",
            "descripcion_completa": "Descripción completa del museo",
            "ciudad": "Buenos Aires",
            "provincia": "Buenos Aires",
            "estado_conservacion": "Bueno",
            "anio_inauguracion": 1990,
            "categoria": "Cultural",
            "visible": True,
            "latitud": -34.61,
            "longitud": -58.38
        }

    def test_datos_validos(self):
        """Debe crear el sitio sin errores si los datos son correctos."""
        sitio = SitioHistorico(self.base_data)
        self.assertEqual(sitio.data["nombre"], "Museo Histórico")
        self.assertTrue(sitio.data["visible"])
        self.assertEqual(sitio.data["estado_conservacion"], "Bueno")

    def test_campo_obligatorio_faltante(self):
        """Debe fallar si falta un campo obligatorio."""
        data = self.base_data.copy()
        del data["nombre"]
        with self.assertRaises(ValueError) as context:
            SitioHistorico(data)
        self.assertIn("nombre", str(context.exception))

    def test_estado_conservacion_invalido(self):
        """Debe fallar si el estado de conservación no es válido."""
        data = self.base_data.copy()
        data["estado_conservacion"] = "Excelente"
        with self.assertRaises(ValueError) as context:
            SitioHistorico(data)
        self.assertIn("Estado de conservación inválido", str(context.exception))

    def test_anio_fuera_de_rango(self):
        """Debe fallar si el año de inauguración está fuera de 1500 y el año actual."""
        data = self.base_data.copy()
        data["anio_inauguracion"] = 1400
        with self.assertRaises(ValueError) as context:
            SitioHistorico(data)
        self.assertIn("año de inauguración", str(context.exception))

    def test_latitud_invalida(self):
        """Debe fallar si la latitud está fuera del rango -90 a 90 o no es numérica."""
        data = self.base_data.copy()
        data["latitud"] = 100
        with self.assertRaises(ValueError) as context:
            SitioHistorico(data)
        self.assertIn("latitud", str(context.exception))

        data["latitud"] = "no es número"
        with self.assertRaises(ValueError) as context:
            SitioHistorico(data)
        self.assertIn("latitud", str(context.exception))

    def test_longitud_invalida(self):
        """Debe fallar si la longitud está fuera del rango -180 a 180 o no es numérica."""
        data = self.base_data.copy()
        data["longitud"] = 200
        with self.assertRaises(ValueError) as context:
            SitioHistorico(data)
        self.assertIn("longitud", str(context.exception))

        data["longitud"] = "no es número"
        with self.assertRaises(ValueError) as context:
            SitioHistorico(data)
        self.assertIn("longitud", str(context.exception))

    def test_latitud_longitud_opcional(self):
        """Debe permitir omitir latitud y longitud sin errores."""
        data = self.base_data.copy()
        del data["latitud"]
        del data["longitud"]
        sitio = SitioHistorico(data)
        self.assertNotIn("latitud", sitio.data)
        self.assertNotIn("longitud", sitio.data)

if __name__ == "__main__":
    unittest.main()