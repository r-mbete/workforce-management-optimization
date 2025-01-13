from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager  # Import LoginManager
from app.db import db, Config  # Import the db object and Config class
from app.routes.api import api  # Import API Blueprint
from app.routes.auth import auth  # Import Auth Blueprint
from app.routes.main import main  # Import Main Blueprint

def create_app():
    """Factory function to create the Flask app."""
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configurations from the Config class

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Initialize the database with the app
    db.init_app(app)

    # Initialize Flask-Login LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login page if unauthorized

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Load the user by ID

    # Load classification models into memory
    from app.ml.classifier import load_model
    load_model()  # Ensure the ML model is loaded once during app startup

    # Register Blueprints
    app.register_blueprint(api, url_prefix='/api')  # API routes
    app.register_blueprint(auth, url_prefix='/auth')  # Auth routes
    app.register_blueprint(main, url_prefix='/')  # Main routes (default)

    return app
