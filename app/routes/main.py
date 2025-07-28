from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models.user import load_data

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def home():
    return render_template('home.html')

@main_bp.route('/dashboard')
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

@main_bp.route('/issues')
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

@main_bp.route('/board/<int:project_id>')
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