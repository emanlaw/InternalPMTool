from datetime import datetime
from werkzeug.security import generate_password_hash
from app.models.user import load_data, save_data
from app.services.notification_service import send_admin_notification, send_user_status_notification

class UserService:
    @staticmethod
    def create_user(username, email, display_name, password, role='user', status='pending'):
        """Create a new user with pending status"""
        data = load_data()
        
        # Check if username or email already exists
        if any(u['username'] == username for u in data.get('users', [])):
            return {'success': False, 'error': 'Username already exists'}
        
        if any(u.get('email') == email for u in data.get('users', [])):
            return {'success': False, 'error': 'Email already exists'}
        
        # Generate new user ID
        try:
            max_id = max([int(u['id']) for u in data.get('users', []) if str(u['id']).isdigit()], default=0)
            new_user_id = max_id + 1
        except:
            new_user_id = len(data.get('users', [])) + 1
        
        # Create new user
        new_user = {
            'id': new_user_id,
            'username': username,
            'email': email,
            'display_name': display_name,
            'password_hash': generate_password_hash(password),
            'role': role,
            'status': status,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': None
        }
        
        if 'users' not in data:
            data['users'] = []
        data['users'].append(new_user)
        save_data(data)
        
        # Send notification to admin
        send_admin_notification('new_user_registration', new_user)
        
        return {'success': True, 'user': new_user}
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        data = load_data()
        return data.get('users', [])
    
    @staticmethod
    def get_pending_users():
        """Get users with pending status"""
        data = load_data()
        return [u for u in data.get('users', []) if u.get('status') == 'pending']
    
    @staticmethod
    def update_user_status(user_id, new_status, admin_username):
        """Update user status (approve/reject/suspend)"""
        data = load_data()
        
        for user in data['users']:
            if user['id'] == user_id:
                old_status = user.get('status')
                user['status'] = new_status
                user['status_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                user['status_updated_by'] = admin_username
                
                save_data(data)
                
                # Send notification to user
                send_user_status_notification(user, old_status, new_status)
                
                return {'success': True, 'user': user}
        
        return {'success': False, 'error': 'User not found'}
    
    @staticmethod
    def update_user_role(user_id, new_role, admin_username):
        """Update user role"""
        data = load_data()
        
        for user in data['users']:
            if user['id'] == user_id:
                user['role'] = new_role
                user['role_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                user['role_updated_by'] = admin_username
                
                save_data(data)
                return {'success': True, 'user': user}
        
        return {'success': False, 'error': 'User not found'}
    
    @staticmethod
    def bulk_update_users(user_ids, action, admin_username):
        """Bulk update multiple users"""
        data = load_data()
        updated_users = []
        
        for user_id in user_ids:
            for user in data['users']:
                if user['id'] == user_id:
                    if action == 'approve':
                        user['status'] = 'active'
                    elif action == 'reject':
                        user['status'] = 'inactive'
                    elif action == 'suspend':
                        user['status'] = 'suspended'
                    
                    user['status_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    user['status_updated_by'] = admin_username
                    updated_users.append(user)
                    break
        
        if updated_users:
            save_data(data)
            
            # Send notifications to affected users
            for user in updated_users:
                send_user_status_notification(user, 'pending', user['status'])
        
        return {'success': True, 'updated_count': len(updated_users)}
    
    @staticmethod
    def get_user_activity_stats():
        """Get user activity statistics"""
        data = load_data()
        users = data.get('users', [])
        
        stats = {
            'total_users': len(users),
            'active_users': len([u for u in users if u.get('status') == 'active']),
            'pending_users': len([u for u in users if u.get('status') == 'pending']),
            'suspended_users': len([u for u in users if u.get('status') == 'suspended']),
            'admin_users': len([u for u in users if u.get('role') == 'admin']),
            'manager_users': len([u for u in users if u.get('role') == 'manager']),
            'regular_users': len([u for u in users if u.get('role') == 'user'])
        }
        
        return stats
    
    @staticmethod
    def search_users(query, status_filter=None, role_filter=None):
        """Search users by username, email, or display name"""
        data = load_data()
        users = data.get('users', [])
        
        # Apply filters
        if status_filter:
            users = [u for u in users if u.get('status') == status_filter]
        
        if role_filter:
            users = [u for u in users if u.get('role') == role_filter]
        
        # Apply search query
        if query:
            query = query.lower()
            users = [u for u in users if 
                    query in u.get('username', '').lower() or
                    query in u.get('email', '').lower() or
                    query in u.get('display_name', '').lower()]
        
        return users