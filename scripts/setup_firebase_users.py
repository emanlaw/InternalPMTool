#!/usr/bin/env python3
"""
Firebase User Setup Script
Creates initial users in Firebase Firestore
"""

import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash
from datetime import datetime

def setup_firebase():
    """Initialize Firebase connection"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate('pm-tool-internal-firebase-adminsdk-fbsvc-828aade312.json')
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("Firebase initialized successfully!")
        return db
    except Exception as e:
        print(f"Firebase initialization failed: {e}")
        return None

def create_users(db):
    """Create initial users in Firebase"""
    users = [
        {
            'id': '1',
            'username': 'admin',
            'password_hash': generate_password_hash('admin123'),
            'email': 'admin@pmtool.com',
            'display_name': 'Administrator',
            'role': 'admin',
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'id': '2', 
            'username': 'manager',
            'password_hash': generate_password_hash('manager123'),
            'email': 'manager@pmtool.com',
            'display_name': 'Project Manager',
            'role': 'admin',
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            'id': '3',
            'username': 'developer',
            'password_hash': generate_password_hash('dev123'),
            'email': 'developer@pmtool.com', 
            'display_name': 'Developer',
            'role': 'user',
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    
    print("Creating users in Firebase...")
    
    for user in users:
        user_id = user.pop('id')
        try:
            # Set user document in Firebase
            db.collection('users').document(user_id).set(user)
            print(f"Created user: {user['username']} (ID: {user_id})")
        except Exception as e:
            print(f"Failed to create user {user['username']}: {e}")

def create_sample_project(db):
    """Create a sample project"""
    project = {
        'name': 'PM Tool Development',
        'description': 'Internal project management tool development',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'active'
    }
    
    try:
        db.collection('projects').document('1').set(project)
        print("Created sample project")
    except Exception as e:
        print(f"Failed to create sample project: {e}")

def main():
    """Main setup function"""
    print("Setting up Firebase users...")
    
    # Initialize Firebase
    db = setup_firebase()
    if not db:
        print("Cannot proceed without Firebase connection")
        return
    
    # Create users
    create_users(db)
    
    # Create sample project
    create_sample_project(db)
    
    print("\nSetup complete!")
    print("\nLogin credentials:")
    print("1. Admin: username='admin', password='admin123'")
    print("2. Manager: username='manager', password='manager123'") 
    print("3. Developer: username='developer', password='dev123'")

if __name__ == '__main__':
    main()