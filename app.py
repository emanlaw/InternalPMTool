from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime, date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import io
import threading

# Firebase imports
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase-service-account.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

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

def get_due_date_class(due_date_str):
    if not due_date_str:
        return ''
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        today = date.today()
        if due_date < today:
            return 'card-overdue'
        elif due_date == today:
            return 'card-due-today'
        elif (due_date - today).days <= 3:
            return 'card-due-soon'
        return ''
    except:
        return ''

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

app.jinja_env.globals.update(
    get_due_date_class=get_due_date_class,
    get_due_date_text_class=get_due_date_text_class,
    get_due_date_status=get_due_date_status,
    get_comment_count=get_comment_count,
    format_timestamp=format_timestamp
)

def load_data():
    data = {'users': [], 'projects': [], 'cards': [], 'comments': []}
    
    try:
        for doc in db.collection('users').stream():
            user_data = doc.to_dict()
            user_data['id'] = int(doc.id)
            data['users'].append(user_data)
    except:
        pass
    
    try:
        for doc in db.collection('projects').stream():
            project_data = doc.to_dict()
            project_data['id'] = int(doc.id)
            data['projects'].append(project_data)
    except:
        pass
    
    try:
        for doc in db.collection('cards').stream():
            card_data = doc.to_dict()
            card_data['id'] = int(doc.id)
            data['cards'].append(card_data)
    except:
        pass
    
    try:
        for doc in db.collection('comments').stream():
            comment_data = doc.to_dict()
            comment_data['id'] = int(doc.id)
            data['comments'].append(comment_data)
    except:
        pass
    
    if not data['users']:
        default_user = {
            'username': 'admin',
            'password_hash': generate_password_hash('admin123')
        }
        db.collection('users').document('1').set(default_user)
        data['users'].append({'id': 1, **default_user})
    
    if not data['projects']:
        default_project = {
            'name': 'Sample Project',
            'description': 'Your first project'
        }
        db.collection('projects').document('1').set(default_project)
        data['projects'].append({'id': 1, **default_project})
    
    return data

def save_data(data):
    try:
        for user in data.get('users', []):
            user_copy = user.copy()
            user_copy.pop('id', None)
            db.collection('users').document(str(user['id'])).set(user_copy)
        
        for project in data.get('projects', []):
            project_copy = project.copy()
            project_copy.pop('id', None)
            db.collection('projects').document(str(project['id'])).set(project_copy)
        
        for card in data.get('cards', []):
            card_copy = card.copy()
            card_copy.pop('id', None)
            db.collection('cards').document(str(card['id'])).set(card_copy)
        
        for comment in data.get('comments', []):
            comment_copy = comment.copy()
            comment_copy.pop('id', None)
            db.collection('comments').document(str(comment['id'])).set(comment_copy)
    except Exception as e:
        print(f"Error saving to Firebase: {e}")

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
        
        if any(u['username'] == username for u in data.get('users', [])):
            flash('Username already exists')
            return render_template('register.html')
        
        new_user = {
            'id': max([u['id'] for u in data.get('users', [])], default=0) + 1,
            'username': username,
            'password_hash': generate_password_hash(password)
        }
        
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

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    data = load_data()
    user_data = next((u for u in data['users'] if u['id'] == current_user.id), None)
    
    if request.method == 'POST':
        email = request.form.get('email', '')
        email_notifications = 'email_notifications' in request.form
        
        for user in data['users']:
            if user['id'] == current_user.id:
                user['email'] = email
                user['email_notifications'] = email_notifications
                break
        
        save_data(data)
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user_data)

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

@app.route('/backlog')
@login_required
def backlog():
    data = load_data()
    backlog_cards = [c for c in data['cards'] if c['status'] == 'todo']
    return render_template('backlog.html', cards=backlog_cards, projects=data['projects'])

@app.route('/analytics')
@login_required
def analytics():
    data = load_data()
    return render_template('gantt_analytics.html', projects=data['projects'], cards=data['cards'])

@app.route('/firebase')
@login_required
def firebase():
    return render_template('firebase_dashboard.html')

@app.route('/firebase-status')
@login_required
def firebase_status():
    try:
        users_count = len(list(db.collection('users').stream()))
        projects_count = len(list(db.collection('projects').stream()))
        cards_count = len(list(db.collection('cards').stream()))
        comments_count = len(list(db.collection('comments').stream()))
        
        return jsonify({
            'success': True,
            'data': {
                'users_count': users_count,
                'projects_count': projects_count,
                'cards_count': cards_count,
                'comments_count': comments_count
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/migrate-to-firebase')
@login_required
def migrate_to_firebase():
    try:
        data = load_data()
        save_data(data)
        return jsonify({
            'success': True,
            'message': 'Data migrated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

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
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'due_date': request.json.get('due_date', ''),
        'story_points': request.json.get('story_points')
    }
    data['cards'].append(new_card)
    save_data(data)
    return jsonify(new_card)

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

@app.route('/api/search')
@login_required
def search_cards():
    data = load_data()
    cards = data['cards']
    
    search_query = request.args.get('q', '').lower()
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    assignee_filter = request.args.get('assignee', '')
    project_filter = request.args.get('project_id', '')
    
    filtered_cards = cards
    
    if project_filter:
        filtered_cards = [c for c in filtered_cards if c['project_id'] == int(project_filter)]
    
    if status_filter:
        filtered_cards = [c for c in filtered_cards if c['status'] == status_filter]
    
    if priority_filter:
        filtered_cards = [c for c in filtered_cards if c['priority'] == priority_filter]
    
    if assignee_filter:
        filtered_cards = [c for c in filtered_cards if c.get('assignee', '').lower() == assignee_filter.lower()]
    
    if search_query:
        filtered_cards = [c for c in filtered_cards if 
                         search_query in c['title'].lower() or 
                         search_query in c.get('description', '').lower()]
    
    return jsonify({
        'cards': filtered_cards,
        'total': len(filtered_cards)
    })

@app.route('/api/move_to_backlog', methods=['POST'])
@login_required
def move_to_backlog():
    try:
        data = load_data()
        card_id = request.json['card_id']
        
        for card in data['cards']:
            if card['id'] == card_id:
                card['status'] = 'todo'
                break
        else:
            return jsonify({'success': False, 'error': 'Card not found'}), 404
        
        save_data(data)
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/delete_card', methods=['POST'])
@login_required
def delete_card():
    try:
        data = load_data()
        card_id = request.json['card_id']
        
        original_count = len(data['cards'])
        data['cards'] = [c for c in data['cards'] if c['id'] != card_id]
        
        if len(data['cards']) == original_count:
            return jsonify({'success': False, 'error': 'Card not found'}), 404
        
        data['comments'] = [c for c in data.get('comments', []) if c['card_id'] != card_id]
        
        save_data(data)
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send_to_assignee', methods=['POST'])
@login_required
def send_to_assignee():
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)