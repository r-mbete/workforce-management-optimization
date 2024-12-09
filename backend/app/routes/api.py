from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Employee, PerformanceClassification  # Using PerformanceClassification for storing results
from app.ml.classifier import classify_performance  # Make sure this is correctly importing your classifier

bp = Blueprint('api', __name__, url_prefix='/api')

# Endpoint to add a new employee
@bp.route('/employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    new_employee = Employee(
        employee_id=data['employee_id'],
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        education_level=data['education_level'],
        job_role=data['job_role'],
        years_experience=data['years_experience']
    )
    db.session.add(new_employee)
    db.session.commit()

    # Classify performance after adding the employee
    performance_rating, confidence = classify_performance({
        'age': data['age'],
        'years_experience': data['years_experience'],
        'education_level': data['education_level']
    })

    # Save the classification result to the database
    new_classification = PerformanceClassification(
        employee_id=new_employee.id,
        classified_rating=performance_rating,
        confidence_score=confidence
    )
    db.session.add(new_classification)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Employee added and classified successfully'}), 201

# Endpoint to get dashboard stats (e.g., number of high, low, and avg performers)
@bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    high_performers = Employee.query.join(PerformanceClassification).filter(PerformanceClassification.classified_rating == 'Exceeds Expectations').count()
    avg_performers = Employee.query.join(PerformanceClassification).filter(PerformanceClassification.classified_rating == 'Fully Meets Expectations').count()
    low_performers = Employee.query.join(PerformanceClassification).filter(PerformanceClassification.classified_rating == 'Needs Improvement').count()
    
    stats = {
        'highPerformers': high_performers,
        'avgPerformers': avg_performers,
        'lowPerformers': low_performers,
    }
    return jsonify(stats)

# Endpoint to classify performance for an employee
@bp.route('/employee/<int:employee_id>/classify', methods=['GET'])
def classify_employee_performance(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'status': 'error', 'message': 'Employee not found'}), 404
    
    # Prepare employee data for classification
    employee_data = {
        'age': employee.age,
        'years_experience': employee.years_experience,
        'education_level': employee.education_level
    }
    
    # Classify performance based on employee data
    performance_rating, confidence = classify_performance(employee_data)
    
    # Save classification result to the database
    new_classification = PerformanceClassification(
        employee_id=employee.id,
        classified_rating=performance_rating,
        confidence_score=confidence
    )
    db.session.add(new_classification)
    db.session.commit()

    return jsonify({
        'employee_id': employee_id,
        'performance_rating': performance_rating,
        'confidence': confidence
    })
