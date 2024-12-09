from flask import Blueprint, request, jsonify
from app import db
from app.models.models import Employee, Prediction
from app.ml.classifier import classify_performance  # Update to use 'classify_performance'

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
    return jsonify({'status': 'success', 'message': 'Employee added successfully'}), 201

# Endpoint to get dashboard stats (e.g., number of high, low, and avg performers)
@bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    high_performers = Employee.query.join(Prediction).filter(Prediction.performance_rating == 'Exceeds').count()
    avg_performers = Employee.query.join(Prediction).filter(Prediction.performance_rating == 'Fully Meets').count()
    low_performers = Employee.query.join(Prediction).filter(Prediction.performance_rating == 'Needs Improvement').count()
    
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
    
    employee_data = {
        'age': employee.age,
        'years_experience': employee.years_experience,
        'education_level': employee.education_level
    }
    
    # Use the updated classify_performance function
    performance_rating, confidence = classify_performance(employee_data)
    
    # Save classification result to the database
    new_prediction = Prediction(
        employee_id=employee.id,
        performance_rating=performance_rating,
        confidence=confidence
    )
    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({
        'employee_id': employee_id,
        'performance_rating': performance_rating,
        'confidence': confidence
    })
