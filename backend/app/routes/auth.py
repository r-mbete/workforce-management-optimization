from flask import Blueprint, request, jsonify
from app import db
from app.models.models import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Endpoint to register a new user
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Hash the password before storing
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(
        username=data['username'],
        password=hashed_password  # Store hashed password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

# Endpoint for user login
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):  # Compare hashed passwords
        return jsonify({'status': 'success', 'message': 'Login successful'})
    
    return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
