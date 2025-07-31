from config.firebase_config import firebase_config
from datetime import datetime
import json

class FirebaseService:
    def __init__(self):
        self.db = firebase_config.db
    
    # User operations
    def create_user(self, user_data):
        """Create a new user in Firestore"""
        user_ref = self.db.collection('users').document()
        user_data['id'] = user_ref.id
        user_data['created_at'] = datetime.now()
        user_ref.set(user_data)
        return user_data
    
    def get_user(self, user_id):
        """Get user by ID"""
        user_ref = self.db.collection('users').document(user_id)
        user = user_ref.get()
        return user.to_dict() if user.exists else None
    
    def get_all_users(self):
        """Get all users"""
        if self.db is None:
            raise Exception("Firebase not configured")
        
        users = []
        users_ref = self.db.collection('users')
        for doc in users_ref.stream():
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            users.append(user_data)
        return users
    
    # Project operations
    def create_project(self, project_data):
        """Create a new project"""
        # Generate readable ID (e.g., PROJ-001, PROJ-002)
        existing_projects = self.get_all_projects()
        project_number = len(existing_projects) + 1
        readable_id = f"PROJ-{project_number:03d}"
        
        project_ref = self.db.collection('projects').document(readable_id)
        project_data['id'] = readable_id
        project_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        project_ref.set(project_data)
        return project_data
    
    def get_all_projects(self):
        """Get all projects"""
        if self.db is None:
            raise Exception("Firebase not configured")
        
        projects = []
        projects_ref = self.db.collection('projects')
        for doc in projects_ref.stream():
            project_data = doc.to_dict()
            project_data['id'] = doc.id
            projects.append(project_data)
        return projects
    
    # Card operations
    def create_card(self, card_data):
        """Create a new card"""
        # Generate readable ID (e.g., CARD-001, CARD-002)
        existing_cards = self.get_all_cards()
        card_number = len(existing_cards) + 1
        readable_id = f"CARD-{card_number:03d}"
        
        card_ref = self.db.collection('cards').document(readable_id)
        card_data['id'] = readable_id
        card_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        card_ref.set(card_data)
        return card_data
    
    def update_card(self, card_id, updates):
        """Update a card"""
        card_ref = self.db.collection('cards').document(card_id)
        updates['updated_at'] = datetime.now()
        card_ref.update(updates)
        return True
    
    def get_all_cards(self):
        """Get all cards"""
        if self.db is None:
            raise Exception("Firebase not configured")
        
        cards = []
        cards_ref = self.db.collection('cards')
        for doc in cards_ref.stream():
            card_data = doc.to_dict()
            card_data['id'] = doc.id
            cards.append(card_data)
        return cards
    
    def get_cards_by_project(self, project_id):
        """Get cards for a specific project"""
        cards = []
        cards_ref = self.db.collection('cards').where('project_id', '==', project_id)
        for doc in cards_ref.stream():
            card_data = doc.to_dict()
            card_data['id'] = doc.id
            cards.append(card_data)
        return cards
    
    # Comment operations
    def create_comment(self, comment_data):
        """Create a new comment"""
        # Generate readable ID (e.g., COM-001, COM-002)
        all_comments = []
        comments_ref = self.db.collection('comments')
        for doc in comments_ref.stream():
            all_comments.append(doc.to_dict())
        
        comment_number = len(all_comments) + 1
        readable_id = f"COM-{comment_number:03d}"
        
        comment_ref = self.db.collection('comments').document(readable_id)
        comment_data['id'] = readable_id
        comment_data['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_ref.set(comment_data)
        return comment_data
    
    def get_comments_by_card(self, card_id):
        """Get comments for a specific card"""
        comments = []
        comments_ref = self.db.collection('comments').where('card_id', '==', card_id)
        for doc in comments_ref.stream():
            comment_data = doc.to_dict()
            comment_data['id'] = doc.id
            comments.append(comment_data)
        return comments
    
    # Data migration from JSON
    def migrate_json_data(self, json_file_path):
        """Migrate existing JSON data to Firestore"""
        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)
            
            # Migrate users
            for user in data.get('users', []):
                self.db.collection('users').document(str(user['id'])).set({
                    'username': user['username'],
                    'password_hash': user['password_hash'],
                    'email': user.get('email', ''),
                    'email_notifications': user.get('email_notifications', True),
                    'created_at': datetime.now()
                })
            
            # Migrate projects
            for project in data.get('projects', []):
                self.db.collection('projects').document(str(project['id'])).set({
                    'name': project['name'],
                    'description': project['description'],
                    'created_at': datetime.now()
                })
            
            # Migrate cards
            for card in data.get('cards', []):
                self.db.collection('cards').document(str(card['id'])).set({
                    'project_id': str(card['project_id']),
                    'title': card['title'],
                    'description': card.get('description', ''),
                    'status': card['status'],
                    'assignee': card.get('assignee', ''),
                    'priority': card['priority'],
                    'due_date': card.get('due_date', ''),
                    'created_at': datetime.now()
                })
            
            # Migrate comments
            for comment in data.get('comments', []):
                self.db.collection('comments').document(str(comment['id'])).set({
                    'card_id': str(comment['card_id']),
                    'author': comment['author'],
                    'content': comment['content'],
                    'created_at': datetime.now()
                })
            
            return True
        except Exception as e:
            print(f"Migration error: {e}")
            return False

# Global Firebase service instance
firebase_service = FirebaseService()