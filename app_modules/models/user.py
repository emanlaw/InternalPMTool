from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import json
import os

DATA_FILE = 'data.json'

# Try to import Firebase, fallback to JSON if not available
try:
    from app.services.firebase_service import firebase_service
    USE_FIREBASE = True
except (ImportError, Exception) as e:
    print(f"Firebase not available, using JSON: {e}")
    USE_FIREBASE = False

class User(UserMixin):
    def __init__(self, id, username, password_hash, email=None, display_name=None, role='user', status='active'):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.display_name = display_name or username
        self.role = role  # admin, manager, user, viewer
        self.status = status  # pending, active, suspended, inactive
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_manager(self):
        return self.role in ['admin', 'manager']
    
    def can_manage_users(self):
        return self.role == 'admin'

def load_data():
    if USE_FIREBASE:
        try:
            # Load data from Firebase
            users = firebase_service.get_all_users()
            projects = firebase_service.get_all_projects()
            cards = firebase_service.get_all_cards()
            comments = []
            for card in cards:
                card_comments = firebase_service.get_comments_by_card(card['id'])
                comments.extend(card_comments)
            
            # If Firebase has data, use it
            if users:
                print("Using Firebase data")
                # Convert Firebase data to expected format
                for user in users:
                    # Keep Firebase string IDs as strings
                    pass
                for project in projects:
                    # Keep Firebase string IDs as strings
                    pass
                for card in cards:
                    # Keep Firebase string IDs as strings
                    pass
                
                return {
                    'users': users,
                    'projects': projects,
                    'cards': cards,
                    'comments': comments
                }
            else:
                print("No users in Firebase, falling back to JSON")
        except Exception as e:
            print(f"Firebase error, falling back to JSON: {e}")
            # Fall back to JSON if Firebase fails
    
    # JSON fallback
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Ensure users section exists
            if 'users' not in data:
                data['users'] = [
                    {
                        'id': 1, 
                        'username': 'admin', 
                        'password_hash': generate_password_hash('admin123'),
                        'email': 'admin@pmtool.com',
                        'display_name': 'Administrator',
                        'role': 'admin',
                        'status': 'active',
                        'created_at': '2024-01-01 00:00:00'
                    }
                ]
                save_data(data)
            # Ensure comments section exists
            if 'comments' not in data:
                data['comments'] = []
                save_data(data)
            return data
    return {
        'users': [
            {
                'id': 1, 
                'username': 'admin', 
                'password_hash': generate_password_hash('admin123'),
                'email': 'admin@pmtool.com',
                'display_name': 'Administrator',
                'role': 'admin',
                'status': 'active',
                'created_at': '2024-01-01 00:00:00'
            }
        ],
        'projects': [{
            'id': 1,
            'name': 'Sample Project',
            'description': 'Your first project'
        }],
        'cards': [
            {'id': 1, 'project_id': 1, 'title': 'Setup project', 'description': 'Initial setup', 'status': 'done', 'assignee': 'John', 'priority': 'High', 'created_at': '2024-01-01', 'due_date': '2024-01-15'},
            {'id': 2, 'project_id': 1, 'title': 'Design UI', 'description': 'Create mockups', 'status': 'in_progress', 'assignee': 'Jane', 'priority': 'Medium', 'created_at': '2024-01-02', 'due_date': '2024-12-30'},
            {'id': 3, 'project_id': 1, 'title': 'Implement backend', 'description': 'API development', 'status': 'todo', 'assignee': 'Bob', 'priority': 'High', 'created_at': '2024-01-03', 'due_date': '2024-12-20'}
        ],
        'comments': [
            {'id': 1, 'card_id': 1, 'author': 'admin', 'content': 'Great work on the setup!', 'created_at': '2024-01-02 10:30:00'},
            {'id': 2, 'card_id': 2, 'author': 'admin', 'content': 'Please update the color scheme', 'created_at': '2024-01-03 14:15:00'}
        ]
    }

def save_data(data):
    if USE_FIREBASE:
        try:
            # Update Firebase with any changes
            print("Saving data to Firebase")
            # Firebase saves data automatically through the service
            pass
        except Exception as e:
            print(f"Firebase save error: {e}")
    else:
        # JSON fallback
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)