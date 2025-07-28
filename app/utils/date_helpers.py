from datetime import datetime, date

def get_due_date_class(due_date_str):
    if not due_date_str:
        return ''
    
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        today = date.today()
        
        if due_date < today:
            return 'card-overdue'
        elif due_date == today:
            return 'card-due-today'
        elif (due_date - today).days <= 3:
            return 'card-due-soon'
        return ''
    except:
        return ''

def get_due_date_text_class(due_date_str):
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

def get_comment_count(card_id):
    from app.models.user import load_data
    data = load_data()
    return len([c for c in data.get('comments', []) if c['card_id'] == card_id])