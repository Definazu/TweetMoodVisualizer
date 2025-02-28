# app.py
"""
Main application module for Tweet Collection Service.

This module initializes the Flask application, configures the database,
and registers API blueprints.
"""

from flask import Flask
from routes import upload_blueprint
from database import init_db
import logging

app = Flask(__name__)
app.register_blueprint(upload_blueprint)

logging.basicConfig(level=logging.INFO)

def initialize_app():
    """Initialize the application context and database connection.
    
    This function should be called before any database operations.
    """
    with app.app_context():
        init_db()

if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)