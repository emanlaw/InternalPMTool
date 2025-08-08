#!/usr/bin/env python3
"""
Testing Environment Flask App
- Runs on port 5001 for testing new features
- Uses same data structure as main app
- Isolated from production
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime, date

# Firebase imports
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate('firebase-service-account.json')
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    print("Firebase initialized successfully!")
    
except Exception as e:
    print(f"Firebase initialization failed: {e}")
    print("ERROR: Please ensure firebase-service-account.json exists with valid credentials")
    db = None

app = Flask(__name__)
app.secret_key = 'testing-secret-key'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password_hash, email=None, display_name=None, role='user', status='active'):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.display_name = display_name or username
        self.role = role
        self.status = status

    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.role == 'admin'

    def is_admin(self):
        """Check if user is an admin"""
        return self.role == 'admin'

@login_manager.user_loader
def load_user(user_id):
    data = load_data()
    user_data = next((u for u in data.get('users', []) if u['id'] == int(user_id)), None)
    if user_data:
        return User(
            user_data['id'], 
            user_data['username'], 
            user_data['password_hash'],
            user_data.get('email'),
            user_data.get('display_name'),
            user_data.get('role', 'user'),
            user_data.get('status', 'active')
        )
    return None

def load_data():
    """Load data from local files for testing"""
    from data_manager import DataManager
    dm = DataManager()
    data = dm.load_data()
    
    # Create default admin user if no users exist
    if not data['users']:
        default_admin = {
            'id': 1,
            'username': 'admin',
            'password_hash': generate_password_hash('admin123'),
            'email': 'admin@test.com',
            'display_name': 'Test Admin',
            'role': 'admin',
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data['users'].append(default_admin)
        save_data(data)
    
    # Ensure there's a test regular user for testing non-admin navigation
    if not any(u.get('username') == 'testuser' for u in data['users']):
        test_user = {
            'id': max([u['id'] for u in data['users']], default=0) + 1,
            'username': 'testuser',
            'password_hash': generate_password_hash('testpass'),
            'email': 'testuser@test.com',
            'display_name': 'Test Regular User',
            'role': 'user',
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data['users'].append(test_user)
        save_data(data)
    
    return data

def save_data(data):
    """Save data to local files for testing"""
    from data_manager import DataManager
    dm = DataManager()
    dm.save_data(data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = load_data()
        user_data = next((u for u in data.get('users', []) if u['username'] == username), None)
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(
                user_data['id'], 
                user_data['username'], 
                user_data['password_hash'],
                user_data.get('email'),
                user_data.get('display_name'),
                user_data.get('role', 'user'),
                user_data.get('status', 'active')
            )
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return redirect(url_for('dashboard'))

@app.route('/issues')
@login_required
def issues_list():
    data = load_data()
    project_id = request.args.get('project_id', type=int)
    
    if project_id:
        cards = [c for c in data['cards'] if c['project_id'] == project_id]
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
        epics = [e for e in data['epics'] if e['project_id'] == project_id]
        stories = [s for s in data['stories'] if s['project_id'] == project_id]
    else:
        cards = data['cards']
        project = None
        epics = data['epics']
        stories = data['stories']
    
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('issues.html', cards=cards, projects=active_projects, epics=epics, stories=stories, current_project=project)

# API Endpoints for testing
@app.route('/api/get_epics/<int:project_id>')
@login_required
def get_epics(project_id):
    try:
        data = load_data()
        epics = [e for e in data['epics'] if e['project_id'] == project_id]
        print(f"TEST API: get_epics({project_id}) returning {len(epics)} epics")
        return jsonify(epics)
    except Exception as e:
        print(f"ERROR in get_epics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_stories/<int:epic_id>')
@login_required
def get_stories(epic_id):
    try:
        data = load_data()
        stories = [s for s in data['stories'] if s['epic_id'] == epic_id]
        print(f"TEST API: get_stories({epic_id}) returning {len(stories)} stories")
        return jsonify(stories)
    except Exception as e:
        print(f"ERROR in get_stories: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
@login_required
def dashboard():
    data = load_data()
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    all_cards = data['cards']
    stats = {
        'todo': len([c for c in all_cards if c['status'] == 'todo']),
        'in_progress': len([c for c in all_cards if c['status'] == 'in_progress']),
        'done': len([c for c in all_cards if c['status'] == 'done']),
        'total': len(all_cards)
    }
    return render_template('dashboard.html', projects=active_projects, stats=stats, load_data=load_data)

@app.route('/backlog')
@login_required
def backlog():
    data = load_data()
    backlog_cards = [c for c in data['cards'] if c['status'] == 'todo']
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('backlog.html', cards=backlog_cards, projects=active_projects)

@app.route('/stories')
@login_required
def stories():
    data = load_data()
    project_id = request.args.get('project_id', type=int)
    
    if project_id:
        epics = [e for e in data['epics'] if e['project_id'] == project_id]
        stories = [s for s in data['stories'] if s['project_id'] == project_id]
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
    else:
        epics = data['epics']
        stories = data['stories']
        project = None
    
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('stories.html', epics=epics, stories=stories, projects=active_projects, current_project=project)

@app.route('/api/update_card_status', methods=['POST'])
@login_required
def update_card_status():
    try:
        data = load_data()
        card_id = request.json['card_id']
        new_status = request.json['status']
        
        for card in data['cards']:
            if card['id'] == card_id:
                card['status'] = new_status
                break
        
        save_data(data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/add_card', methods=['POST'])
@login_required
def add_card():
    try:
        data = load_data()
        
        project_id = request.json.get('project_id')
        epic_id = request.json.get('epic_id')
        story_id = request.json.get('story_id')
        
        # If story_id is provided, get epic_id and project_id from story
        if story_id:
            story = next((s for s in data['stories'] if s['id'] == story_id), None)
            if story:
                epic_id = story['epic_id']
                project_id = story['project_id']
        
        # If epic_id is provided but no story_id, get project_id from epic
        elif epic_id:
            epic = next((e for e in data['epics'] if e['id'] == epic_id), None)
            if epic:
                project_id = epic['project_id']
        
        next_id = max([c['id'] for c in data['cards']], default=0) + 1
        
        new_card = {
            'id': next_id,
            'project_id': project_id,
            'epic_id': epic_id,
            'story_id': story_id,
            'title': request.json['title'],
            'description': request.json.get('description', ''),
            'status': request.json.get('status', 'todo'),
            'assignee': request.json.get('assignee', ''),
            'priority': request.json.get('priority', 'Medium'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'due_date': request.json.get('due_date', ''),
            'labels': request.json.get('labels', [])
        }
        
        data['cards'].append(new_card)
        save_data(data)
        print(f"TEST API: Created card {next_id}: {new_card['title']}")
        return jsonify(new_card)
    except Exception as e:
        print(f"ERROR in add_card: {e}")
        return jsonify({'error': str(e)}), 500

# Template helper functions
def get_due_date_text_class(due_date_str):
    if not due_date_str:
        return ''
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        today = date.today()
        if due_date < today:
            return 'due-date-overdue'
        elif due_date == today:
            return 'due-date-today'
        return 'due-date-upcoming'
    except:
        return ''

def get_due_date_status(due_date_str):
    if not due_date_str:
        return ''
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        today = date.today()
        if due_date < today:
            return '(OVERDUE)'
        elif due_date == today:
            return '(TODAY)'
        elif (due_date - today).days <= 3:
            return '(SOON)'
        return ''
    except:
        return ''

def get_comment_count(card_id):
    data = load_data()
    return len([c for c in data.get('comments', []) if c['card_id'] == card_id])

def format_timestamp(timestamp):
    if not timestamp:
        return '-'
    if isinstance(timestamp, str) and len(timestamp) == 10:
        return timestamp
    try:
        if isinstance(timestamp, str):
            for fmt in ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                try:
                    dt = datetime.strptime(timestamp, fmt)
                    return dt.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    continue
        return timestamp
    except:
        return timestamp

# Register template functions
app.jinja_env.globals.update(
    get_due_date_text_class=get_due_date_text_class,
    get_due_date_status=get_due_date_status,
    get_comment_count=get_comment_count,
    format_timestamp=format_timestamp
)

if __name__ == '__main__':
    print("🧪 TESTING ENVIRONMENT STARTED")
    print("📍 URL: http://127.0.0.1:5002")
    print("👤 Login: admin / admin123")
    print("🔄 Using local JSON files for data")
    app.run(debug=True, host='127.0.0.1', port=5002)