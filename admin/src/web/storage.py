"""Configuración de almacenamiento con MinIO para la aplicación."""

from minio import Minio

class Storage:
    """Clase para manejar la conexión con MinIO."""
    
    def __init__(self, app=None):
        """Inicializa la clase Storage.
        
        Args:
            app: Instancia de Flask (opcional)
        """
        self._client = None

        if app is not None:
            self.init_app(app)
        
    def init_app(self, app):
        """Inicializa MinIO con la configuración de Flask.
        
        Args:
            app: Instancia de Flask
        
        Returns:
            Aplicación Flask configurada
        """
        self._client = Minio(
            app.config['MINIO_SERVER'],  
            access_key=app.config['MINIO_ACCESS_KEY'],  
            secret_key=app.config['MINIO_SECRET_KEY'],  
            secure=app.config.get('MINIO_SECURE', False)
         )
        app.storage = self._client

        return app
    

storage = Storage()