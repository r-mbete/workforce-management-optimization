from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Employee, PerformanceClassification
from app.db import db
from app.ml.classifier import classify_performance
from flask import Response
import csv

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        # Redirect authenticated users to the dashboard
        return redirect(url_for('main.dashboard'))
    # Render the index.html for unauthenticated users
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Query classification statistics
    performance_stats = {
        'high_performers': PerformanceClassification.query.filter(
            PerformanceClassification.performance_rating == 'Fully Meets'
        ).count(),
        'average_performers': PerformanceClassification.query.filter(
            PerformanceClassification.performance_rating == 'Needs Improvement'
        ).count()
    }

    # Query all employees with their classifications
    employees = Employee.query.all()
    classified_employees = PerformanceClassification.query.all()

    # Pass statistics and employee details to the template
    return render_template(
        'dashboard.html',
        stats=performance_stats,
        employees=employees,
        classified_employees=classified_employees
    )

@main.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        employee_data = {
            'employee_id': request.form.get('employee_id'),
            'name': request.form.get('name'),
            'age': int(request.form.get('age')),
            'gender': request.form.get('gender'),
            'education_level': request.form.get('education_level'),
            'job_role': request.form.get('job_role'),
            'total_working_years': float(request.form.get('years_experience')),
            'work_life_balance': float(request.form.get('work_life_balance')),
            'years_in_current_role': int(request.form.get('years_in_current_role'))
        }
        new_employee = Employee(**employee_data)
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('employee/add.html')

@main.route('/employee/classify', methods=['GET', 'POST'])
@login_required
def classify_employee():
    employees = Employee.query.all()  # Ensure employees are available for both GET and POST

    if request.method == 'POST':
        employee_id = request.form.get('employee_id')

        # Check if employee_id is valid
        if not employee_id:
            flash("No employee selected. Please try again.", "danger")
            return render_template('employee/classification.html', employees=employees)

        # Fetch the employee
        employee = Employee.query.get_or_404(employee_id)

        try:
            # Perform classification
            classification_label, confidence = classify_performance({
                'WorkLifeBalance': employee.work_life_balance,
                'YearsInCurrentRole': employee.years_in_current_role,
                'TotalWorkingYears': employee.total_working_years,
            })
            classification = {
                'rating': classification_label,
                'confidence': round(confidence * 100, 2),
            }

            # Save classification result to the database
            existing_classification = PerformanceClassification.query.filter_by(employee_id=employee.id).first()
            if existing_classification:
                # Update existing record
                existing_classification.performance_rating = classification_label
                existing_classification.confidence = classification['confidence']
            else:
                # Create a new record
                new_classification = PerformanceClassification(
                    employee_id=employee.id,
                    performance_rating=classification_label,
                    confidence=classification['confidence']
                )
                db.session.add(new_classification)
            db.session.commit()

            prediction = True
        except Exception as e:
            flash(f"Error during classification: {e}", "danger")
            classification = None
            prediction = False

        # Render the template with classification and employee details
        return render_template(
            'employee/classification.html',
            employees=employees,
            employee=employee,
            classification=classification,
            prediction=prediction,
        )

    # For GET requests, just render the form
    return render_template('employee/classification.html', employees=employees)


@main.route('/profile')
@login_required
def profile():
    user = current_user  # Assuming `current_user` is provided by Flask-Login
    return render_template('profile.html', user=user)

@main.route('/employee/edit/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    # Fetch the employee from the database
    employee = Employee.query.get_or_404(employee_id)

    if request.method == 'POST':
        # Update employee attributes with the submitted form data
        employee.name = request.form.get('name')
        employee.job_role = request.form.get('job_role')
        employee.age = int(request.form.get('age'))
        employee.gender = request.form.get('gender')
        employee.education_level = request.form.get('education_level')
        employee.total_working_years = float(request.form.get('years_experience'))
        employee.work_life_balance = float(request.form.get('work_life_balance'))
        employee.years_in_current_role = int(request.form.get('years_in_current_role'))

        # Save changes to the database
        db.session.commit()

        # Redirect to the dashboard with a success message
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    # Render the edit.html page with the employee data for a GET request
    return render_template('employee/edit.html', employee=employee)

@main.route('/employee/delete/<int:employee_id>', methods=['POST'])
@login_required
def delete_employee(employee_id):
    """
    Deletes an employee by their ID.
    """
    employee = Employee.query.get_or_404(employee_id)
    
    try:
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting employee: {e}', 'error')
    
    return redirect(url_for('main.dashboard'))

@main.route('/generate_report', methods=['POST'])
@login_required
def generate_report():
    # Query all classifications and employees
    classifications = PerformanceClassification.query.all()

    # Prepare the data for CSV
    output = []
    header = ['Employee ID', 'Name', 'Job Role', 'Performance Rating', 'Confidence (%)']
    output.append(header)

    for classification in classifications:
        output.append([
            classification.employee.employee_id,
            classification.employee.name,
            classification.employee.job_role,
            classification.performance_rating,
            classification.confidence
        ])

    # Generate CSV content
    csv_output = '\n'.join([','.join(map(str, row)) for row in output])

    # Create a response with the CSV data
    response = Response(csv_output, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=employee_performance_report.csv'

    return response