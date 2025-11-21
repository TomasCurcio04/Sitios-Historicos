import os

# Configuración básica
bind = "0.0.0.0:5000"
workers = 2
worker_class = "sync"
timeout = 30
keepalive = 2

# Configuración para servir archivos estáticos
static_map = {
    '/static': 'src/web/static'
}

# Variables de entorno
raw_env = [
    'FLASK_ENV=production'
]

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'