"""
Simple Flask app using modular structure.

This is the new minimal app.py that uses the modular structure.
For the original monolithic app, see app_original.py.
"""



from flask import request, redirect, url_for, render_template, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from app.models.user import User
from datetime import datetime, date
PREDEFINED_LABELS = [
    {'id': 'bug', 'name': 'Bug', 'color': '#ff5630'},
    {'id': 'feature', 'name': 'Feature', 'color': '#0052cc'},
    {'id': 'urgent', 'name': 'Urgent', 'color': '#ff8b00'},
    {'id': 'enhancement', 'name': 'Enhancement', 'color': '#36b37e'}
]
from werkzeug.security import generate_password_hash
from app import create_app
try:
    from app.services.firebase_service import get_firestore_client
    db = get_firestore_client()
except Exception:
    db = None

# Create the Flask application using the app factory
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)



def load_data():
    """Load data from Firebase or local files"""
    data = {'users': [], 'projects': [], 'epics': [], 'stories': [], 'cards': [], 'comments': [], 'notifications': [], 'sprints': []}
    
    if db is None:
        print("ERROR: Firebase not initialized! Please check your firebase-service-account.json file.")
        print("You need to download the real service account key from Firebase Console.")
        print("Falling back to local data files...")
        # Try to load from local files
        try:
            from data_manager import DataManager
            dm = DataManager()
            local_data = dm.load_data()
            if local_data and local_data.get('users'):
                print(f"Using local data: {len(local_data['users'])} users, {len(local_data.get('projects', []))} projects")
                return local_data
        except Exception as e:
            print(f"Error loading local data: {e}")
        
        # If local data fails, try data.json directly
        try:
            import json
            with open('data.json', 'r') as f:
                local_data = json.load(f)
                if local_data and local_data.get('users'):
                    print(f"Using data.json: {len(local_data['users'])} users, {len(local_data.get('projects', []))} projects")
                    return local_data
        except Exception as e:
            print(f"Error loading data.json: {e}")
        
        return data
    
    try:
        # Load from Firebase collections
        for doc in db.collection('users').stream():
            user_data = doc.to_dict()
            user_data['id'] = int(doc.id)
            data['users'].append(user_data)
        
        for doc in db.collection('projects').stream():
            project_data = doc.to_dict()
            try:
                project_data['id'] = int(doc.id)
                data['projects'].append(project_data)
            except ValueError:
                print(f"Skipping project with non-numeric ID: {doc.id}")
                continue
        
        # Load epics
        for project_doc in db.collection('projects').stream():
            try:
                project_id = int(project_doc.id)
            except ValueError:
                continue
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
        
        # Load sprints
        for doc in db.collection('sprints').stream():
            sprint_data = doc.to_dict()
            sprint_data['id'] = int(doc.id)
            data['sprints'].append(sprint_data)
        
        # Load cards from stories/{storyId}/issues subcollection
        for project_doc in db.collection('projects').stream():
            try:
                project_id = int(project_doc.id)
            except ValueError:
                continue
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
                    
        print(f"Loaded from Firebase: {len(data['users'])} users, {len(data['projects'])} projects, {len(data['cards'])} cards, {len(data['sprints'])} sprints")
        
    except Exception as e:
        print(f"Firebase error: {e}")
    
    # Create default admin user if no users exist
    # If Firebase fails or has no data, use local files
    print(f"Debug - Checking users count: {len(data['users'])}")
    if not data['users']:
        print("Debug - No users found, trying local fallback")
        try:
            from data_manager import DataManager
            dm = DataManager()
            local_data = dm.load_data()
            print(f"Debug - Local data manager loaded: {len(local_data.get('users', []))} users")
            if local_data['users']:
                data = local_data
                print(f"Using local data files: {len(data['users'])} users, {len(data['projects'])} projects, {len(data.get('epics', []))} epics, {len(data.get('stories', []))} stories, {len(data.get('sprints', []))} sprints")
        except Exception as e:
            print(f"Error loading local data: {e}")
            print("Debug - Exception in local data loading, trying data.json fallback")
            # Try the main data.json file as final fallback
            try:
                with open('data.json', 'r') as f:
                    json_data = json.load(f)
                    data = json_data
                    print(f"Using data.json fallback: {len(data.get('users', []))} users, {len(data.get('projects', []))} projects")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading data.json fallback: {e}")
    else:
        print(f"Debug - Using Firebase data with {len(data['users'])} users")
    
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
        
        # Save sprints to Firebase
        for sprint in data.get('sprints', []):
            sprint_copy = sprint.copy()
            sprint_copy.pop('id', None)
            db.collection('sprints').document(str(sprint['id'])).set(sprint_copy)
        
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
    # from app_modules.services.user_service import UserService  # REMOVED: not in modular structure
        

        # Validation
        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long')
            return render_template('register.html')

        # Create user through service
        # result = UserService.create_user(username, email, display_name, password)
        result = {'success': True, 'message': 'User created successfully'}  # Placeholder

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
    
    # from app_modules.services.user_service import UserService  # REMOVED: not in modular structure
    
    # Get filter parameters
    status_filter = request.args.get('status', '')
    role_filter = request.args.get('role', '')
    search_query = request.args.get('search', '')
    
    # Get filtered users
    users = []  # Placeholder for user list
    stats = []  # Placeholder for user stats
    
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
    
    # from app_modules.services.user_service import UserService  # REMOVED: not in modular structure
    
    user_id = request.json.get('user_id')
    new_status = request.json.get('status')
    
    result = {'success': True}  # Placeholder for update status
    return jsonify(result)

