"""Data loading and saving service for Firebase and local files."""

import json
from datetime import datetime
from werkzeug.security import generate_password_hash


def load_data(db=None):
    """Load data from Firebase or local files"""
    data = {'users': [], 'projects': [], 'epics': [], 'stories': [], 'cards': [], 'comments': [], 'notifications': [], 'sprints': []}
    
    if db is None:
        print("ERROR: Firebase not initialized! Please check your firebase-service-account.json file.")
        print("You need to download the real service account key from Firebase Console.")
        print("Falling back to local data files...")
        # Try to load from local files
        try:
            from data_manager import DataManager
            dm = DataManager()
            local_data = dm.load_data()
            if local_data and local_data.get('users'):
                print(f"Using local data: {len(local_data['users'])} users, {len(local_data.get('projects', []))} projects")
                return local_data
        except Exception as e:
            print(f"Error loading local data: {e}")
        
        # If local data fails, try data.json directly
        try:
            with open('data.json', 'r') as f:
                local_data = json.load(f)
                if local_data and local_data.get('users'):
                    print(f"Using data.json: {len(local_data['users'])} users, {len(local_data.get('projects', []))} projects")
                    return local_data
        except Exception as e:
            print(f"Error loading data.json: {e}")
        
        return data
    
    try:
        # Load from Firebase collections
        for doc in db.collection('users').stream():
            user_data = doc.to_dict()
            user_data['id'] = int(doc.id)
            data['users'].append(user_data)
        
        for doc in db.collection('projects').stream():
            project_data = doc.to_dict()
            try:
                project_data['id'] = int(doc.id)
                data['projects'].append(project_data)
            except ValueError:
                print(f"Skipping project with non-numeric ID: {doc.id}")
                continue
        
        # Load epics
        for project_doc in db.collection('projects').stream():
            try:
                project_id = int(project_doc.id)
            except ValueError:
                continue
            epics_ref = db.collection('projects').document(project_doc.id).collection('epics')
            for epic_doc in epics_ref.stream():
                epic_data = epic_doc.to_dict()
                epic_data['id'] = int(epic_doc.id)
                epic_data['project_id'] = project_id
                data['epics'].append(epic_data)
                
                # Load stories for this epic
                stories_ref = epics_ref.document(epic_doc.id).collection('stories')
                for story_doc in stories_ref.stream():
                    story_data = story_doc.to_dict()
                    story_data['id'] = int(story_doc.id)
                    story_data['epic_id'] = int(epic_doc.id)
                    story_data['project_id'] = project_id
                    data['stories'].append(story_data)
        
        # Load sprints
        for doc in db.collection('sprints').stream():
            sprint_data = doc.to_dict()
            sprint_data['id'] = int(doc.id)
            data['sprints'].append(sprint_data)
        
        # Load cards from stories/{storyId}/issues subcollection
        for project_doc in db.collection('projects').stream():
            try:
                project_id = int(project_doc.id)
            except ValueError:
                continue
            epics_ref = db.collection('projects').document(project_doc.id).collection('epics')
            for epic_doc in epics_ref.stream():
                epic_id = int(epic_doc.id)
                stories_ref = epics_ref.document(epic_doc.id).collection('stories')
                for story_doc in stories_ref.stream():
                    story_id = int(story_doc.id)
                    issues_ref = stories_ref.document(story_doc.id).collection('issues')
                    for issue_doc in issues_ref.stream():
                        card_data = issue_doc.to_dict()
                        card_data['id'] = int(issue_doc.id)
                        card_data['story_id'] = story_id
                        card_data['epic_id'] = epic_id
                        card_data['project_id'] = project_id
                        data['cards'].append(card_data)
                
                        # Load comments for this issue
                        comments_ref = issues_ref.document(issue_doc.id).collection('comments')
                        for comment_doc in comments_ref.stream():
                            comment_data = comment_doc.to_dict()
                            comment_data['id'] = int(comment_doc.id)
                            comment_data['card_id'] = int(issue_doc.id)
                            data['comments'].append(comment_data)
                    
        print(f"Loaded from Firebase: {len(data['users'])} users, {len(data['projects'])} projects, {len(data['cards'])} cards, {len(data['sprints'])} sprints")
        
    except Exception as e:
        print(f"Firebase error: {e}")
    
    # Create default admin user if no users exist
    # If Firebase fails or has no data, use local files
    print(f"Debug - Checking users count: {len(data['users'])}")
    if not data['users']:
        print("Debug - No users found, trying local fallback")
        try:
            from data_manager import DataManager
            dm = DataManager()
            local_data = dm.load_data()
            print(f"Debug - Local data manager loaded: {len(local_data.get('users', []))} users")
            if local_data['users']:
                data = local_data
                print(f"Using local data files: {len(data['users'])} users, {len(data['projects'])} projects, {len(data.get('epics', []))} epics, {len(data.get('stories', []))} stories, {len(data.get('sprints', []))} sprints")
        except Exception as e:
            print(f"Error loading local data: {e}")
            print("Debug - Exception in local data loading, trying data.json fallback")
            # Try the main data.json file as final fallback
            try:
                with open('data.json', 'r') as f:
                    json_data = json.load(f)
                    data = json_data
                    print(f"Using data.json fallback: {len(data.get('users', []))} users, {len(data.get('projects', []))} projects")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading data.json fallback: {e}")
    else:
        print(f"Debug - Using Firebase data with {len(data['users'])} users")
    
    if not data['users']:
        default_admin = {
            'username': 'admin',
            'password_hash': generate_password_hash('admin123'),
            'email': 'admin@example.com',
            'display_name': 'Administrator',
            'role': 'admin',
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if db:
            try:
                db.collection('users').document('1').set(default_admin)
                print("Default admin user created in Firebase")
            except Exception as e:
                print(f"Error creating admin user in Firebase: {e}")
        
        data['users'].append({'id': 1, **default_admin})
        print("Default admin user created: admin/admin123")
    
    # Create default project if no projects exist
    if not data['projects']:
        default_project = {
            'name': 'Sample Project',
            'description': 'Your first project',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if db:
            try:
                db.collection('projects').document('1').set(default_project)
                print("Default project created in Firebase")
            except Exception as e:
                print(f"Error creating project in Firebase: {e}")
        
        data['projects'].append({'id': 1, **default_project})
        print("Default project created")
    
    return data


def save_data(data, db=None):
    """Save data to Firebase and local files"""
    # Always save to local files as backup
    try:
        from data_manager import DataManager
        dm = DataManager()
        dm.save_data(data)
    except Exception as e:
        print(f"Error saving to local files: {e}")
    
    if db is None:
        print("WARNING: Firebase not initialized! Data saved locally only.")
        return
    
    try:
        # Save to Firebase collections
        for user in data.get('users', []):
            user_copy = user.copy()
            user_copy.pop('id', None)
            db.collection('users').document(str(user['id'])).set(user_copy)
        
        for project in data.get('projects', []):
            project_copy = project.copy()
            project_copy.pop('id', None)
            db.collection('projects').document(str(project['id'])).set(project_copy)
        
        # Save epics to projects/{projectId}/epics subcollection
        for epic in data.get('epics', []):
            epic_copy = epic.copy()
            epic_copy.pop('id', None)
            epic_copy.pop('project_id', None)
            project_ref = db.collection('projects').document(str(epic['project_id']))
            project_ref.collection('epics').document(str(epic['id'])).set(epic_copy)
        
        # Save stories to projects/{projectId}/epics/{epicId}/stories subcollection
        for story in data.get('stories', []):
            story_copy = story.copy()
            story_copy.pop('id', None)
            story_copy.pop('epic_id', None)
            story_copy.pop('project_id', None)
            project_ref = db.collection('projects').document(str(story['project_id']))
            epic_ref = project_ref.collection('epics').document(str(story['epic_id']))
            epic_ref.collection('stories').document(str(story['id'])).set(story_copy)
        
        # Save cards to projects/{projectId}/epics/{epicId}/stories/{storyId}/issues subcollection
        for card in data.get('cards', []):
            card_copy = card.copy()
            card_copy.pop('id', None)
            card_copy.pop('story_id', None)
            card_copy.pop('epic_id', None)
            card_copy.pop('project_id', None)
            project_ref = db.collection('projects').document(str(card['project_id']))
            epic_ref = project_ref.collection('epics').document(str(card['epic_id']))
            story_ref = epic_ref.collection('stories').document(str(card['story_id']))
            story_ref.collection('issues').document(str(card['id'])).set(card_copy)
        
        # Save sprints to Firebase
        for sprint in data.get('sprints', []):
            sprint_copy = sprint.copy()
            sprint_copy.pop('id', None)
            db.collection('sprints').document(str(sprint['id'])).set(sprint_copy)
        
        # Save comments to projects/{projectId}/epics/{epicId}/stories/{storyId}/issues/{issueId}/comments
        for comment in data.get('comments', []):
            comment_copy = comment.copy()
            comment_copy.pop('id', None)
            card_id = comment_copy.pop('card_id')
            card = next((c for c in data.get('cards', []) if c['id'] == card_id), None)
            if card:
                project_ref = db.collection('projects').document(str(card['project_id']))
                epic_ref = project_ref.collection('epics').document(str(card['epic_id']))
                story_ref = epic_ref.collection('stories').document(str(card['story_id']))
                issue_ref = story_ref.collection('issues').document(str(card_id))
                issue_ref.collection('comments').document(str(comment['id'])).set(comment_copy)
                
        print("Data saved to Firebase successfully")
    except Exception as e:
        print(f"Error saving to Firebase: {e}")