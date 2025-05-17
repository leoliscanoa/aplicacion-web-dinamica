"""
Punto de entrada WSGI para despliegue en servidores como Render.com
"""
import sys
import os

# Añadir el directorio src al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Importar el servidor desde app
from src.app import server

# Esto le indica a gunicorn dónde encontrar la aplicación Flask
application = server

if __name__ == "__main__":
    application.run()