"""Project management routes including boards, gantt, and mindmap."""

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.services.data_service import load_data
from app.services.firebase_service import get_firestore_client

# Get database instance
db = get_firestore_client()


projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/board/<int:project_id>')
@login_required
def kanban_board(project_id):
    data = load_data(db)
    project = next((p for p in data['projects'] if p['id'] == project_id), None)
    if not project:
        return "Project not found", 404
    
    cards = [c for c in data['cards'] if c['project_id'] == project_id]
    todo_cards = [c for c in cards if c['status'] == 'todo']
    in_progress_cards = [c for c in cards if c['status'] == 'in_progress']
    done_cards = [c for c in cards if c['status'] == 'done']
    
    epics = [e for e in data['epics'] if e['project_id'] == project_id]
    stories = [s for s in data['stories'] if s['project_id'] == project_id]
    
    return render_template('board.html', 
                         project=project,
                         todo_cards=todo_cards,
                         in_progress_cards=in_progress_cards,
                         done_cards=done_cards,
                         epics=epics,
                         stories=stories)


@projects_bp.route('/gantt')
@login_required
def gantt():
    data = load_data(db)
    # Filter out archived projects
    projects = [p for p in data.get('projects', []) if not p.get('archived', False)]
    cards = data.get('cards', [])
    
    # Calculate project progress
    def get_project_progress(project_id):
        project_cards = [c for c in cards if c.get('project_id') == project_id]
        if not project_cards:
            return 0
        completed = len([c for c in project_cards if c.get('status') == 'done'])
        return round((completed / len(project_cards)) * 100, 1)
    
    # Add progress to projects
    for project in projects:
        project['progress'] = get_project_progress(project['id'])
    
    return render_template('gantt.html', projects=projects, cards=cards)


@projects_bp.route('/mindmap')
@login_required
def mindmap():
    data = load_data(db)
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    return render_template('mindmap.html', projects=active_projects)