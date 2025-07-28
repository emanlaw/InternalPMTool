from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import json
import os

DATA_FILE = 'data.json'

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Ensure users section exists
            if 'users' not in data:
                data['users'] = [
                    {'id': 1, 'username': 'admin', 'password_hash': generate_password_hash('admin123')}
                ]
                save_data(data)
            # Ensure comments section exists
            if 'comments' not in data:
                data['comments'] = []
                save_data(data)
            return data
    return {
        'users': [
            {'id': 1, 'username': 'admin', 'password_hash': generate_password_hash('admin123')}
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
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)