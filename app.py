"""
Entry point for the application when deployed to render.com.
This file imports and exposes the Flask server from the src module.
"""

# Import the server from the src module
from src.app import server as app

# This is needed for gunicorn to find the app
if __name__ == "__main__":
    app.run()