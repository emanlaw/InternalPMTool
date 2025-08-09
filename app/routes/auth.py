"""Authentication routes: login, logout, registration, profile."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime

from app.models.user import User
from app.services.data_service import load_data, save_data
from app.services.firebase_service import get_firestore_client

# Get database instance
db = get_firestore_client()


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = load_data(db)
        user_data = next((u for u in data.get('users', []) if u['username'] == username), None)
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            # Debug: Print user data
            print(f"Debug - User data: {user_data}")
            print(f"Debug - Status: {user_data.get('status')}")
            
            # Check if user account is active
            if user_data.get('status') != 'active':
                status_messages = {
                    'pending': 'Your account is pending admin approval.',
                    'suspended': 'Your account has been suspended.',
                    'inactive': 'Your account is inactive.'
                }
                flash(f"Account status: {user_data.get('status')} - {status_messages.get(user_data.get('status'), 'Your account is not active.')}")
                return render_template('login.html')
            
            user = User(
                user_data['id'], 
                user_data['username'], 
                user_data['password_hash'],
                user_data.get('email'),
                user_data.get('display_name'),
                user_data.get('role', 'user'),
                user_data.get('status', 'active')
            )
            
            # Update last login
            for u in data['users']:
                if u['id'] == user_data['id']:
                    u['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    break
            save_data(data, db)
            
            login_user(user)
            return redirect(url_for('dashboard.home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        display_name = request.form['display_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # TODO: Import UserService here to avoid circular imports
        # from app.services.user_service import UserService
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long')
            return render_template('register.html')
        
        # TODO: Create user through service
        # result = UserService.create_user(username, email, display_name, password)
        
        # For now, show a message
        flash('Registration feature will be implemented in the next phase.')
        return render_template('register.html')
    
    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    data = load_data(db)
    user_data = next((u for u in data['users'] if u['id'] == current_user.id), None)
    
    if request.method == 'POST':
        email = request.form.get('email', '')
        email_notifications = 'email_notifications' in request.form
        
        for user in data['users']:
            if user['id'] == current_user.id:
                user['email'] = email
                user['email_notifications'] = email_notifications
                break
        
        save_data(data, db)
        flash('Profile updated successfully!')
        return redirect(url_for('auth.profile'))
    
    return render_template('profile.html', user=user_data)