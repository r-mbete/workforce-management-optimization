from flask import Blueprint, jsonify
from app.db import db
from app.models import Employee, PerformanceClassification
from app.ml.classifier import classify_performance

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/dashboard', methods=['GET'])
def api_dashboard():
    high_performers = PerformanceClassification.query.filter(
        PerformanceClassification.performance_rating == 'Fully Meets'
    ).count()
    average_performers = PerformanceClassification.query.filter(
        PerformanceClassification.performance_rating == 'Needs Improvement'
    ).count()

    return jsonify({
        'status': 'success',
        'high_performers': high_performers,
        'average_performers': average_performers
    }), 200

