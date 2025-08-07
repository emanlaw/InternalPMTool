"""Issue/Card management routes."""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from app.services.data_service import load_data, save_data
from app.services.firebase_service import get_firestore_client
from app.utils.helpers import extract_mentions
from app.services.notification_service import create_mention_notifications

# Get database instance
db = get_firestore_client()

issues_bp = Blueprint('issues', __name__, url_prefix='/api')


@issues_bp.route('/update_card', methods=['POST'])
@login_required
def update_card():
    try:
        data = load_data(db)
        card_id = request.json.get('card_id')
        
        card = next((c for c in data['cards'] if c['id'] == card_id), None)
        if not card:
            return jsonify({'success': False, 'error': 'Card not found'})
        
        # Update card fields
        if 'title' in request.json:
            card['title'] = request.json['title']
        if 'description' in request.json:
            card['description'] = request.json['description']
        if 'priority' in request.json:
            card['priority'] = request.json['priority']
        if 'assignee' in request.json:
            card['assignee'] = request.json['assignee']
        if 'labels' in request.json:
            card['labels'] = request.json['labels']
        
        card['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_data(data, db)
        
        return jsonify({'success': True, 'card': card})
        
    except Exception as e:
        print(f"Error updating card: {e}")
        return jsonify({'success': False, 'error': str(e)})


@issues_bp.route('/card/<int:card_id>')
@login_required
def get_card_details(card_id):
    try:
        data = load_data(db)
        card = next((c for c in data['cards'] if c['id'] == card_id), None)
        
        if card:
            return jsonify({'success': True, 'card': card})
        else:
            return jsonify({'success': False, 'error': 'Card not found'})
            
    except Exception as e:
        print(f"Error getting card details: {e}")
        return jsonify({'success': False, 'error': str(e)})


@issues_bp.route('/card/<int:card_id>/comments', methods=['GET', 'POST'])
@login_required
def card_comments(card_id):
    try:
        data = load_data(db)
        
        if request.method == 'GET':
            comments = [c for c in data.get('comments', []) if c['card_id'] == card_id]
            return jsonify({'success': True, 'comments': comments})
        
        elif request.method == 'POST':
            content = request.json.get('content')
            if not content:
                return jsonify({'success': False, 'error': 'Comment content is required'})
            
            # Get next comment ID
            comment_id = max([c.get('id', 0) for c in data.get('comments', [])], default=0) + 1
            
            comment = {
                'id': comment_id,
                'card_id': card_id,
                'content': content,
                'author': current_user.username,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if 'comments' not in data:
                data['comments'] = []
            
            data['comments'].append(comment)
            
            # Handle mentions
            mentions = extract_mentions(content)
            if mentions:
                create_mention_notifications(
                    mentions, card_id, current_user.username,
                    lambda: load_data(db), lambda d: save_data(d, db)
                )
            
            save_data(data, db)
            
            return jsonify({'success': True, 'comment': comment})
            
    except Exception as e:
        print(f"Error with card comments: {e}")
        return jsonify({'success': False, 'error': str(e)})


@issues_bp.route('/update_card_due_date', methods=['POST'])
@login_required
def update_card_due_date():
    try:
        data = load_data(db)
        card_id = request.json.get('card_id')
        due_date = request.json.get('due_date')
        
        card = next((c for c in data['cards'] if c['id'] == card_id), None)
        if card:
            card['due_date'] = due_date
            card['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_data(data, db)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Card not found'})
            
    except Exception as e:
        print(f"Error updating card due date: {e}")
        return jsonify({'success': False, 'error': str(e)})


@issues_bp.route('/move_to_backlog', methods=['POST'])
@login_required
def move_to_backlog():
    try:
        data = load_data(db)
        card_id = request.json.get('card_id')
        
        card = next((c for c in data['cards'] if c['id'] == card_id), None)
        if card:
            card['status'] = 'todo'
            card['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_data(data, db)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Card not found'})
            
    except Exception as e:
        print(f"Error moving card to backlog: {e}")
        return jsonify({'success': False, 'error': str(e)})


@issues_bp.route('/delete_card', methods=['POST'])
@login_required
def delete_card():
    try:
        data = load_data(db)
        card_id = request.json.get('card_id')
        
        # Find and remove the card
        card_index = next((i for i, c in enumerate(data['cards']) if c['id'] == card_id), None)
        if card_index is not None:
            data['cards'].pop(card_index)
            
            # Also remove associated comments
            data['comments'] = [c for c in data.get('comments', []) if c['card_id'] != card_id]
            
            save_data(data, db)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Card not found'})
            
    except Exception as e:
        print(f"Error deleting card: {e}")
        return jsonify({'success': False, 'error': str(e)})


@issues_bp.route('/send_to_assignee', methods=['POST'])
@login_required
def send_to_assignee():
    # Placeholder for sending notification to assignee
    try:
        card_id = request.json.get('card_id')
        message = request.json.get('message', '')
        
        # TODO: Implement actual notification sending
        # For now, just return success
        return jsonify({'success': True, 'message': 'Notification sent to assignee'})
        
    except Exception as e:
        print(f"Error sending to assignee: {e}")
        return jsonify({'success': False, 'error': str(e)})


@issues_bp.route('/notifications/mark_read', methods=['POST'])
@login_required
def mark_notification_read():
    try:
        data = load_data(db)
        notification_id = request.json.get('notification_id')
        
        notification = next((n for n in data.get('notifications', []) 
                           if n['id'] == notification_id and n['user_id'] == current_user.id), None)
        
        if notification:
            notification['read'] = True
            save_data(data, db)
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Notification not found'})
            
    except Exception as e:
        print(f"Error marking notification as read: {e}")
        return jsonify({'success': False, 'error': str(e)})


@issues_bp.route('/activity_feed')
@login_required
def activity_feed():
    try:
        data = load_data(db)
        
        # Generate activity feed from recent changes
        activities = []
        
        # Recent cards
        recent_cards = sorted(data.get('cards', []), 
                            key=lambda x: x.get('updated_at', x.get('created_at', '')), 
                            reverse=True)[:10]
        
        for card in recent_cards:
            activities.append({
                'type': 'card_update',
                'card_id': card['id'],
                'title': card['title'],
                'user': card.get('updated_by', card.get('created_by', 'Unknown')),
                'timestamp': card.get('updated_at', card.get('created_at', '')),
                'action': 'updated' if card.get('updated_at') else 'created'
            })
        
        # Recent comments
        recent_comments = sorted(data.get('comments', []), 
                               key=lambda x: x.get('created_at', ''), 
                               reverse=True)[:5]
        
        for comment in recent_comments:
            card = next((c for c in data['cards'] if c['id'] == comment['card_id']), None)
            if card:
                activities.append({
                    'type': 'comment',
                    'card_id': comment['card_id'],
                    'card_title': card['title'],
                    'user': comment['author'],
                    'timestamp': comment['created_at'],
                    'action': 'commented'
                })
        
        # Sort all activities by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({'success': True, 'activities': activities[:15]})
        
    except Exception as e:
        print(f"Error getting activity feed: {e}")
        return jsonify({'success': False, 'error': str(e)})