from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'projects': [{
            'id': 1,
            'name': 'Sample Project',
            'description': 'Your first project'
        }],
        'cards': [
            {'id': 1, 'project_id': 1, 'title': 'Setup project', 'description': 'Initial setup', 'status': 'done', 'assignee': 'John', 'priority': 'High', 'created_at': '2024-01-01'},
            {'id': 2, 'project_id': 1, 'title': 'Design UI', 'description': 'Create mockups', 'status': 'in_progress', 'assignee': 'Jane', 'priority': 'Medium', 'created_at': '2024-01-02'},
            {'id': 3, 'project_id': 1, 'title': 'Implement backend', 'description': 'API development', 'status': 'todo', 'assignee': 'Bob', 'priority': 'High', 'created_at': '2024-01-03'}
        ]
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
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

@app.route('/issues')
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

@app.route('/board/<int:project_id>')
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

@app.route('/api/move_card', methods=['POST'])
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

@app.route('/api/add_card', methods=['POST'])
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
        'created_at': datetime.now().strftime('%Y-%m-%d')
    }
    data['cards'].append(new_card)
    save_data(data)
    return jsonify(new_card)

@app.route('/api/add_project', methods=['POST'])
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

@app.route('/api/update_card_status', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)