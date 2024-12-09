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
    # Query the performance stats from the Employee table based on performance ratings
    performance_stats = {
        'high_performers': Employee.query.filter(Employee.performance_rating == 'Exceeds Expectations').count(),
        'avg_performers': Employee.query.filter(Employee.performance_rating == 'Fully Meets Expectations').count(),
        'low_performers': Employee.query.filter(Employee.performance_rating == 'Needs Improvement').count()
    }
    return render_template('dashboard.html', stats=performance_stats)

@main.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        # Get form data for the new employee
        employee_data = {
            'employee_id': request.form.get('employee_id'),
            'name': request.form.get('name'),
            'age': int(request.form.get('age')),
            'gender': request.form.get('gender'),
            'education_level': request.form.get('education_level'),
            'job_role': request.form.get('job_role'),
            'years_experience': float(request.form.get('years_experience'))
        }
        
        # Create new Employee record and add to database
        employee = Employee(**employee_data)
        db.session.add(employee)
        db.session.commit()
        
        # Classify performance based on the employee data
        classification = classify_performance(employee_data)
        
        # Save classification results into PerformanceClassification table
        classification_record = PerformanceClassification(
            employee_id=employee.id,
            classified_rating=classification['rating'],
            confidence_score=classification['confidence'],
            features_used=employee_data
        )
        db.session.add(classification_record)
        db.session.commit()
        
        flash('Employee added and classified successfully!', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('employee/add.html')

@main.route('/classify/<int:employee_id>')
@login_required
def classify_employee(employee_id):
    # Retrieve employee details
    employee = Employee.query.get_or_404(employee_id)
    
    # Classify employee performance based on the employee's data
    classification = classify_performance(employee.__dict__)
    
    return render_template('employee/classification.html', employee=employee, classification=classification)

def classify_performance(employee_data):
    # Load the pre-trained machine learning model
    model = joblib.load('app/ml/classifier.joblib')

    # Prepare the data (ensure it is processed the same way as during model training)
    df = pd.DataFrame([employee_data])
    df = pd.get_dummies(df, columns=['gender', 'education_level', 'job_role'])
    
    # Classify the performance using the model
    classification = model.predict(df)[0]  # Get model's classification output (e.g., 0, 1, or 2)
    
    # Mapping numerical classifications to performance ratings
    rating_map = {
        0: 'Exceeds Expectations',
        1: 'Fully Meets Expectations',
        2: 'Needs Improvement'
    }
    
    performance_rating = rating_map.get(classification, 'Unknown')  # Default to 'Unknown' if invalid
    
    # Retrieve the classification confidence (probability of the predicted class)
    confidence = model.predict_proba(df).max()  # Get the maximum probability of the prediction
    
    return {
        'rating': performance_rating,
        'confidence': confidence
    }


