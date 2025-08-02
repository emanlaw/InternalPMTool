from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime, date

# Firebase imports
import firebase_admin
from firebase_admin import credentials, firestore

# Sprint management imports
from app_modules.services.sprint_service import SprintService

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase-service-account.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Simple Flask app for Windows
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

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
    
    def is_admin(self):
        return self.role == 'admin'
    
    def can_manage_users(self):
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
    """Load data from Firebase"""
    data = {'users': [], 'projects': [], 'cards': [], 'comments': []}
    
    try:
        # Load from Firebase collections
        for doc in db.collection('users').stream():
            user_data = doc.to_dict()
            user_data['id'] = int(doc.id)
            data['users'].append(user_data)
        
        for doc in db.collection('projects').stream():
            project_data = doc.to_dict()
            project_data['id'] = int(doc.id)
            data['projects'].append(project_data)
        
        # Load cards from projects/{projectId}/cards subcollection
        for project_doc in db.collection('projects').stream():
            project_id = int(project_doc.id)
            cards_ref = db.collection('projects').document(project_doc.id).collection('cards')
            for card_doc in cards_ref.stream():
                card_data = card_doc.to_dict()
                card_data['id'] = int(card_doc.id)
                card_data['project_id'] = project_id
                data['cards'].append(card_data)
                
                # Load comments for this card
                comments_ref = cards_ref.document(card_doc.id).collection('comments')
                for comment_doc in comments_ref.stream():
                    comment_data = comment_doc.to_dict()
                    comment_data['id'] = int(comment_doc.id)
                    comment_data['card_id'] = int(card_doc.id)
                    data['comments'].append(comment_data)
    except Exception as e:
        print(f"Firebase error: {e}")
    
    # Create default data if empty
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
    """Save data to Firebase"""
    try:
        # Save to Firebase collections
        for user in data.get('users', []):
            user_copy = user.copy()
            user_copy.pop('id', None)
            db.collection('users').document(str(user['id'])).set(user_copy)
        
        for project in data.get('projects', []):
            project_copy = project.copy()
            project_copy.pop('id', None)
            db.collection('projects').document(str(project['id'])).set(project_copy)
        
        # Save cards to projects/{projectId}/cards subcollection
        for card in data.get('cards', []):
            card_copy = card.copy()
            card_copy.pop('id', None)
            card_copy.pop('project_id', None)  # Remove project_id as it's implicit in path
            project_ref = db.collection('projects').document(str(card['project_id']))
            project_ref.collection('cards').document(str(card['id'])).set(card_copy)
        
        # Save comments to projects/{projectId}/cards/{cardId}/comments
        for comment in data.get('comments', []):
            comment_copy = comment.copy()
            comment_copy.pop('id', None)
            card_id = comment_copy.pop('card_id')
            # Find project_id for this card
            card = next((c for c in data.get('cards', []) if c['id'] == card_id), None)
            if card:
                project_ref = db.collection('projects').document(str(card['project_id']))
                card_ref = project_ref.collection('cards').document(str(card_id))
                card_ref.collection('comments').document(str(comment['id'])).set(comment_copy)
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
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        display_name = request.form['display_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Import UserService here to avoid circular imports
        from app_modules.services.user_service import UserService
        
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
            return redirect(url_for('login'))
        else:
            flash(result['error'])
            return render_template('register.html')
    
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

# Admin Routes
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('home'))
    
    from app_modules.services.user_service import UserService
    
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

@app.route('/admin/users/update_status', methods=['POST'])
@login_required
def admin_update_user_status():
    if not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    from app_modules.services.user_service import UserService
    
    user_id = request.json.get('user_id')
    new_status = request.json.get('status')
    
    result = UserService.update_user_status(user_id, new_status, current_user.username)
    return jsonify(result)

