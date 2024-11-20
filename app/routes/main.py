# app/routes/main.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Employee, PerformancePrediction
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
        'high_performers': Employee.query.filter(Employee.performance_rating >= 4).count(),
        'avg_performers': Employee.query.filter(Employee.performance_rating == 3).count(),
        'low_performers': Employee.query.filter(Employee.performance_rating <= 2).count()
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
        
        # Make prediction
        prediction = predict_performance(employee_data)
        
        # Save prediction
        pred_record = PerformancePrediction(
            employee_id=employee.id,
            predicted_rating=prediction['rating'],
            confidence_score=prediction['confidence'],
            features_used=employee_data
        )
        db.session.add(pred_record)
        db.session.commit()
        
        flash('Employee added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('employee/add.html')

@main.route('/predict/<int:employee_id>')
@login_required
def predict_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    prediction = predict_performance(employee.__dict__)
    return render_template('employee/prediction.html', employee=employee, prediction=prediction)

def predict_performance(employee_data):
    # Load the model
    model = joblib.load('model/saved_models/classifier.pkl')
    
    # Prepare data (similar to your notebook preprocessing)
    df = pd.DataFrame([employee_data])
    df = pd.get_dummies(df, columns=['gender', 'education_level', 'job_role'])
    
    # Make prediction
    prediction = model.predict(df)[0]
    confidence = model.predict_proba(df).max()
    
    return {
        'rating': prediction,
        'confidence': confidence
    }