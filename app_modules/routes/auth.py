from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User, load_data, save_data
from app.services.user_service import UserService
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = load_data()
        user_data = next((u for u in data.get('users', []) if u['username'] == username), None)
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            # Check if user account is active
            if user_data.get('status') != 'active':
                status_messages = {
                    'pending': 'Your account is pending admin approval.',
                    'suspended': 'Your account has been suspended.',
                    'inactive': 'Your account is inactive.'
                }
                flash(status_messages.get(user_data.get('status'), 'Your account is not active.'))
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
            save_data(data)
            
            login_user(user)
            return redirect(url_for('main.home'))
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
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long')
            return render_template('register.html')
        
        # Create user through service
        result = UserService.create_user(username, email, display_name, password)
        
        if result['success']:
            flash('Registration successful! Your account is pending admin approval. You will receive an email notification once approved.')
            return redirect(url_for('auth.login'))
        else:
            flash(result['error'])
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
    data = load_data()
    user_data = next((u for u in data['users'] if u['id'] == current_user.id), None)
    
    if request.method == 'POST':
        # Update user email and notification preferences
        email = request.form.get('email', '')
        email_notifications = 'email_notifications' in request.form
        
        for user in data['users']:
            if user['id'] == current_user.id:
                user['email'] = email
                user['email_notifications'] = email_notifications
                break
        
        save_data(data)
        flash('Profile updated successfully!')
        return redirect(url_for('auth.profile'))
    
    return render_template('profile.html', user=user_data)

# Admin Routes
@auth_bp.route('/admin/users')
@login_required
def admin_users():
    if not current_user.can_manage_users():
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('main.home'))
    
    # Get filter parameters
    status_filter = request.args.get('status', '')
    role_filter = request.args.get('role', '')
    search_query = request.args.get('search', '')
    
    # Get filtered users
    users = UserService.search_users(search_query, status_filter, role_filter)
    stats = UserService.get_user_activity_stats()
    
    return render_template('admin/users.html', 
                         users=users, 
                         stats=stats,
                         current_status=status_filter,
                         current_role=role_filter,
                         current_search=search_query)

@auth_bp.route('/admin/users/update_status', methods=['POST'])
@login_required
def admin_update_user_status():
    if not current_user.can_manage_users():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    user_id = request.json.get('user_id')
    new_status = request.json.get('status')
    
    result = UserService.update_user_status(user_id, new_status, current_user.username)
    return jsonify(result)

@auth_bp.route('/admin/users/update_role', methods=['POST'])
@login_required
def admin_update_user_role():
    if not current_user.can_manage_users():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    user_id = request.json.get('user_id')
    new_role = request.json.get('role')
    
    result = UserService.update_user_role(user_id, new_role, current_user.username)
    return jsonify(result)

@auth_bp.route('/admin/users/bulk_update', methods=['POST'])
@login_required
def admin_bulk_update_users():
    if not current_user.can_manage_users():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    user_ids = request.json.get('user_ids', [])
    action = request.json.get('action')
    
    result = UserService.bulk_update_users(user_ids, action, current_user.username)
    return jsonify(result)

@auth_bp.route('/admin/users/stats')
@login_required
def admin_user_stats():
    if not current_user.can_manage_users():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    stats = UserService.get_user_activity_stats()
    return jsonify(stats)