@app.route('/admin/users/update_role', methods=['POST'])
@login_required
def admin_update_user_role():
    if not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # from app_modules.services.user_service import UserService  # REMOVED: not in modular structure
    
    user_id = request.json.get('user_id')
    new_role = request.json.get('role')
    
    result = {'success': True}  # Placeholder for update role
    return jsonify(result)

@app.route('/admin/users/bulk_update', methods=['POST'])
@login_required
def admin_bulk_update_users():
    if not current_user.is_admin():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # from app_modules.services.user_service import UserService  # REMOVED: not in modular structure
    
    user_ids = request.json.get('user_ids', [])
    action = request.json.get('action')
    
    result = {'success': True}  # Placeholder for bulk update
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
    
    # Filter out archived projects for the dropdown
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('issues.html', cards=cards, projects=active_projects, epics=epics, stories=stories, current_project=project)

@app.route('/backlog')
@login_required
def backlog():
    data = load_data()
    backlog_cards = [c for c in data['cards'] if c['status'] == 'todo']
    # Filter out archived projects
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
    
    # Filter out archived projects
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('stories.html', epics=epics, stories=stories, projects=active_projects, current_project=project)

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
    
    # Filter out archived projects
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('epics.html', epics=epics, projects=active_projects, current_project=project)

@app.route('/analytics')
@login_required
def analytics():
    data = load_data()
    # Filter out archived projects
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('gantt_analytics.html', projects=active_projects, cards=data['cards'])

@app.route('/debug_load_data')
def debug_load_data():
    """Test the load_data function directly"""
    data = load_data()
    return jsonify({
        'users_count': len(data.get('users', [])),
        'projects_count': len(data.get('projects', [])),
        'cards_count': len(data.get('cards', [])),
        'users': data.get('users', []),
        'projects': data.get('projects', []),
        'data_keys': list(data.keys())
    })

@app.route('/gantt_debug')
def gantt_debug():
    """Debug version of gantt route without login requirement"""
    data = load_data()
    print(f"Debug - All projects from data: {data.get('projects', [])}")
    
    # Filter out archived projects
    projects = [p for p in data.get('projects', []) if not p.get('archived', False)]
    cards = data.get('cards', [])
    
    print(f"Debug - Projects after filtering: {projects}")
    print(f"Debug - Cards: {cards}")
    
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

