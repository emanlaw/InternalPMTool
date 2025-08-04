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
    """Load data from Firebase or local files"""
    # Try to load from separate files first (fallback)
    try:
        from data_manager import DataManager
        dm = DataManager()
        local_data = dm.load_data()
    except:
        local_data = {'users': [], 'projects': [], 'epics': [], 'stories': [], 'cards': [], 'comments': [], 'notifications': []}
    
    data = {'users': [], 'projects': [], 'epics': [], 'stories': [], 'cards': [], 'comments': [], 'notifications': []}
    
    if db is None:
        print("ERROR: Firebase not initialized! Please check your firebase-service-account.json file.")
        print("You need to download the real service account key from Firebase Console.")
        return data
    
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
        
        # Load epics
        for project_doc in db.collection('projects').stream():
            project_id = int(project_doc.id)
            epics_ref = db.collection('projects').document(project_doc.id).collection('epics')
            for epic_doc in epics_ref.stream():
                epic_data = epic_doc.to_dict()
                epic_data['id'] = int(epic_doc.id)
                epic_data['project_id'] = project_id
                data['epics'].append(epic_data)
                
                # Load stories for this epic
                stories_ref = epics_ref.document(epic_doc.id).collection('stories')
                for story_doc in stories_ref.stream():
                    story_data = story_doc.to_dict()
                    story_data['id'] = int(story_doc.id)
                    story_data['epic_id'] = int(epic_doc.id)
                    story_data['project_id'] = project_id
                    data['stories'].append(story_data)
        
        # Load cards from stories/{storyId}/issues subcollection
        for project_doc in db.collection('projects').stream():
            project_id = int(project_doc.id)
            epics_ref = db.collection('projects').document(project_doc.id).collection('epics')
            for epic_doc in epics_ref.stream():
                epic_id = int(epic_doc.id)
                stories_ref = epics_ref.document(epic_doc.id).collection('stories')
                for story_doc in stories_ref.stream():
                    story_id = int(story_doc.id)
                    issues_ref = stories_ref.document(story_doc.id).collection('issues')
                    for issue_doc in issues_ref.stream():
                        card_data = issue_doc.to_dict()
                        card_data['id'] = int(issue_doc.id)
                        card_data['story_id'] = story_id
                        card_data['epic_id'] = epic_id
                        card_data['project_id'] = project_id
                        data['cards'].append(card_data)
                
                        # Load comments for this issue
                        comments_ref = issues_ref.document(issue_doc.id).collection('comments')
                        for comment_doc in comments_ref.stream():
                            comment_data = comment_doc.to_dict()
                            comment_data['id'] = int(comment_doc.id)
                            comment_data['card_id'] = int(issue_doc.id)
                            data['comments'].append(comment_data)
                    
        print(f"Loaded from Firebase: {len(data['users'])} users, {len(data['projects'])} projects, {len(data['cards'])} cards")
        
    except Exception as e:
        print(f"Firebase error: {e}")
    
    # Create default admin user if no users exist
    # If Firebase fails, use local data
    if not data['users'] and local_data['users']:
        data = local_data
        print(f"Using local data files: {len(data['users'])} users, {len(data['projects'])} projects")
    
    if not data['users']:
        default_admin = {
            'username': 'admin',
            'password_hash': generate_password_hash('admin123'),
            'email': 'admin@example.com',
            'display_name': 'Administrator',
            'role': 'admin',
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if db:
            try:
                db.collection('users').document('1').set(default_admin)
                print("Default admin user created in Firebase")
            except Exception as e:
                print(f"Error creating admin user in Firebase: {e}")
        
        data['users'].append({'id': 1, **default_admin})
        print("Default admin user created: admin/admin123")
    
    # Create default project if no projects exist
    if not data['projects']:
        default_project = {
            'name': 'Sample Project',
            'description': 'Your first project',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if db:
            try:
                db.collection('projects').document('1').set(default_project)
                print("Default project created in Firebase")
            except Exception as e:
                print(f"Error creating project in Firebase: {e}")
        
        data['projects'].append({'id': 1, **default_project})
        print("Default project created")
    
    return data

def save_data(data):
    """Save data to Firebase and local files"""
    # Always save to local files as backup
    try:
        from data_manager import DataManager
        dm = DataManager()
        dm.save_data(data)
    except Exception as e:
        print(f"Error saving to local files: {e}")
    
    if db is None:
        print("WARNING: Firebase not initialized! Data saved locally only.")
        return
    
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
        
        # Save epics to projects/{projectId}/epics subcollection
        for epic in data.get('epics', []):
            epic_copy = epic.copy()
            epic_copy.pop('id', None)
            epic_copy.pop('project_id', None)
            project_ref = db.collection('projects').document(str(epic['project_id']))
            project_ref.collection('epics').document(str(epic['id'])).set(epic_copy)
        
        # Save stories to projects/{projectId}/epics/{epicId}/stories subcollection
        for story in data.get('stories', []):
            story_copy = story.copy()
            story_copy.pop('id', None)
            story_copy.pop('epic_id', None)
            story_copy.pop('project_id', None)
            project_ref = db.collection('projects').document(str(story['project_id']))
            epic_ref = project_ref.collection('epics').document(str(story['epic_id']))
            epic_ref.collection('stories').document(str(story['id'])).set(story_copy)
        
        # Save cards to projects/{projectId}/epics/{epicId}/stories/{storyId}/issues subcollection
        for card in data.get('cards', []):
            card_copy = card.copy()
            card_copy.pop('id', None)
            card_copy.pop('story_id', None)
            card_copy.pop('epic_id', None)
            card_copy.pop('project_id', None)
            project_ref = db.collection('projects').document(str(card['project_id']))
            epic_ref = project_ref.collection('epics').document(str(card['epic_id']))
            story_ref = epic_ref.collection('stories').document(str(card['story_id']))
            story_ref.collection('issues').document(str(card['id'])).set(card_copy)
        
        # Save comments to projects/{projectId}/epics/{epicId}/stories/{storyId}/issues/{issueId}/comments
        for comment in data.get('comments', []):
            comment_copy = comment.copy()
            comment_copy.pop('id', None)
            card_id = comment_copy.pop('card_id')
            card = next((c for c in data.get('cards', []) if c['id'] == card_id), None)
            if card:
                project_ref = db.collection('projects').document(str(card['project_id']))
                epic_ref = project_ref.collection('epics').document(str(card['epic_id']))
                story_ref = epic_ref.collection('stories').document(str(card['story_id']))
                issue_ref = story_ref.collection('issues').document(str(card_id))
                issue_ref.collection('comments').document(str(comment['id'])).set(comment_copy)
                
        print("Data saved to Firebase successfully")
        
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
            # Debug: Print user data
            print(f"Debug - User data: {user_data}")
            print(f"Debug - Status: {user_data.get('status')}")
            
            # Check if user account is active
            if user_data.get('status') != 'active':
                status_messages = {
                    'pending': 'Your account is pending admin approval.',
                    'suspended': 'Your account has been suspended.',
                    'inactive': 'Your account is inactive.'
                }
                flash(f"Account status: {user_data.get('status')} - {status_messages.get(user_data.get('status'), 'Your account is not active.')}")
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
        epics = [e for e in data['epics'] if e['project_id'] == project_id]
        stories = [s for s in data['stories'] if s['project_id'] == project_id]
    else:
        cards = data['cards']
        project = None
        epics = data['epics']
        stories = data['stories']
    
    return render_template('issues.html', cards=cards, projects=data['projects'], epics=epics, stories=stories, current_project=project)

@app.route('/backlog')
@login_required
def backlog():
    data = load_data()
    backlog_cards = [c for c in data['cards'] if c['status'] == 'todo']
    return render_template('backlog.html', cards=backlog_cards, projects=data['projects'])

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
    
    return render_template('stories.html', epics=epics, stories=stories, projects=data['projects'], current_project=project)

@app.route('/epics')
@login_required
def epics():
    data = load_data()
    project_id = request.args.get('project_id', type=int)
    
    if project_id:
        epics = [e for e in data['epics'] if e['project_id'] == project_id]
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
    else:
        epics = data['epics']
        project = None
    
    return render_template('epics.html', epics=epics, projects=data['projects'], current_project=project)

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
    
    # Get epics and stories for context
    epics = [e for e in data['epics'] if e['project_id'] == project_id]
    stories = [s for s in data['stories'] if s['project_id'] == project_id]
    
    return render_template('kanban.html', 
                         project=project,
                         epics=epics,
                         stories=stories,
                         todo_cards=todo_cards,
                         in_progress_cards=in_progress_cards,
                         done_cards=done_cards)

@app.route('/api/add_epic', methods=['POST'])
@login_required
def add_epic():
    data = load_data()
    project_id = request.json['project_id']
    
    next_id = max([e['id'] for e in data['epics']], default=0) + 1
    
    new_epic = {
        'id': next_id,
        'project_id': project_id,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'status': 'active',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'created_by': current_user.username
    }
    
    data['epics'].append(new_epic)
    save_data(data)
    return jsonify(new_epic)

@app.route('/api/add_story', methods=['POST'])
@login_required
def add_story():
    data = load_data()
    epic_id = request.json['epic_id']
    epic = next((e for e in data['epics'] if e['id'] == epic_id), None)
    
    if not epic:
        return jsonify({'error': 'Epic not found'}), 404
    
    next_id = max([s['id'] for s in data['stories']], default=0) + 1
    
    new_story = {
        'id': next_id,
        'epic_id': epic_id,
        'project_id': epic['project_id'],
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'status': 'todo',
        'story_points': request.json.get('story_points', 0),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'created_by': current_user.username
    }
    
    data['stories'].append(new_story)
    save_data(data)
    return jsonify(new_story)

@app.route('/api/add_card', methods=['POST'])
@login_required
def add_card():
    data = load_data()
    story_id = request.json.get('story_id')
    
    if story_id:
        story = next((s for s in data['stories'] if s['id'] == story_id), None)
        if not story:
            return jsonify({'error': 'Story not found'}), 404
        project_id = story['project_id']
        epic_id = story['epic_id']
    else:
        # Legacy support for direct project cards
        project_id = request.json['project_id']
        story_id = None
        epic_id = None
    
    next_id = max([c['id'] for c in data['cards']], default=0) + 1
    
    new_card = {
        'id': next_id,
        'project_id': project_id,
        'epic_id': epic_id,
        'story_id': story_id,
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

@app.route('/api/get_epics/<int:project_id>')
@login_required
def get_epics(project_id):
    data = load_data()
    epics = [e for e in data['epics'] if e['project_id'] == project_id]
    return jsonify(epics)

@app.route('/api/get_stories/<int:epic_id>')
@login_required
def get_stories(epic_id):
    data = load_data()
    stories = [s for s in data['stories'] if s['epic_id'] == epic_id]
    return jsonify(stories)

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

@app.route('/api/notifications')
@login_required
def get_notifications():
    data = load_data()
    user_notifications = [n for n in data.get('notifications', []) if n['user_id'] == current_user.id]
    return jsonify(user_notifications)

@app.route('/api/notifications/mark_read', methods=['POST'])
@login_required
def mark_notification_read():
    data = load_data()
    notification_id = request.json['notification_id']
    
    for notification in data.get('notifications', []):
        if notification['id'] == notification_id and notification['user_id'] == current_user.id:
            notification['read'] = True
            break
    
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/activity_feed')
@login_required
def activity_feed():
    data = load_data()
    activities = []
    
    # Recent card updates
    for card in data['cards'][-10:]:  # Last 10 cards
        activities.append({
            'type': 'card_created',
            'message': f'Card "{card["title"]}" was created',
            'timestamp': card.get('created_at', ''),
            'card_id': card['id']
        })
    
    # Recent comments
    for comment in data.get('comments', [])[-10:]:  # Last 10 comments
        card = next((c for c in data['cards'] if c['id'] == comment['card_id']), None)
        if card:
            activities.append({
                'type': 'comment_added',
                'message': f'{comment["author"]} commented on "{card["title"]}"',
                'timestamp': comment['created_at'],
                'card_id': card['id']
            })
    
    # Sort by timestamp
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(activities[:20])  # Return last 20 activities

@app.route('/api/team_members')
@login_required
def get_team_members():
    data = load_data()
    team_members = [{'id': u['id'], 'username': u['username']} for u in data['users']]
    return jsonify(team_members)

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
        content = request.json['content']
        mentions = extract_mentions(content)
        
        new_comment = {
            'id': max([c['id'] for c in data.get('comments', [])], default=0) + 1,
            'card_id': card_id,
            'author': current_user.username,
            'content': content,
            'mentions': mentions,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        if 'comments' not in data:
            data['comments'] = []
        data['comments'].append(new_comment)
        
        # Create notifications for mentioned users
        create_mention_notifications(mentions, card_id, current_user.username)
        
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
    
    # Simple sprint data structure for now
    all_sprints = []
    active_sprints = []
    completed_sprints = []
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    
    return render_template('sprints.html', 
                         sprints=all_sprints,
                         active_sprints=active_sprints,
                         completed_sprints=completed_sprints,
                         projects=active_projects)

@app.route('/sprints/<int:sprint_id>')
@login_required
def sprint_detail(sprint_id):
    # Placeholder for sprint detail - will implement later
    return "Sprint detail page - Coming soon!", 200

# Sprint API Routes
@app.route('/api/sprints', methods=['POST'])
@login_required
def create_sprint():
    try:
        # Placeholder for sprint creation - will implement later
        return jsonify({'success': True, 'message': 'Sprint creation coming soon!'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/start', methods=['POST'])
@login_required
def start_sprint(sprint_id):
    try:
        return jsonify({'success': True, 'message': 'Sprint start coming soon!'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/complete', methods=['POST'])
@login_required
def complete_sprint(sprint_id):
    try:
        return jsonify({'success': True, 'message': 'Sprint completion coming soon!'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/issues', methods=['POST'])
@login_required
def add_issue_to_sprint(sprint_id):
    try:
        return jsonify({'success': True, 'message': 'Issue assignment coming soon!'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/issues/<int:issue_id>', methods=['DELETE'])
@login_required
def remove_issue_from_sprint(sprint_id, issue_id):
    try:
        return jsonify({'success': True, 'message': 'Issue removal coming soon!'})
            
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

def extract_mentions(content):
    """Extract @mentions from comment content"""
    import re
    mentions = re.findall(r'@(\w+)', content)
    return list(set(mentions))  # Remove duplicates

def create_mention_notifications(mentions, card_id, author):
    """Create notifications for mentioned users"""
    data = load_data()
    
    for username in mentions:
        # Check if user exists
        user = next((u for u in data['users'] if u['username'] == username), None)
        if user:
            notification = {
                'id': max([n.get('id', 0) for n in data.get('notifications', [])], default=0) + 1,
                'user_id': user['id'],
                'type': 'mention',
                'message': f'{author} mentioned you in a comment',
                'card_id': card_id,
                'read': False,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if 'notifications' not in data:
                data['notifications'] = []
            data['notifications'].append(notification)
    
    save_data(data)

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