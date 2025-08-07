"""Notification service for user mentions and notifications."""

from datetime import datetime


def create_mention_notifications(mentions, card_id, author, data_loader, data_saver):
    """Create notifications for mentioned users."""
    data = data_loader()
    
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
    
    data_saver(data)