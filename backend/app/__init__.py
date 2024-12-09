from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
from app.ml.classifier import load_models  # Import the load_models function

# Initialize the database
db = SQLAlchemy()

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    
    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)  # To handle cross-origin requests from your React frontend
    
    # Load environment variables from .env file
    load_dotenv()

    # Load configuration settings
    app.config.from_object('app.config.Config')
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Load classification models into memory for the app (e.g., decision tree, AdaBoost)
    load_models()  # This function should be implemented in your classifier.py to load models
    
    # Import and register routes after initializing the app and db
    from app.routes import api, auth, main  # Add main blueprint here
    app.register_blueprint(api.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)  # Register the main blueprint
    
    return app