@app.route('/gantt')
@login_required
def gantt():
    data = load_data()
    # Filter out archived projects
    projects = [p for p in data.get('projects', []) if not p.get('archived', False)]
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
    
    # Get parameters from request
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
        'story_points': request.json.get('story_points'),
        'labels': request.json.get('labels', [])  # Add support for labels
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
    try:
        data = load_data()
        print(f"DEBUG get_epics: project_id={project_id}, total_epics={len(data.get('epics', []))}")
        epics = [e for e in data['epics'] if e['project_id'] == project_id]
        print(f"DEBUG get_epics: filtered_epics={epics}")
        return jsonify(epics)
    except Exception as e:
        print(f"ERROR in get_epics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_stories/<int:epic_id>')
@login_required
def get_stories(epic_id):
    try:
        data = load_data()
        print(f"DEBUG get_stories: epic_id={epic_id}, total_stories={len(data.get('stories', []))}")
        stories = [s for s in data['stories'] if s['epic_id'] == epic_id]
        print(f"DEBUG get_stories: filtered_stories={stories}")
        return jsonify(stories)
    except Exception as e:
        print(f"ERROR in get_stories: {e}")
        return jsonify({'error': str(e)}), 500

# Test endpoints without authentication
@app.route('/api/test/epics/<int:project_id>')
def test_get_epics(project_id):
    try:
        data = load_data()
        epics = [e for e in data['epics'] if e['project_id'] == project_id]
        return jsonify({'success': True, 'epics': epics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/test/stories/<int:epic_id>')
def test_get_stories(epic_id):
    try:
        data = load_data()
        stories = [s for s in data['stories'] if s['epic_id'] == epic_id]
        return jsonify({'success': True, 'stories': stories})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

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
    label_filter = request.args.get('label', '')
    
    filtered_cards = cards
    
    if project_filter:
        filtered_cards = [c for c in filtered_cards if c['project_id'] == int(project_filter)]
    
    if status_filter:
        filtered_cards = [c for c in filtered_cards if c['status'] == status_filter]
    
    if priority_filter:
        filtered_cards = [c for c in filtered_cards if c['priority'] == priority_filter]
    
    if assignee_filter:
        filtered_cards = [c for c in filtered_cards if c.get('assignee', '').lower() == assignee_filter.lower()]
    
    if label_filter:
        filtered_cards = [c for c in filtered_cards if label_filter in c.get('labels', [])]
    
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
            if 'labels' in updates:
                card['labels'] = updates['labels']
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
    
    all_sprints = data.get('sprints', [])
    active_sprints = [s for s in all_sprints if s.get('status') == 'active']
    completed_sprints = [s for s in all_sprints if s.get('status') == 'completed']
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
        data = load_data()
        
        next_id = max([s['id'] for s in data.get('sprints', [])], default=0) + 1
        
        new_sprint = {
            'id': next_id,
            'name': request.json['name'],
            'project_id': int(request.json['project_id']),
            'start_date': request.json['start_date'],
            'end_date': request.json['end_date'],
            'goal': request.json.get('goal', ''),
            'story_points': int(request.json.get('story_points', 0)),
            'status': 'planning',
            'issues': [],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': current_user.username
        }
        
        if 'sprints' not in data:
            data['sprints'] = []
        data['sprints'].append(new_sprint)
        save_data(data)
        
        return jsonify({'success': True, 'sprint': new_sprint})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/start', methods=['POST'])
@login_required
def start_sprint(sprint_id):
    try:
        data = load_data()
        
        # Find the sprint
        sprint = None
        for s in data.get('sprints', []):
            if s['id'] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'}), 404
        
        if sprint['status'] != 'planning':
            return jsonify({'success': False, 'error': 'Can only start sprints in planning status'}), 400
        
        # Validate start date is not in the past
        from datetime import datetime, date
        start_date = datetime.strptime(sprint['start_date'], '%Y-%m-%d').date()
        if start_date < date.today():
            return jsonify({'success': False, 'error': 'Cannot start sprint with past start date'}), 400
        
        # Update sprint status
        sprint['status'] = 'active'
        sprint['started_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sprint['started_by'] = current_user.username
        
        save_data(data)
        return jsonify({'success': True, 'sprint': sprint})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/complete', methods=['POST'])
@login_required
def complete_sprint(sprint_id):
    try:
        data = load_data()
        
        # Find the sprint
        sprint = None
        for s in data.get('sprints', []):
            if s['id'] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'}), 404
        
        if sprint['status'] != 'active':
            return jsonify({'success': False, 'error': 'Can only complete active sprints'}), 400
        
        # Update sprint status
        sprint['status'] = 'completed'
        sprint['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sprint['completed_by'] = current_user.username
        
        save_data(data)
        return jsonify({'success': True, 'sprint': sprint})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/issues', methods=['POST'])
@login_required
def add_issue_to_sprint(sprint_id):
    try:
        data = load_data()
        
        # Find the sprint
        sprint = None
        for s in data.get('sprints', []):
            if s['id'] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'}), 404
        
        issue_id = request.json.get('issue_id')
        if not issue_id:
            return jsonify({'success': False, 'error': 'Issue ID is required'}), 400
        
        # Add issue to sprint if not already present
        if 'issues' not in sprint:
            sprint['issues'] = []
        
        if issue_id not in sprint['issues']:
            sprint['issues'].append(issue_id)
        
        save_data(data)
        return jsonify({'success': True, 'sprint': sprint})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/items', methods=['GET'])
@login_required
def get_sprint_items(sprint_id):
    try:
        data = load_data()
        
        # Find the sprint
        sprint = None
        for s in data.get('sprints', []):
            if s['id'] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'}), 404
        
        # Get epics, stories, and issues for this sprint
        epics = []
        stories = []
        issues = []
        
        # If sprint has assigned items, get them
        if 'epics' in sprint:
            epics = [e for e in data.get('epics', []) if e['id'] in sprint['epics']]
        if 'stories' in sprint:
            stories = [s for s in data.get('stories', []) if s['id'] in sprint['stories']]
        if 'issues' in sprint:
            issues = [c for c in data.get('cards', []) if c['id'] in sprint['issues']]
        
        return jsonify({
            'success': True,
            'sprint': sprint,
            'epics': epics,
            'stories': stories,
            'issues': issues
        })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/items', methods=['POST'])
@login_required
def add_items_to_sprint(sprint_id):
    try:
        data = load_data()
        
        # Find the sprint
        sprint = None
        for s in data.get('sprints', []):
            if s['id'] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'}), 404
        
        epic_ids = request.json.get('epic_ids', [])
        story_ids = request.json.get('story_ids', [])
        issue_ids = request.json.get('issue_ids', [])
        
        # Initialize sprint collections if they don't exist
        if 'epics' not in sprint:
            sprint['epics'] = []
        if 'stories' not in sprint:
            sprint['stories'] = []
        if 'issues' not in sprint:
            sprint['issues'] = []
        
        # Add items to sprint
        for epic_id in epic_ids:
            if epic_id not in sprint['epics']:
                sprint['epics'].append(epic_id)
        
        for story_id in story_ids:
            if story_id not in sprint['stories']:
                sprint['stories'].append(story_id)
        
        for issue_id in issue_ids:
            if issue_id not in sprint['issues']:
                sprint['issues'].append(issue_id)
        
        save_data(data)
        return jsonify({'success': True, 'sprint': sprint})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>/items/<item_type>/<int:item_id>', methods=['DELETE'])
@login_required
def remove_item_from_sprint(sprint_id, item_type, item_id):
    try:
        data = load_data()
        
        # Find the sprint
        sprint = None
        for s in data.get('sprints', []):
            if s['id'] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'}), 404
        
        # Remove item based on type
        if item_type == 'epic' and 'epics' in sprint and item_id in sprint['epics']:
            sprint['epics'].remove(item_id)
        elif item_type == 'story' and 'stories' in sprint and item_id in sprint['stories']:
            sprint['stories'].remove(item_id)
        elif item_type == 'issue' and 'issues' in sprint and item_id in sprint['issues']:
            sprint['issues'].remove(item_id)
        
        save_data(data)
        return jsonify({'success': True, 'sprint': sprint})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/sprints/<int:sprint_id>', methods=['PUT'])
@login_required
def update_sprint(sprint_id):
    try:
        data = load_data()
        
        # Find the sprint
        sprint = None
        for s in data.get('sprints', []):
            if s['id'] == sprint_id:
                sprint = s
                break
        
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'}), 404
        
        # Update sprint details
        if 'name' in request.json:
            sprint['name'] = request.json['name']
        if 'goal' in request.json:
            sprint['goal'] = request.json['goal']
        if 'story_points' in request.json:
            sprint['story_points'] = int(request.json['story_points'])
        if 'start_date' in request.json:
            sprint['start_date'] = request.json['start_date']
        if 'end_date' in request.json:
            sprint['end_date'] = request.json['end_date']
        
        sprint['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sprint['updated_by'] = current_user.username
        
        save_data(data)
        return jsonify({'success': True, 'sprint': sprint})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/projects/<int:project_id>/hierarchy', methods=['GET'])
@login_required
def get_project_hierarchy(project_id):
    try:
        data = load_data()
        
        # Get project epics
        epics = [e for e in data.get('epics', []) if e.get('project_id') == project_id]
        
        # For each epic, get its stories and issues
        for epic in epics:
            epic['stories'] = [s for s in data.get('stories', []) if s.get('epic_id') == epic['id']]
            
            # For each story, get its issues
            for story in epic['stories']:
                story['issues'] = [c for c in data.get('cards', []) if c.get('story_id') == story['id']]
        
        # Get orphaned stories (stories without epic)
        orphaned_stories = [s for s in data.get('stories', []) 
                           if s.get('project_id') == project_id and 
                           not any(e['id'] == s.get('epic_id') for e in epics)]
        
        # Get orphaned issues (issues without story)
        orphaned_issues = [c for c in data.get('cards', []) 
                          if c.get('project_id') == project_id and 
                          not any(s['id'] == c.get('story_id') for s in data.get('stories', []))]
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'epics': epics,
            'orphaned_stories': orphaned_stories,
            'orphaned_issues': orphaned_issues
        })
            
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

@app.route('/api/sprints/<int:sprint_id>', methods=['DELETE'])
@login_required
def delete_sprint(sprint_id):
    """Delete a sprint and remove all item assignments"""
    try:
        data = load_data()
        
        # Find the sprint to delete
        sprint = next((s for s in data['sprints'] if s['id'] == sprint_id), None)
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'})
        
        # Check if sprint can be deleted (optional business rule)
        if sprint.get('status') == 'active':
            return jsonify({
                'success': False, 
                'error': 'Cannot delete an active sprint. Please complete or stop the sprint first.'
            })
        
        # Remove sprint from the list
        data['sprints'] = [s for s in data['sprints'] if s['id'] != sprint_id]
        
        # Remove sprint assignments from all items
        # Remove from epics
        for epic in data['epics']:
            if 'sprint_ids' in epic and sprint_id in epic['sprint_ids']:
                epic['sprint_ids'].remove(sprint_id)
        
        # Remove from stories  
        for story in data['stories']:
            if 'sprint_ids' in story and sprint_id in story['sprint_ids']:
                story['sprint_ids'].remove(sprint_id)
        
        # Remove from cards/issues
        for card in data['cards']:
            if 'sprint_ids' in card and sprint_id in card['sprint_ids']:
                card['sprint_ids'].remove(sprint_id)
        
        # Save the updated data
        save_data(data)
        
        return jsonify({
            'success': True, 
            'message': f'Sprint "{sprint["name"]}" has been deleted successfully'
        })
        
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
    format_timestamp=format_timestamp,
    predefined_labels=PREDEFINED_LABELS,
    get_label_by_id=lambda label_id: next((label for label in PREDEFINED_LABELS if label['id'] == label_id), None)
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