@app.route('/admin/users/update_role', methods=['POST'])
@login_required
def admin_update_user_role():
    if not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    from app_modules.services.user_service import UserService
    
    user_id = request.json.get('user_id')
    new_role = request.json.get('role')
    
    result = UserService.update_user_role(user_id, new_role, current_user.username)
    return jsonify(result)

@app.route('/admin/users/bulk_update', methods=['POST'])
@login_required
def admin_bulk_update_users():
    if not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    from app_modules.services.user_service import UserService
    
    user_ids = request.json.get('user_ids', [])
    action = request.json.get('action')
    
    result = UserService.bulk_update_users(user_ids, action, current_user.username)
    return jsonify(result)

@app.route('/api/save_mindmap', methods=['POST'])
@login_required
def save_mindmap():
    try:
        data = load_data()
        project_id = request.json.get('project_id')
        nodes = request.json.get('nodes', [])
        connections = request.json.get('connections', [])
        
        # Initialize mindmaps if not exists
        if 'mindmaps' not in data:
            data['mindmaps'] = {}
        
        # Save mind map data
        data['mindmaps'][str(project_id)] = {
            'nodes': nodes,
            'connections': connections,
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_by': current_user.username
        }
        
        save_data(data)
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/load_mindmap/<int:project_id>')
@login_required
def load_mindmap(project_id):
    try:
        data = load_data()
        mindmaps = data.get('mindmaps', {})
        mindmap_data = mindmaps.get(str(project_id), {'nodes': [], 'connections': []})
        
        return jsonify({
            'success': True,
            'nodes': mindmap_data.get('nodes', []),
            'connections': mindmap_data.get('connections', [])
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    data = load_data()
    # Filter out archived projects
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    all_cards = data['cards']
    stats = {
        'todo': len([c for c in all_cards if c['status'] == 'todo']),
        'in_progress': len([c for c in all_cards if c['status'] == 'in_progress']),
        'done': len([c for c in all_cards if c['status'] == 'done']),
        'total': len(all_cards)
    }
    return render_template('dashboard.html', projects=active_projects, stats=stats, load_data=load_data)

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

@app.route('/gantt')
@login_required
def gantt():
    data = load_data()
    projects = data.get('projects', [])
    cards = data.get('cards', [])
    
    # Calculate project progress
    def get_project_progress(project_id):
        project_cards = [c for c in cards if c.get('project_id') == project_id]
        if not project_cards:
            return 0
        completed = len([c for c in project_cards if c.get('status') == 'done'])
        return round((completed / len(project_cards)) * 100)
    
    return render_template('gantt.html', 
                         projects=projects, 
                         cards=cards,
                         get_project_progress=get_project_progress)

@app.route('/firebase')
@login_required
def firebase_dashboard():
    data = load_data()
    stats = {
        'users_count': len(data['users']),
        'projects_count': len(data['projects']),
        'cards_count': len(data['cards']),
        'comments_count': len(data['comments'])
    }
    return render_template('firebase_dashboard.html', stats=stats)

@app.route('/firebase-status')
@login_required
def firebase_status():
    data = load_data()
    return jsonify({
        'success': True,
        'data': {
            'users_count': len(data['users']),
            'projects_count': len(data['projects']),
            'cards_count': len(data['cards']),
            'comments_count': len(data['comments'])
        }
    })

@app.route('/migrate-to-firebase')
@login_required
def migrate_to_firebase():
    try:
        data = load_data()
        # Since we're using JSON storage, this is just a placeholder
        # In a real Firebase setup, this would migrate data to Firestore
        return jsonify({
            'success': True,
            'message': f'Data ready for migration: {len(data["users"])} users, {len(data["projects"])} projects, {len(data["cards"])} cards'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/settings')
@login_required
def settings():
    data = load_data()
    stats = {
        'users_count': len(data['users']),
        'projects_count': len(data['projects']),
        'cards_count': len(data['cards']),
        'comments_count': len(data['comments'])
    }
    return render_template('dashboard.html', projects=data['projects'], stats=stats)

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
@login_required
def add_card():
    project_id = request.json['project_id']
    data = load_data()
    
    # Get next card ID for this project
    project_cards = [c for c in data['cards'] if c['project_id'] == project_id]
    next_id = max([c['id'] for c in project_cards], default=0) + 1
    
    new_card = {
        'id': next_id,
        'project_id': project_id,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'status': 'todo',
        'assignee': request.json.get('assignee', ''),
        'priority': request.json.get('priority', 'Medium'),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'due_date': request.json.get('due_date', ''),
        'story_points': request.json.get('story_points')
    }
    
    # Save directly to Firebase subcollection
    card_copy = new_card.copy()
    card_copy.pop('id', None)
    card_copy.pop('project_id', None)
    
    project_ref = db.collection('projects').document(str(project_id))
    project_ref.collection('cards').document(str(next_id)).set(card_copy)
    
    return jsonify(new_card)

@app.route('/api/update_card_status', methods=['POST'])
@login_required
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

@app.route('/api/add_project', methods=['POST'])
@login_required
def add_project():
    data = load_data()
    new_project = {
        'id': max([p['id'] for p in data['projects']], default=0) + 1,
        'name': request.json['name'],
        'description': request.json.get('description', ''),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data['projects'].append(new_project)
    save_data(data)
    return jsonify(new_project)

@app.route('/api/update_card', methods=['POST'])
@login_required
def update_card():
    data = load_data()
    card_id = request.json['card_id']
    updates = request.json.get('updates', {})
    
    for card in data['cards']:
        if card['id'] == card_id:
            card.update(updates)
            card['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            break
    
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/card/<int:card_id>')
@login_required
def get_card_details(card_id):
    data = load_data()
    card = next((c for c in data['cards'] if c['id'] == card_id), None)
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    comments = [c for c in data.get('comments', []) if c['card_id'] == card_id]
    return jsonify({'card': card, 'comments': comments})

@app.route('/api/card/<int:card_id>/comments', methods=['GET', 'POST'])
@login_required
def card_comments(card_id):
    data = load_data()
    
    if request.method == 'POST':
        new_comment = {
            'id': max([c['id'] for c in data.get('comments', [])], default=0) + 1,
            'card_id': card_id,
            'author': current_user.username,
            'content': request.json['content'],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        if 'comments' not in data:
            data['comments'] = []
        data['comments'].append(new_comment)
        save_data(data)
        return jsonify(new_comment)
    
    comments = [c for c in data.get('comments', []) if c['card_id'] == card_id]
    return jsonify(comments)

@app.route('/api/update_card_due_date', methods=['POST'])
@login_required
def update_card_due_date():
    data = load_data()
    card_id = request.json['card_id']
    new_due_date = request.json['due_date']
    
    for card in data['cards']:
        if card['id'] == card_id:
            card['due_date'] = new_due_date
            card['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            break
    
    save_data(data)
    return jsonify({'success': True})

@app.route('/archive')
@login_required
def archive():
    data = load_data()
    archived_projects = [p for p in data['projects'] if p.get('archived', False)]
    return render_template('archive.html', projects=archived_projects)

@app.route('/mindmap')
@login_required
def mindmap():
    data = load_data()
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('mindmap.html', projects=active_projects)

# Sprint Management Routes
@app.route('/sprints')
@login_required
def sprints():
    data = load_data()
    sprint_service = SprintService()
    
    all_sprints = sprint_service.get_all_sprints()
    active_sprints = sprint_service.get_active_sprints()
    completed_sprints = [s for s in all_sprints if s.status == 'completed']
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    
    return render_template('sprints.html', 
                         sprints=all_sprints,
                         active_sprints=active_sprints,
                         completed_sprints=completed_sprints,
                         projects=active_projects)

@app.route('/sprints/<int:sprint_id>')
@login_required
def sprint_detail(sprint_id):
    data = load_data()
    sprint_service = SprintService()
    
    sprint = sprint_service.get_sprint_by_id(sprint_id)
    if not sprint:
        return "Sprint not found", 404
    
    # Get project cards
    project_cards = [c for c in data['cards'] if c['project_id'] == sprint.project_id]
    
    # Separate backlog and sprint issues
    sprint_issues = [c for c in project_cards if c['id'] in sprint.issues]
    backlog_issues = [c for c in project_cards if c['id'] not in sprint.issues and c['status'] == 'todo']
    
    # Calculate metrics
    completed_issues = [c for c in sprint_issues if c['status'] == 'done']
    days_remaining = max(0, (sprint.end_date - date.today()).days)
    
    return render_template('sprint_detail.html',
                         sprint=sprint,
                         sprint_issues=sprint_issues,
                         backlog_issues=backlog_issues,
                         completed_issues=completed_issues,
                         days_remaining=days_remaining)

# Sprint API Routes
@app.route('/api/sprints', methods=['POST'])
@login_required
def create_sprint():
    try:
        sprint_service = SprintService()
        
        name = request.json['name']
        project_id = request.json['project_id']
        start_date = datetime.fromisoformat(request.json['start_date']).date()
        end_date = datetime.fromisoformat(request.json['end_date']).date()
        goal = request.json.get('goal', '')
        story_points = request.json.get('story_points', 0)
        
        sprint = sprint_service.create_sprint(
            name=name,
            project_id=project_id,
            start_date=start_date,
            end_date=end_date,
            goal=goal,
            story_points=story_points
        )
        
        return jsonify({'success': True, 'sprint': sprint.to_dict()})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/start', methods=['POST'])
@login_required
def start_sprint(sprint_id):
    try:
        sprint_service = SprintService()
        success = sprint_service.start_sprint(sprint_id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Sprint not found'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/complete', methods=['POST'])
@login_required
def complete_sprint(sprint_id):
    try:
        sprint_service = SprintService()
        success = sprint_service.complete_sprint(sprint_id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Sprint not found'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/issues', methods=['POST'])
@login_required
def add_issue_to_sprint(sprint_id):
    try:
        sprint_service = SprintService()
        issue_id = request.json['issue_id']
        
        success = sprint_service.assign_issue_to_sprint(sprint_id, issue_id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to add issue to sprint'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/issues/<int:issue_id>', methods=['DELETE'])
@login_required
def remove_issue_from_sprint(sprint_id, issue_id):
    try:
        sprint_service = SprintService()
        success = sprint_service.remove_issue_from_sprint(sprint_id, issue_id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to remove issue from sprint'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/retrospective', methods=['POST'])
@login_required
def save_retrospective(sprint_id):
    try:
        # For now, just return success - in a full implementation,
        # this would save retrospective data to the database
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/export')
@login_required
def export_sprint_report(sprint_id):
    try:
        # For now, just return a placeholder - in a full implementation,
        # this would generate and return a PDF or Excel report
        return jsonify({'success': True, 'message': 'Export functionality coming soon!'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/archive_project', methods=['POST'])
@login_required
def archive_project():
    try:
        data = load_data()
        project_id = request.json['project_id']
        
        for project in data['projects']:
            if project['id'] == project_id:
                project['archived'] = True
                project['archived_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                project['archived_by'] = current_user.username
                break
        else:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        save_data(data)
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/restore_project', methods=['POST'])
@login_required
def restore_project():
    try:
        data = load_data()
        project_id = request.json['project_id']
        
        for project in data['projects']:
            if project['id'] == project_id:
                project['archived'] = False
                project.pop('archived_date', None)
                project.pop('archived_by', None)
                break
        else:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        save_data(data)
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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

@app.template_filter('format_date')
def format_date(date_string):
    if not date_string:
        return ''
    try:
        if len(date_string) == 10:  # YYYY-MM-DD format
            return date_string
        dt = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y-%m-%d')
    except:
        return date_string

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)