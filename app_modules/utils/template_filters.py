from app.utils.date_helpers import (
    get_due_date_class,
    get_due_date_text_class,
    get_due_date_status,
    get_comment_count
)
from datetime import datetime

def format_timestamp(timestamp):
    """Format timestamp to YYYY-MM-DD HH:MM:SS (remove milliseconds)"""
    if not timestamp:
        return '-'
    
    # If it's already in the desired format, return as is
    if isinstance(timestamp, str) and len(timestamp) <= 19:
        return timestamp
    
    # Try to parse and format
    try:
        if isinstance(timestamp, str):
            # Handle ISO format with milliseconds
            if 'T' in timestamp:
                date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        else:
            date = timestamp
        
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return str(timestamp)  # Return original if parsing fails

def register_template_filters(app):
    """Register template filters and globals"""
    app.jinja_env.globals.update(
        get_due_date_class=get_due_date_class,
        get_due_date_text_class=get_due_date_text_class,
        get_due_date_status=get_due_date_status,
        get_comment_count=get_comment_count,
        format_timestamp=format_timestamp
    )