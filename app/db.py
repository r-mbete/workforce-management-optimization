from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy without binding it to an app
db = SQLAlchemy()

# Configuration class for the app
class Config:
    # Define the database URI and other configurations
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/HP/Downloads/workforce-management-optimization/app/my_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY= 'secretkey123'

