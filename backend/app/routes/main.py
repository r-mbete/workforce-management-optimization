from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Employee, PerformanceClassification
from app import db
import joblib
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    employees = Employee.query.all()
    performance_stats = {
        'high_performers': Employee.query.filter(Employee.performance_rating == 'Exceeds Expectations').count(),
        'avg_performers': Employee.query.filter(Employee.performance_rating == 'Fully Meets Expectations').count(),
        'low_performers': Employee.query.filter(Employee.performance_rating == 'Needs Improvement').count()
    }
    return render_template('dashboard.html', employees=employees, stats=performance_stats)

@main.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        # Get form data
        employee_data = {
            'employee_id': request.form.get('employee_id'),
            'name': request.form.get('name'),
            'age': int(request.form.get('age')),
            'gender': request.form.get('gender'),
            'education_level': request.form.get('education_level'),
            'job_role': request.form.get('job_role'),
            'years_experience': float(request.form.get('years_experience'))
        }
        
        # Create new employee
        employee = Employee(**employee_data)
        db.session.add(employee)
        db.session.commit()
        
        # Classify performance
        classification = classify_performance(employee_data)
        
        # Save classification
        classification_record = PerformanceClassification(
            employee_id=employee.id,
            classified_rating=classification['rating'],
            confidence_score=classification['confidence'],
            features_used=employee_data
        )
        db.session.add(classification_record)
        db.session.commit()
        
        flash('Employee added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('employee/add.html')

@main.route('/classify/<int:employee_id>')
@login_required
def classify_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    classification = classify_performance(employee.__dict__)
    return render_template('employee/classification.html', employee=employee, classification=classification)

def classify_performance(employee_data):
    # Load the model (Ensure it's the correct model file for classification)
    model = joblib.load('app/ml/classifier.joblib')

    # Prepare data (ensure preprocessing aligns with model training)
    df = pd.DataFrame([employee_data])
    df = pd.get_dummies(df, columns=['gender', 'education_level', 'job_role'])
    
    # Classify employee performance
    classification = model.predict(df)[0]  # Model output (e.g., 0, 1, or 2)
    
    # Map numeric classification to performance rating
    rating_map = {
        0: 'Exceeds Expectations',
        1: 'Fully Meets Expectations',
        2: 'Needs Improvement'
    }
    performance_rating = rating_map.get(classification, 'Unknown')  # Default to 'Unknown' if invalid
    
    # Get the classification confidence (probability of the classified class)
    confidence = model.predict_proba(df).max()  # Confidence of the classification
    
    return {
        'rating': performance_rating,
        'confidence': confidence
    }

