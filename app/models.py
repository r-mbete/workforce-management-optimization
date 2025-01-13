from app.db import db
from flask_login import UserMixin

# Employee Model
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    education_level = db.Column(db.String(50), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)
    total_working_years = db.Column(db.Integer, nullable=False)
    job_satisfaction = db.Column(db.Float, nullable=False)  
    work_life_balance = db.Column(db.Float, nullable=False)
    years_in_current_role = db.Column(db.Integer, nullable=False) 

    def __repr__(self):
        return f'<Employee {self.name}>'
    
# User Model
class User(db.Model, UserMixin):  # Add UserMixin
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Store hashed password

    def __repr__(self):
        return f'<User {self.username}>'

# PerformanceClassification Model
class PerformanceClassification(db.Model):
    __tablename__ = 'classification_results'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False, index=True)
    performance_rating = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    employee = db.relationship('Employee', backref=db.backref('classification_results', lazy=True))

    def __repr__(self):
        return f'<PerformanceClassification {self.performance_rating} for {self.employee.name}>'
