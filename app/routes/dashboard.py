"""Dashboard and main navigation routes."""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from app.services.data_service import load_data
from app.services.firebase_service import get_firestore_client

# Get database instance
db = get_firestore_client()


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def home():
    return render_template('home.html')


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    data = load_data(db)
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


@dashboard_bp.route('/issues')
@login_required
def issues_list():
    data = load_data(db)
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

    # Filter out archived projects
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    
    return render_template('issues.html', 
                         cards=cards, 
                         projects=active_projects,
                         project=project,
                         epics=epics,
                         stories=stories,
                         current_project_id=project_id)


@dashboard_bp.route('/backlog')
@login_required
def backlog():
    data = load_data(db)
    backlog_cards = [c for c in data['cards'] if c['status'] == 'todo']
    # Filter out archived projects
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('backlog.html', cards=backlog_cards, projects=active_projects)


@dashboard_bp.route('/stories')
@login_required
def stories():
    data = load_data(db)
    project_id = request.args.get('project_id', type=int)
    
    if project_id:
        stories = [s for s in data['stories'] if s['project_id'] == project_id]
        epics = [e for e in data['epics'] if e['project_id'] == project_id]
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
    else:
        stories = data['stories']
        epics = data['epics']
        project = None
    
    # Filter out archived projects
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    
    return render_template('stories.html', 
                         stories=stories, 
                         epics=epics,
                         projects=active_projects,
                         project=project,
                         current_project_id=project_id)


@dashboard_bp.route('/epics')
@login_required
def epics():
    data = load_data(db)
    project_id = request.args.get('project_id', type=int)
    
    if project_id:
        epics = [e for e in data['epics'] if e['project_id'] == project_id]
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
    else:
        epics = data['epics']
        project = None
    
    # Filter out archived projects
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    
    return render_template('epics.html', 
                         epics=epics, 
                         projects=active_projects,
                         project=project,
                         current_project_id=project_id)


@dashboard_bp.route('/analytics')
@login_required
def analytics():
    data = load_data(db)
    return render_template('analytics.html', load_data=load_data)


@dashboard_bp.route('/settings')
@login_required
def settings():
    data = load_data(db)
    # Filter out archived projects
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('settings.html', projects=active_projects, load_data=load_data)


@dashboard_bp.route('/archive')
@login_required
def archive():
    data = load_data(db)
    archived_projects = [p for p in data['projects'] if p.get('archived', False)]
    return render_template('archive.html', projects=archived_projects)


@dashboard_bp.route('/debug_load_data')
def debug_load_data():
    """Test the load_data function directly"""
    data = load_data(db)
    return jsonify({
        'users_count': len(data.get('users', [])),
        'projects_count': len(data.get('projects', [])),
        'cards_count': len(data.get('cards', [])),
        'users': data.get('users', []),
        'projects': data.get('projects', []),
        'data_keys': list(data.keys())
    })


@dashboard_bp.route('/gantt_debug')
def gantt_debug():
    """Debug version of gantt route without login requirement"""
    data = load_data(db)
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


@dashboard_bp.route('/firebase')
@login_required
def firebase_dashboard():
    data = load_data(db)
    stats = {
        'users_count': len(data['users']),
        'projects_count': len(data['projects']),
        'cards_count': len(data['cards']),
        'comments_count': len(data['comments'])
    }
    return render_template('firebase_dashboard.html', stats=stats)


@dashboard_bp.route('/firebase-status')
@login_required
def firebase_status():
    data = load_data(db)
    return jsonify({
        'success': True,
        'data': {
            'users_count': len(data['users']),
            'projects_count': len(data['projects']),
            'cards_count': len(data['cards']),
            'comments_count': len(data['comments'])
        }
    })


@dashboard_bp.route('/migrate-to-firebase')
@login_required
def migrate_to_firebase():
    try:
        data = load_data(db)
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