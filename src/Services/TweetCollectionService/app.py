"""
Main application module for Tweet Collection Service.
This module initializes the Flask application, configures the database,
and registers API blueprints.
"""

from flask import Flask
from flask_cors import CORS
from routes import upload_blueprint
from database import init_db
import logging


app = Flask(__name__)
CORS(app)
app.register_blueprint(upload_blueprint)

logging.basicConfig(level=logging.INFO)

def initialize_app():
    """Initialize the application context and database connection."""
    with app.app_context():
        init_db()


initialize_app()


if __name__ == '__main__':
    app.run(debug=True, port=5001)