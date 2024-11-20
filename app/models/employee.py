# app/models/employee.py
from app import db
from datetime import datetime

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Basic Information
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    # Features from your model
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    education_level = db.Column(db.String(50))
    job_role = db.Column(db.String(50))
    years_experience = db.Column(db.Float)
    
    # Performance Metrics
    performance_rating = db.Column(db.Integer)  # Target variable
    previous_performance_ratings = db.Column(db.JSON)  # Historical ratings
    
    # Additional Tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    prediction_history = db.Column(db.JSON)  # Store model predictions

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))  # HR, Manager, Admin
    department = db.Column(db.String(50))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PerformancePrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    predicted_rating = db.Column(db.Integer)
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)
    model_version = db.Column(db.String(50))
    confidence_score = db.Column(db.Float)
    features_used = db.Column(db.JSON)  # Store the feature values used for prediction