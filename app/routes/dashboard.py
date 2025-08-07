"""Dashboard and main navigation routes."""

from flask import Blueprint, render_template, request
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