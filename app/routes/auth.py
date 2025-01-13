from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.db import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

# Endpoint for user registration
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Render the registration form
        return render_template('auth/register.html')  # Registration form template

    if request.method == 'POST':
        # Process registration form
        data = request.form
        existing_user = User.query.filter_by(username=data['username']).first()

        if existing_user:
            # Flash error if username already exists
            flash("Username already exists. Please choose a different one.", "error")
            return render_template('auth/register.html')

        # Hash the password
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

        # Create a new user
        new_user = User(
            username=data['username'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        # Flash success message and redirect to login
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('auth.login'))


# Endpoint for user login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Render the login form
        return render_template('auth/login.html')  # Login form template

    if request.method == 'POST':
        # Process login form
        data = request.form
        user = User.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):  # Check hashed password
            login_user(user)  # Log in the user
            return redirect(url_for('main.dashboard'))  # Redirect to dashboard

        # Flash error message if credentials are invalid
        flash("Invalid username or password. Please try again.", "error")
        return render_template('auth/login.html')


# Endpoint for user logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))
