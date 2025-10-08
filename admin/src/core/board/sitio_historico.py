"""
Modelo de sitio histórico para modo JSON y validaciones.

Esta clase se usa como estructura de datos base antes de guardar en JSON o DB.
"""
from datetime import datetime

class SitioHistorico:
    """
    Representa un sitio histórico con todos sus campos y validaciones.
    """

    # Campos obligatorios
    CAMPOS_OBLIGATORIOS = [
        "nombre",
        "descripcion_breve",
        "descripcion_completa",
        "ciudad",
        "provincia",
        "estado_conservacion",
        "anio_inauguracion",
        "categoria",
        "visible"
    ]

    # Estados válidos para el campo estado_conservacion
    ESTADOS_VALIDOS = ["Bueno", "Regular", "Malo"]

    def __init__(self, data: dict):
        """
        Inicializa y valida los datos del sitio histórico.
        Lanza ValueError si falta algún campo obligatorio o si hay errores de formato.
        """
        self.validar_datos(data)
        self.data = data

    @classmethod
    def validar_datos(cls, data: dict):
        """Valida que los campos requeridos existan y tengan formato correcto."""
        # 1. Campos obligatorios presentes
        for campo in cls.CAMPOS_OBLIGATORIOS:
            if campo not in data or not str(data[campo]).strip():
                raise ValueError(f"El campo '{campo}' es obligatorio.")

        # 2. Estado de conservación válido
        if data["estado_conservacion"] not in cls.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado de conservación inválido. Debe ser uno de: {cls.ESTADOS_VALIDOS}"
            )

        # 3. Año de inauguración numérico y razonable
        anio = int(data["anio_inauguracion"])
        if anio < 1500 or anio > datetime.now().year:
            raise ValueError("El año de inauguración debe estar entre 1500 y el año actual.")

        # 4. Latitud y longitud opcionales, pero válidas si se incluyen
        if "latitud" in data and data["latitud"] not in (None, ""):
            try:
                lat = float(data["latitud"])
                if not (-90 <= lat <= 90):
                    raise ValueError("La latitud debe estar entre -90 y 90.")
            except ValueError:
                raise ValueError("La latitud debe ser numérica.")

        if "longitud" in data and data["longitud"] not in (None, ""):
            try:
                lon = float(data["longitud"])
                if not (-180 <= lon <= 180):
                    raise ValueError("La longitud debe estar entre -180 y 180.")
            except ValueError:
                raise ValueError("La longitud debe ser numérica.")