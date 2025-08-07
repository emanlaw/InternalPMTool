"""Admin routes for user management."""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user

from app.services.data_service import load_data, save_data
from app.services.firebase_service import get_firestore_client

# Get database instance
db = get_firestore_client()


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/users')
@login_required
def admin_users():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard.home'))
    
    # TODO: Import UserService here to avoid circular imports
    # from app.services.user_service import UserService
    
    # Get filter parameters
    status_filter = request.args.get('status', '')
    role_filter = request.args.get('role', '')
    search_query = request.args.get('search', '')
    
    # For now, get users directly from data
    data = load_data(db)
    users = data.get('users', [])
    
    # Apply filters if needed
    if status_filter:
        users = [u for u in users if u.get('status') == status_filter]
    if role_filter:
        users = [u for u in users if u.get('role') == role_filter]
    if search_query:
        users = [u for u in users if search_query.lower() in u.get('username', '').lower() or 
                 search_query.lower() in u.get('display_name', '').lower()]
    
    # Calculate stats
    all_users = data.get('users', [])
    stats = {
        'total': len(all_users),
        'active': len([u for u in all_users if u.get('status') == 'active']),
        'pending': len([u for u in all_users if u.get('status') == 'pending']),
        'admins': len([u for u in all_users if u.get('role') == 'admin'])
    }
    
    return render_template('admin/users.html', 
                         users=users, 
                         stats=stats,
                         current_status=status_filter,
                         current_role=role_filter,
                         current_search=search_query)


@admin_bp.route('/users/update_status', methods=['POST'])
@login_required
def admin_update_user_status():
    if not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # TODO: Import UserService here to avoid circular imports
    # from app.services.user_service import UserService
    
    user_id = request.json.get('user_id')
    new_status = request.json.get('status')
    
    # For now, update directly
    data = load_data()
    for user in data['users']:
        if user['id'] == user_id:
            user['status'] = new_status
            break
    
    save_data(data)
    return jsonify({'success': True})


@admin_bp.route('/users/update_role', methods=['POST'])
@login_required
def admin_update_user_role():
    if not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # TODO: Import UserService here to avoid circular imports
    # from app.services.user_service import UserService
    
    user_id = request.json.get('user_id')
    new_role = request.json.get('role')
    
    # For now, update directly
    data = load_data()
    for user in data['users']:
        if user['id'] == user_id:
            user['role'] = new_role
            break
    
    save_data(data)
    return jsonify({'success': True})


@admin_bp.route('/users/bulk_update', methods=['POST'])
@login_required
def admin_bulk_update_users():
    if not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # TODO: Import UserService here to avoid circular imports
    # from app.services.user_service import UserService
    
    user_ids = request.json.get('user_ids', [])
    action = request.json.get('action')
    
    # For now, implement basic bulk update
    data = load_data(db)
    
    if action == 'activate':
        for user in data['users']:
            if user['id'] in user_ids:
                user['status'] = 'active'
    elif action == 'suspend':
        for user in data['users']:
            if user['id'] in user_ids:
                user['status'] = 'suspended'
    
    save_data(data)
    return jsonify({'success': True})