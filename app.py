from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Simple User class
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    data = load_data()
    user_data = next((u for u in data.get('users', []) if u['id'] == int(user_id)), None)
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['password_hash'])
    return None

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
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
            {'id': 1, 'project_id': 1, 'title': 'Setup project', 'description': 'Initial setup', 'status': 'done', 'assignee': 'John', 'priority': 'High', 'created_at': '2024-01-01'},
            {'id': 2, 'project_id': 1, 'title': 'Design UI', 'description': 'Create mockups', 'status': 'in_progress', 'assignee': 'Jane', 'priority': 'Medium', 'created_at': '2024-01-02'},
            {'id': 3, 'project_id': 1, 'title': 'Implement backend', 'description': 'API development', 'status': 'todo', 'assignee': 'Bob', 'priority': 'High', 'created_at': '2024-01-03'}
        ]
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = load_data()
        user_data = next((u for u in data.get('users', []) if u['username'] == username), None)
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], user_data['username'], user_data['password_hash'])
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = load_data()
        
        # Check if user exists
        if any(u['username'] == username for u in data.get('users', [])):
            flash('Username already exists')
            return render_template('register.html')
        
        # Create new user
        new_user = {
            'id': max([u['id'] for u in data.get('users', [])], default=0) + 1,
            'username': username,
            'password_hash': generate_password_hash(password)
        }
        
        if 'users' not in data:
            data['users'] = []
        data['users'].append(new_user)
        save_data(data)
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    data = load_data()
    all_cards = data['cards']
    stats = {
        'todo': len([c for c in all_cards if c['status'] == 'todo']),
        'in_progress': len([c for c in all_cards if c['status'] == 'in_progress']),
        'done': len([c for c in all_cards if c['status'] == 'done']),
        'total': len(all_cards)
    }
    return render_template('dashboard.html', projects=data['projects'], stats=stats)

@app.route('/issues')
@login_required
def issues_list():
    data = load_data()
    project_id = request.args.get('project_id', type=int)
    
    if project_id:
        cards = [c for c in data['cards'] if c['project_id'] == project_id]
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
    else:
        cards = data['cards']
        project = None
    
    return render_template('issues.html', cards=cards, projects=data['projects'], current_project=project)

@app.route('/board/<int:project_id>')
@login_required
def kanban_board(project_id):
    data = load_data()
    project = next((p for p in data['projects'] if p['id'] == project_id), None)
    if not project:
        return "Project not found", 404
    
    cards = [c for c in data['cards'] if c['project_id'] == project_id]
    todo_cards = [c for c in cards if c['status'] == 'todo']
    in_progress_cards = [c for c in cards if c['status'] == 'in_progress']
    done_cards = [c for c in cards if c['status'] == 'done']
    
    return render_template('kanban.html', 
                         project=project,
                         todo_cards=todo_cards,
                         in_progress_cards=in_progress_cards,
                         done_cards=done_cards)

@app.route('/api/move_card', methods=['POST'])
def move_card():
    data = load_data()
    card_id = request.json['card_id']
    new_status = request.json['status']
    
    for card in data['cards']:
        if card['id'] == card_id:
            card['status'] = new_status
            break
    
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/add_card', methods=['POST'])
def add_card():
    data = load_data()
    new_card = {
        'id': max([c['id'] for c in data['cards']], default=0) + 1,
        'project_id': request.json['project_id'],
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'status': 'todo',
        'assignee': request.json.get('assignee', ''),
        'priority': request.json.get('priority', 'Medium'),
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    data['cards'].append(new_card)
    save_data(data)
    return jsonify(new_card)

@app.route('/api/add_project', methods=['POST'])
def add_project():
    data = load_data()
    new_project = {
        'id': max([p['id'] for p in data['projects']], default=0) + 1,
        'name': request.json['name'],
        'description': request.json.get('description', '')
    }
    data['projects'].append(new_project)
    save_data(data)
    return jsonify(new_project)

@app.route('/api/update_card_status', methods=['POST'])
def update_card_status():
    data = load_data()
    card_id = request.json['card_id']
    new_status = request.json['status']
    
    for card in data['cards']:
        if card['id'] == card_id:
            card['status'] = new_status
            break
    
    save_data(data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)