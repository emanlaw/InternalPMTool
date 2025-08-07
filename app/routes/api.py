"""General API routes for various functionality."""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from app.services.data_service import load_data, save_data
from app.services.firebase_service import get_firestore_client
from app.utils.helpers import extract_mentions
from app.services.notification_service import create_mention_notifications

# Get database instance
db = get_firestore_client()

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/save_mindmap', methods=['POST'])
@login_required
def save_mindmap():
    try:
        data = load_data(db)
        project_id = request.json.get('project_id')
        nodes = request.json.get('nodes', [])
        connections = request.json.get('connections', [])
        
        # Find project and save mindmap data
        for project in data['projects']:
            if project['id'] == project_id:
                project['mindmap_nodes'] = nodes
                project['mindmap_connections'] = connections
                project['mindmap_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                break
        
        save_data(data, db)
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Error saving mindmap: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/load_mindmap/<int:project_id>')
@login_required
def load_mindmap(project_id):
    try:
        data = load_data(db)
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
        
        if project:
            return jsonify({
                'success': True,
                'nodes': project.get('mindmap_nodes', []),
                'connections': project.get('mindmap_connections', [])
            })
        else:
            return jsonify({'success': False, 'error': 'Project not found'})
            
    except Exception as e:
        print(f"Error loading mindmap: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/add_epic', methods=['POST'])
@login_required
def add_epic():
    try:
        data = load_data(db)
        project_id = request.json.get('project_id')
        name = request.json.get('name')
        description = request.json.get('description', '')
        
        if not name or not project_id:
            return jsonify({'success': False, 'error': 'Name and project ID are required'})
        
        # Get next epic ID
        epic_id = max([e.get('id', 0) for e in data.get('epics', [])], default=0) + 1
        
        epic = {
            'id': epic_id,
            'name': name,
            'description': description,
            'project_id': project_id,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': current_user.username
        }
        
        if 'epics' not in data:
            data['epics'] = []
        
        data['epics'].append(epic)
        save_data(data, db)
        
        return jsonify({'success': True, 'epic': epic})
        
    except Exception as e:
        print(f"Error adding epic: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/add_story', methods=['POST'])
@login_required
def add_story():
    try:
        data = load_data(db)
        epic_id = request.json.get('epic_id')
        name = request.json.get('name')
        description = request.json.get('description', '')
        
        if not name or not epic_id:
            return jsonify({'success': False, 'error': 'Name and epic ID are required'})
        
        # Find the epic to get project_id
        epic = next((e for e in data.get('epics', []) if e['id'] == epic_id), None)
        if not epic:
            return jsonify({'success': False, 'error': 'Epic not found'})
        
        # Get next story ID
        story_id = max([s.get('id', 0) for s in data.get('stories', [])], default=0) + 1
        
        story = {
            'id': story_id,
            'name': name,
            'description': description,
            'epic_id': epic_id,
            'project_id': epic['project_id'],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': current_user.username
        }
        
        if 'stories' not in data:
            data['stories'] = []
        
        data['stories'].append(story)
        save_data(data, db)
        
        return jsonify({'success': True, 'story': story})
        
    except Exception as e:
        print(f"Error adding story: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/add_card', methods=['POST'])
@login_required
def add_card():
    try:
        data = load_data(db)
        
        title = request.json.get('title')
        description = request.json.get('description', '')
        project_id = request.json.get('project_id')
        epic_id = request.json.get('epic_id')
        story_id = request.json.get('story_id')
        priority = request.json.get('priority', 'Medium')
        labels = request.json.get('labels', [])
        
        if not title:
            return jsonify({'success': False, 'error': 'Title is required'})
        
        # Get next card ID
        card_id = max([c.get('id', 0) for c in data.get('cards', [])], default=0) + 1
        
        card = {
            'id': card_id,
            'title': title,
            'description': description,
            'project_id': project_id,
            'epic_id': epic_id,
            'story_id': story_id,
            'status': 'todo',
            'priority': priority,
            'labels': labels,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': current_user.username,
            'assignee': '',
            'due_date': ''
        }
        
        if 'cards' not in data:
            data['cards'] = []
        
        data['cards'].append(card)
        save_data(data, db)
        
        return jsonify({'success': True, 'card': card})
        
    except Exception as e:
        print(f"Error adding card: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/update_card_status', methods=['POST'])
@login_required
def update_card_status():
    try:
        data = load_data(db)
        card_id = request.json.get('card_id')
        new_status = request.json.get('status')
        
        card = next((c for c in data['cards'] if c['id'] == card_id), None)
        if card:
            card['status'] = new_status
            card['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_data(data, db)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Card not found'})
            
    except Exception as e:
        print(f"Error updating card status: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/get_epics/<int:project_id>')
@login_required
def get_epics(project_id):
    try:
        data = load_data(db)
        epics = [e for e in data.get('epics', []) if e['project_id'] == project_id]
        return jsonify({'success': True, 'epics': epics})
        
    except Exception as e:
        print(f"Error getting epics: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/get_stories/<int:epic_id>')
@login_required
def get_stories(epic_id):
    try:
        data = load_data(db)
        stories = [s for s in data.get('stories', []) if s['epic_id'] == epic_id]
        return jsonify({'success': True, 'stories': stories})
        
    except Exception as e:
        print(f"Error getting stories: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/search')
@login_required
def search():
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'success': True, 'results': []})
        
        data = load_data(db)
        results = []
        
        # Search cards
        for card in data.get('cards', []):
            if (query in card.get('title', '').lower() or 
                query in card.get('description', '').lower()):
                results.append({
                    'type': 'card',
                    'id': card['id'],
                    'title': card['title'],
                    'description': card.get('description', '')[:100]
                })
        
        # Search epics
        for epic in data.get('epics', []):
            if (query in epic.get('name', '').lower() or 
                query in epic.get('description', '').lower()):
                results.append({
                    'type': 'epic',
                    'id': epic['id'],
                    'title': epic['name'],
                    'description': epic.get('description', '')[:100]
                })
        
        # Search stories
        for story in data.get('stories', []):
            if (query in story.get('name', '').lower() or 
                query in story.get('description', '').lower()):
                results.append({
                    'type': 'story',
                    'id': story['id'],
                    'title': story['name'],
                    'description': story.get('description', '')[:100]
                })
        
        return jsonify({'success': True, 'results': results})
        
    except Exception as e:
        print(f"Error in search: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/notifications')
@login_required
def get_notifications():
    try:
        data = load_data(db)
        user_notifications = [n for n in data.get('notifications', []) 
                            if n.get('user_id') == current_user.id]
        return jsonify({'success': True, 'notifications': user_notifications})
        
    except Exception as e:
        print(f"Error getting notifications: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/team_members')
@login_required
def get_team_members():
    try:
        data = load_data(db)
        members = [{'id': u['id'], 'username': u['username'], 'display_name': u.get('display_name', u['username'])} 
                  for u in data.get('users', []) if u.get('status') == 'active']
        return jsonify({'success': True, 'members': members})
        
    except Exception as e:
        print(f"Error getting team members: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/add_project', methods=['POST'])
@login_required
def add_project():
    try:
        data = load_data(db)
        name = request.json.get('name')
        description = request.json.get('description', '')
        
        if not name:
            return jsonify({'success': False, 'error': 'Project name is required'})
        
        # Get next project ID
        project_id = max([p.get('id', 0) for p in data.get('projects', [])], default=0) + 1
        
        project = {
            'id': project_id,
            'name': name,
            'description': description,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': current_user.username,
            'archived': False
        }
        
        if 'projects' not in data:
            data['projects'] = []
        
        data['projects'].append(project)
        save_data(data, db)
        
        return jsonify({'success': True, 'project': project})
        
    except Exception as e:
        print(f"Error adding project: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/projects/<int:project_id>/hierarchy', methods=['GET'])
@login_required
def get_project_hierarchy(project_id):
    try:
        data = load_data(db)
        
        # Get project
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'})
        
        # Get epics for this project
        epics = [e for e in data.get('epics', []) if e['project_id'] == project_id]
        
        # Build hierarchy
        hierarchy = {
            'project': project,
            'epics': []
        }
        
        for epic in epics:
            epic_data = {
                'epic': epic,
                'stories': []
            }
            
            # Get stories for this epic
            stories = [s for s in data.get('stories', []) if s['epic_id'] == epic['id']]
            
            for story in stories:
                story_data = {
                    'story': story,
                    'cards': [c for c in data.get('cards', []) if c['story_id'] == story['id']]
                }
                epic_data['stories'].append(story_data)
            
            hierarchy['epics'].append(epic_data)
        
        return jsonify({'success': True, 'hierarchy': hierarchy})
        
    except Exception as e:
        print(f"Error getting project hierarchy: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/archive_project', methods=['POST'])
@login_required
def archive_project():
    try:
        data = load_data(db)
        project_id = request.json.get('project_id')
        
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
        if project:
            project['archived'] = True
            project['archived_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            project['archived_by'] = current_user.username
            save_data(data, db)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Project not found'})
            
    except Exception as e:
        print(f"Error archiving project: {e}")
        return jsonify({'success': False, 'error': str(e)})


@api_bp.route('/restore_project', methods=['POST'])
@login_required
def restore_project():
    try:
        data = load_data(db)
        project_id = request.json.get('project_id')
        
        project = next((p for p in data['projects'] if p['id'] == project_id), None)
        if project:
            project['archived'] = False
            project['restored_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            project['restored_by'] = current_user.username
            save_data(data, db)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Project not found'})
            
    except Exception as e:
        print(f"Error restoring project: {e}")
        return jsonify({'success': False, 'error': str(e)})