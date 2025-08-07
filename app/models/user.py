"""User model and authentication utilities."""

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, password_hash, email=None, display_name=None, role='user', status='active'):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.display_name = display_name or username
        self.role = role
        self.status = status

    def get_id(self):
        return str(self.id)

    def has_permission(self, permission):
        """Check if user has a specific permission based on role"""
        if self.role == 'admin':
            return True
        # Add more role-based permissions as needed
        return False

    def is_admin(self):
        """Check if user is an admin"""
        return self.role == 'admin'

    def is_active_user(self):
        """Check if user account is active"""
        return self.status == 'active'

    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.role == 'admin'