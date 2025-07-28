from flask import Blueprint, request, jsonify, send_file, current_app
from flask_login import login_required, current_user
from flask_mail import Message
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import io
from app.models.user import load_data, save_data
from app.utils.date_helpers import get_comment_count

api_bp = Blueprint('api', __name__)

@api_bp.route('/test-email')
@login_required
def test_email():
    """Test email functionality"""
    try:
        data = load_data()
        user_data = next((u for u in data['users'] if u['id'] == current_user.id), None)
        
        if not user_data or not user_data.get('email'):
            return jsonify({'error': 'No email address set in profile'}), 400
        
        # Send test email
        msg = Message(
            subject="PM Tool - Test Email",
            recipients=[user_data['email']],
            html="""
            <h2>Test Email Successful! 🎉</h2>
            <p>Your email notifications are working correctly.</p>
            <p>You will receive daily notifications for overdue cards.</p>
            """
        )
        
        current_app.extensions['mail'].send(msg)
        return jsonify({'success': True, 'message': 'Test email sent successfully!'})
        
    except Exception as e:
        return jsonify({'error': f'Email test failed: {str(e)}'}), 500

@api_bp.route('/move_card', methods=['POST'])
def move_card():
    data = load_data()
    card_id = request.json['card_id']
    new_status = request.json['status']
    
    for card in data['cards']:
        if card['id'] == card_id:
            card['status'] = new_status
            break
    
    save_data(data)
    return jsonify({'success': True})

@api_bp.route('/add_card', methods=['POST'])
def add_card():
    data = load_data()
    new_card = {
        'id': max([c['id'] for c in data['cards']], default=0) + 1,
        'project_id': request.json['project_id'],
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'status': 'todo',
        'assignee': request.json.get('assignee', ''),
        'priority': request.json.get('priority', 'Medium'),
        'created_at': datetime.now().strftime('%Y-%m-%d'),
        'due_date': request.json.get('due_date', '')
    }
    data['cards'].append(new_card)
    save_data(data)
    return jsonify(new_card)

@api_bp.route('/add_project', methods=['POST'])
def add_project():
    data = load_data()
    new_project = {
        'id': max([p['id'] for p in data['projects']], default=0) + 1,
        'name': request.json['name'],
        'description': request.json.get('description', '')
    }
    data['projects'].append(new_project)
    save_data(data)
    return jsonify(new_project)

@api_bp.route('/update_card_status', methods=['POST'])
def update_card_status():
    data = load_data()
    card_id = request.json['card_id']
    new_status = request.json['status']
    
    for card in data['cards']:
        if card['id'] == card_id:
            card['status'] = new_status
            break
    
    save_data(data)
    return jsonify({'success': True})

@api_bp.route('/card/<int:card_id>/comments')
@login_required
def get_comments(card_id):
    data = load_data()
    comments = [c for c in data.get('comments', []) if c['card_id'] == card_id]
    return jsonify(comments)

@api_bp.route('/card/<int:card_id>/comments', methods=['POST'])
@login_required
def add_comment(card_id):
    data = load_data()
    new_comment = {
        'id': max([c['id'] for c in data.get('comments', [])], default=0) + 1,
        'card_id': card_id,
        'author': current_user.username,
        'content': request.json['content'],
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if 'comments' not in data:
        data['comments'] = []
    data['comments'].append(new_comment)
    save_data(data)
    return jsonify(new_comment)

@api_bp.route('/card/<int:card_id>')
@login_required
def get_card_details(card_id):
    data = load_data()
    card = next((c for c in data['cards'] if c['id'] == card_id), None)
    if not card:
        return jsonify({'error': 'Card not found'}), 404
    
    comments = [c for c in data.get('comments', []) if c['card_id'] == card_id]
    return jsonify({'card': card, 'comments': comments})

@api_bp.route('/search')
@login_required
def search_cards():
    data = load_data()
    cards = data['cards']
    
    # Get search parameters
    search_query = request.args.get('q', '').lower()
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    assignee_filter = request.args.get('assignee', '')
    project_filter = request.args.get('project_id', '')
    
    # Filter cards
    filtered_cards = cards
    
    # Project filter
    if project_filter:
        filtered_cards = [c for c in filtered_cards if c['project_id'] == int(project_filter)]
    
    # Status filter
    if status_filter:
        filtered_cards = [c for c in filtered_cards if c['status'] == status_filter]
    
    # Priority filter
    if priority_filter:
        filtered_cards = [c for c in filtered_cards if c['priority'] == priority_filter]
    
    # Assignee filter
    if assignee_filter:
        filtered_cards = [c for c in filtered_cards if c.get('assignee', '').lower() == assignee_filter.lower()]
    
    # Search query (title and description)
    if search_query:
        filtered_cards = [c for c in filtered_cards if 
                         search_query in c['title'].lower() or 
                         search_query in c.get('description', '').lower()]
    
    return jsonify({
        'cards': filtered_cards,
        'total': len(filtered_cards)
    })

@api_bp.route('/export-excel')
@login_required
def export_excel():
    data = load_data()
    cards = data['cards']
    projects = {p['id']: p['name'] for p in data['projects']}
    
    # Apply same filters as search
    search_query = request.args.get('q', '').lower()
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    assignee_filter = request.args.get('assignee', '')
    project_filter = request.args.get('project_id', '')
    
    # Filter cards (same logic as search)
    filtered_cards = cards
    if project_filter:
        filtered_cards = [c for c in filtered_cards if c['project_id'] == int(project_filter)]
    if status_filter:
        filtered_cards = [c for c in filtered_cards if c['status'] == status_filter]
    if priority_filter:
        filtered_cards = [c for c in filtered_cards if c['priority'] == priority_filter]
    if assignee_filter:
        filtered_cards = [c for c in filtered_cards if c.get('assignee', '').lower() == assignee_filter.lower()]
    if search_query:
        filtered_cards = [c for c in filtered_cards if 
                         search_query in c['title'].lower() or 
                         search_query in c.get('description', '').lower()]
    
    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Issues Export"
    
    # Headers
    headers = ['ID', 'Title', 'Description', 'Status', 'Priority', 'Assignee', 'Project', 'Due Date', 'Comments', 'Created Date']
    ws.append(headers)
    
    # Style headers
    header_font = Font(bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='0079BF', end_color='0079BF', fill_type='solid')
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
    
    # Add data
    for card in filtered_cards:
        comment_count = get_comment_count(card['id'])
        project_name = projects.get(card['project_id'], 'Unknown')
        
        row_data = [
            f"#{card['id']}",
            card['title'],
            card.get('description', ''),
            card['status'].replace('_', ' ').title(),
            card['priority'],
            card.get('assignee', 'Unassigned'),
            project_name,
            card.get('due_date', ''),
            comment_count,
            card['created_at']
        ]
        ws.append(row_data)
    
    # Auto-adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Save to memory
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    # Generate filename with current date
    filename = f"issues_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )