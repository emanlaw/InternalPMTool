from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models.user import load_data

main_bp = Blueprint('main', __name__)

def load_firebase_data():
    """Load data from Firebase or fallback to JSON"""
    try:
        from app.services.firebase_service import firebase_service
        from config.firebase_config import firebase_config
        
        if firebase_config.db is not None:
            # Load from Firebase
            projects = firebase_service.get_all_projects()
            cards = firebase_service.get_all_cards()
            
            # Convert Firebase data to match JSON structure
            for project in projects:
                if isinstance(project.get('id'), str) and project['id'].startswith('PROJ-'):
                    # Convert PROJ-001 to integer for compatibility
                    project['id'] = int(project['id'].split('-')[1])
            
            for card in cards:
                if isinstance(card.get('id'), str) and card['id'].startswith('CARD-'):
                    # Convert CARD-001 to integer for compatibility
                    card['id'] = int(card['id'].split('-')[1])
                if isinstance(card.get('project_id'), str):
                    if card['project_id'].startswith('PROJ-'):
                        card['project_id'] = int(card['project_id'].split('-')[1])
                    else:
                        card['project_id'] = int(card['project_id'])
            
            return {
                'projects': projects,
                'cards': cards,
                'users': [],  # Users handled separately
                'comments': []
            }
        else:
            # Fallback to JSON
            return load_data()
    except Exception as e:
        print(f"Error loading Firebase data: {e}")
        return load_data()

@main_bp.route('/')
@login_required
def home():
    return render_template('home.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    data = load_firebase_data()
    all_cards = data['cards']
    stats = {
        'todo': len([c for c in all_cards if c['status'] == 'todo']),
        'in_progress': len([c for c in all_cards if c['status'] == 'in_progress']),
        'done': len([c for c in all_cards if c['status'] == 'done']),
        'total': len(all_cards)
    }
    return render_template('dashboard.html', projects=data['projects'], stats=stats)

@main_bp.route('/issues')
@login_required
def issues_list():
    data = load_firebase_data()
    project_id = request.args.get('project_id', type=int)
    
    if project_id:
        cards = [c for c in data['cards'] if c['project_id'] == project_id]
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
    else:
        cards = data['cards']
        project = None
    
    return render_template('issues.html', cards=cards, projects=data['projects'], current_project=project)

@main_bp.route('/board/<int:project_id>')
@login_required
def kanban_board(project_id):
    data = load_firebase_data()
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

@main_bp.route('/backlog')
@login_required
def backlog():
    data = load_firebase_data()
    project_id = request.args.get('project_id', type=int)
    
    # Filter for backlog items (todo status)
    if project_id:
        cards = [c for c in data['cards'] if c['project_id'] == project_id and c['status'] == 'todo']
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
    else:
        cards = [c for c in data['cards'] if c['status'] == 'todo']
        project = None
    
    return render_template('backlog.html', cards=cards, projects=data['projects'], current_project=project)

@main_bp.route('/analytics')
@login_required
def gantt_analytics():
    """Gantt Chart Analytics Dashboard"""
    return render_template('gantt_analytics.html')