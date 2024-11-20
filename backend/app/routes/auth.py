from flask import Blueprint, request, jsonify
from app import db
from app.models.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Endpoint to register a new user
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        password=data['password']  # Hash password before storing in production
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

# Endpoint for user login
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:  # Implement proper password hashing in production
        return jsonify({'status': 'success', 'message': 'Login successful'})
    return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
