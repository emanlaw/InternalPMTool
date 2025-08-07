"""Template helpers and utility functions."""

import re
from datetime import datetime, date


def get_due_date_text_class(due_date_str):
    """Get CSS class for due date text based on status."""
    if not due_date_str:
        return ''
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        today = date.today()
        if due_date < today:
            return 'due-date-overdue'
        elif due_date == today:
            return 'due-date-today'
        return 'due-date-upcoming'
    except:
        return ''


def get_due_date_status(due_date_str):
    """Get human-readable due date status."""
    if not due_date_str:
        return ''
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        today = date.today()
        if due_date < today:
            return '(OVERDUE)'
        elif due_date == today:
            return '(TODAY)'
        elif (due_date - today).days <= 3:
            return '(SOON)'
        return ''
    except:
        return ''


def get_comment_count(card_id, data_loader=None):
    """Get count of comments for a card."""
    if data_loader:
        data = data_loader()
    else:
        # Import here to avoid circular imports
        from app.services.data_service import load_data
        data = load_data()
    return len([c for c in data.get('comments', []) if c['card_id'] == card_id])


def format_timestamp(timestamp):
    """Format timestamp for display."""
    if not timestamp:
        return '-'
    if isinstance(timestamp, str) and len(timestamp) == 10:
        return timestamp
    try:
        if isinstance(timestamp, str):
            for fmt in ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                try:
                    dt = datetime.strptime(timestamp, fmt)
                    return dt.strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    continue
        return timestamp
    except:
        return timestamp


def format_date(date_string):
    """Format date string for display."""
    if not date_string:
        return ''
    try:
        if len(date_string) == 10:  # YYYY-MM-DD format
            return date_string
        dt = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y-%m-%d')
    except:
        return date_string


def extract_mentions(content):
    """Extract @mentions from comment content."""
    mentions = re.findall(r'@(\w+)', content)
    return list(set(mentions))  # Remove duplicates


def get_label_by_id(label_id, predefined_labels):
    """Get label by ID from predefined labels."""
    return next((label for label in predefined_labels if label['id'] == label_id), None)