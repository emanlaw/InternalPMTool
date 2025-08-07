"""Sprint management routes - both UI and API endpoints."""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from app.services.data_service import load_data, save_data
from app.services.firebase_service import get_firestore_client

# Get database instance
db = get_firestore_client()

sprints_bp = Blueprint('sprints', __name__)


@sprints_bp.route('/sprints')
@login_required
def sprints():
    data = load_data(db)
    
    all_sprints = data.get('sprints', [])
    active_sprints = [s for s in all_sprints if s.get('status') == 'active']
    completed_sprints = [s for s in all_sprints if s.get('status') == 'completed']
    active_projects = [p for p in data['projects'] if not p.get('archived', False)]
    
    return render_template('sprints.html', 
                         sprints=all_sprints,
                         active_sprints=active_sprints,
                         completed_sprints=completed_sprints,
                         projects=active_projects)


@sprints_bp.route('/sprints/<int:sprint_id>')
@login_required
def sprint_detail(sprint_id):
    # Placeholder for sprint detail - will implement later
    return "Sprint detail page - Coming soon!", 200


# Sprint API Routes
@sprints_bp.route('/api/sprints', methods=['POST'])
@login_required
def create_sprint():
    try:
        data = load_data(db)
        
        name = request.json.get('name')
        description = request.json.get('description', '')
        project_id = request.json.get('project_id')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        
        if not name or not project_id:
            return jsonify({'success': False, 'error': 'Name and project are required'})
        
        # Get next sprint ID
        sprint_id = max([s.get('id', 0) for s in data.get('sprints', [])], default=0) + 1
        
        sprint = {
            'id': sprint_id,
            'name': name,
            'description': description,
            'project_id': project_id,
            'start_date': start_date,
            'end_date': end_date,
            'status': 'planning',
            'created_by': current_user.username,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'items': []
        }
        
        if 'sprints' not in data:
            data['sprints'] = []
        
        data['sprints'].append(sprint)
        save_data(data, db)
        
        return jsonify({'success': True, 'sprint': sprint})
        
    except Exception as e:
        print(f"Error creating sprint: {e}")
        return jsonify({'success': False, 'error': str(e)})


@sprints_bp.route('/api/sprints/<int:sprint_id>/start', methods=['POST'])
@login_required
def start_sprint(sprint_id):
    try:
        data = load_data(db)
        
        sprint = next((s for s in data.get('sprints', []) if s['id'] == sprint_id), None)
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'})
        
        if sprint.get('status') == 'active':
            return jsonify({'success': False, 'error': 'Sprint is already active'})
        
        # Check if there's already an active sprint for this project
        project_id = sprint.get('project_id')
        active_sprint = next((s for s in data.get('sprints', []) 
                             if s.get('project_id') == project_id and s.get('status') == 'active'), None)
        
        if active_sprint:
            return jsonify({'success': False, 'error': 'There is already an active sprint for this project'})
        
        # Start the sprint
        sprint['status'] = 'active'
        sprint['started_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sprint['started_by'] = current_user.username
        
        save_data(data, db)
        
        return jsonify({'success': True, 'message': 'Sprint started successfully'})
        
    except Exception as e:
        print(f"Error starting sprint: {e}")
        return jsonify({'success': False, 'error': str(e)})


@sprints_bp.route('/api/sprints/<int:sprint_id>/complete', methods=['POST'])
@login_required
def complete_sprint(sprint_id):
    try:
        data = load_data(db)
        
        sprint = next((s for s in data.get('sprints', []) if s['id'] == sprint_id), None)
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'})
        
        if sprint.get('status') != 'active':
            return jsonify({'success': False, 'error': 'Only active sprints can be completed'})
        
        # Complete the sprint
        sprint['status'] = 'completed'
        sprint['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sprint['completed_by'] = current_user.username
        
        save_data(data, db)
        
        return jsonify({'success': True, 'message': 'Sprint completed successfully'})
        
    except Exception as e:
        print(f"Error completing sprint: {e}")
        return jsonify({'success': False, 'error': str(e)})


@sprints_bp.route('/api/sprints/<int:sprint_id>/items', methods=['GET'])
@login_required
def get_sprint_items(sprint_id):
    try:
        data = load_data(db)
        
        sprint = next((s for s in data.get('sprints', []) if s['id'] == sprint_id), None)
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'})
        
        # Get sprint items (stories, epics, cards)
        items = sprint.get('items', [])
        
        # Enrich items with full data
        enriched_items = []
        for item in items:
            item_type = item.get('type')
            item_id = item.get('id')
            
            if item_type == 'epic':
                epic = next((e for e in data.get('epics', []) if e['id'] == item_id), None)
                if epic:
                    enriched_items.append({'type': 'epic', 'data': epic})
            elif item_type == 'story':
                story = next((s for s in data.get('stories', []) if s['id'] == item_id), None)
                if story:
                    enriched_items.append({'type': 'story', 'data': story})
            elif item_type == 'card':
                card = next((c for c in data.get('cards', []) if c['id'] == item_id), None)
                if card:
                    enriched_items.append({'type': 'card', 'data': card})
        
        return jsonify({'success': True, 'items': enriched_items})
        
    except Exception as e:
        print(f"Error getting sprint items: {e}")
        return jsonify({'success': False, 'error': str(e)})


@sprints_bp.route('/api/sprints/<int:sprint_id>/items', methods=['POST'])
@login_required
def add_sprint_item(sprint_id):
    try:
        data = load_data(db)
        
        sprint = next((s for s in data.get('sprints', []) if s['id'] == sprint_id), None)
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'})
        
        item_type = request.json.get('type')  # 'epic', 'story', 'card'
        item_id = request.json.get('id')
        
        if not item_type or not item_id:
            return jsonify({'success': False, 'error': 'Type and ID are required'})
        
        # Check if item exists
        item_data = None
        if item_type == 'epic':
            item_data = next((e for e in data.get('epics', []) if e['id'] == item_id), None)
        elif item_type == 'story':
            item_data = next((s for s in data.get('stories', []) if s['id'] == item_id), None)
        elif item_type == 'card':
            item_data = next((c for c in data.get('cards', []) if c['id'] == item_id), None)
        
        if not item_data:
            return jsonify({'success': False, 'error': f'{item_type.title()} not found'})
        
        # Add to sprint items
        if 'items' not in sprint:
            sprint['items'] = []
        
        # Check if already in sprint
        existing = next((i for i in sprint['items'] if i['type'] == item_type and i['id'] == item_id), None)
        if existing:
            return jsonify({'success': False, 'error': f'{item_type.title()} already in sprint'})
        
        sprint['items'].append({
            'type': item_type,
            'id': item_id,
            'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'added_by': current_user.username
        })
        
        save_data(data, db)
        
        return jsonify({'success': True, 'message': f'{item_type.title()} added to sprint'})
        
    except Exception as e:
        print(f"Error adding sprint item: {e}")
        return jsonify({'success': False, 'error': str(e)})


# Additional sprint API routes can be added here as needed