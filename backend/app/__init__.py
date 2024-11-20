from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize the database
db = SQLAlchemy()

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    
    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)  # To handle cross-origin requests from your React frontend
    
    # Load configuration settings
    app.config.from_object('app.config.Config')
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Import and register routes after initializing the app and db
    from app.routes import api, auth
    app.register_blueprint(api.bp)
    app.register_blueprint(auth.bp)
    
    return app

