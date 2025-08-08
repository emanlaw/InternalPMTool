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
        
        # Separate items by type
        epics = []
        stories = []
        issues = []
        
        for item in items:
            item_type = item.get('type')
            item_id = item.get('id')
            
            if item_type == 'epic':
                epic = next((e for e in data.get('epics', []) if e['id'] == item_id), None)
                if epic:
                    epics.append(epic)
            elif item_type == 'story':
                story = next((s for s in data.get('stories', []) if s['id'] == item_id), None)
                if story:
                    stories.append(story)
            elif item_type == 'card':
                card = next((c for c in data.get('cards', []) if c['id'] == item_id), None)
                if card:
                    issues.append(card)
        
        return jsonify({
            'success': True, 
            'sprint': sprint,
            'epics': epics,
            'stories': stories,
            'issues': issues
        })
        
    except Exception as e:
        print(f"Error getting sprint items: {e}")
        return jsonify({'success': False, 'error': str(e)})


@sprints_bp.route('/api/sprints/<int:sprint_id>/items', methods=['POST'])
@login_required
def update_sprint_items(sprint_id):
    """Update sprint items based on edit modal selections"""
    try:
        data = load_data(db)
        
        sprint = next((s for s in data.get('sprints', []) if s['id'] == sprint_id), None)
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'})
        
        epic_ids = request.json.get('epic_ids', [])
        story_ids = request.json.get('story_ids', [])
        issue_ids = request.json.get('issue_ids', [])
        
        # Clear existing items and add new ones
        sprint['items'] = []
        
        # Add epics
        for epic_id in epic_ids:
            sprint['items'].append({
                'type': 'epic',
                'id': epic_id,
                'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'added_by': current_user.username
            })
        
        # Add stories
        for story_id in story_ids:
            sprint['items'].append({
                'type': 'story',
                'id': story_id,
                'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'added_by': current_user.username
            })
        
        # Add issues (cards)
        for issue_id in issue_ids:
            sprint['items'].append({
                'type': 'card',
                'id': issue_id,
                'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'added_by': current_user.username
            })
        
        save_data(data, db)
        
        return jsonify({'success': True, 'message': 'Sprint items updated successfully'})
        
    except Exception as e:
        print(f"Error updating sprint items: {e}")
        return jsonify({'success': False, 'error': str(e)})


@sprints_bp.route('/api/sprints/<int:sprint_id>', methods=['PUT'])
@login_required
def update_sprint(sprint_id):
    """Update sprint details"""
    try:
        data = load_data(db)
        
        sprint = next((s for s in data.get('sprints', []) if s['id'] == sprint_id), None)
        if not sprint:
            return jsonify({'success': False, 'error': 'Sprint not found'})
        
        # Update sprint fields
        if 'name' in request.json:
            sprint['name'] = request.json['name']
        if 'goal' in request.json:
            sprint['goal'] = request.json['goal']
        if 'story_points' in request.json:
            sprint['story_points'] = request.json['story_points']
        if 'start_date' in request.json:
            sprint['start_date'] = request.json['start_date']
        if 'end_date' in request.json:
            sprint['end_date'] = request.json['end_date']
            
        sprint['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sprint['updated_by'] = current_user.username
        
        save_data(data, db)
        
        return jsonify({'success': True, 'message': 'Sprint updated successfully'})
        
    except Exception as e:
        print(f"Error updating sprint: {e}")
        return jsonify({'success': False, 'error': str(e)})


@sprints_bp.route('/api/projects/<int:project_id>/hierarchy', methods=['GET'])
@login_required
def get_project_hierarchy(project_id):
    """Get project hierarchy for sprint planning"""
    try:
        data = load_data(db)
        
        project = next((p for p in data.get('projects', []) if p['id'] == project_id), None)
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'})
        
        # Get all epics for this project
        epics = [e for e in data.get('epics', []) if e.get('project_id') == project_id]
        
        # Get all stories for this project
        all_stories = [s for s in data.get('stories', []) if s.get('project_id') == project_id]
        
        # Get all issues (cards) for this project
        all_issues = [c for c in data.get('cards', []) if c.get('project_id') == project_id]
        
        # Build hierarchy
        enriched_epics = []
        orphaned_stories = []
        orphaned_issues = []
        
        for epic in epics:
            epic_stories = [s for s in all_stories if s.get('epic_id') == epic['id']]
            
            # Add stories to epic and get their issues
            epic_with_stories = epic.copy()
            epic_with_stories['stories'] = []
            
            for story in epic_stories:
                story_issues = [i for i in all_issues if i.get('story_id') == story['id']]
                story_with_issues = story.copy()
                story_with_issues['issues'] = story_issues
                epic_with_stories['stories'].append(story_with_issues)
            
            enriched_epics.append(epic_with_stories)
        
        # Find orphaned stories (not in any epic)
        used_story_ids = set()
        for epic in enriched_epics:
            for story in epic.get('stories', []):
                used_story_ids.add(story['id'])
        
        orphaned_stories = [s for s in all_stories if s['id'] not in used_story_ids]
        
        # Find orphaned issues (not in any story)
        used_issue_ids = set()
        for epic in enriched_epics:
            for story in epic.get('stories', []):
                for issue in story.get('issues', []):
                    used_issue_ids.add(issue['id'])
        
        orphaned_issues = [i for i in all_issues if i['id'] not in used_issue_ids]
        
        return jsonify({
            'success': True,
            'epics': enriched_epics,
            'orphaned_stories': orphaned_stories,
            'orphaned_issues': orphaned_issues
        })
        
    except Exception as e:
        print(f"Error getting project hierarchy: {e}")
        return jsonify({'success': False, 'error': str(e)})


# Additional sprint API routes can be added here as needed