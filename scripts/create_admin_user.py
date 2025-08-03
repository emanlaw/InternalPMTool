#!/usr/bin/env python3
"""
Script to create the admin user directly in Firebase Firestore
Run this after setting up your real Firebase service account credentials
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin_user():
    try:
        # Import Firebase
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        # Initialize Firebase
        if not firebase_admin._apps:
            cred = credentials.Certificate('firebase-service-account.json')
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        
        # Create admin user
        admin_user = {
            'username': 'admin',
            'password_hash': generate_password_hash('admin123'),
            'email': 'admin@pmtool.com',
            'display_name': 'System Administrator',
            'role': 'admin',
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': None,
            'email_notifications': True
        }
        
        # Save to Firebase
        db.collection('users').document('1').set(admin_user)
        print("Admin user created successfully!")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Role: admin")
        print("   Status: active")
        
        # Create default project
        default_project = {
            'name': 'Welcome Project',
            'description': 'Your first project to get started',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'archived': False
        }
        
        db.collection('projects').document('1').set(default_project)
        print("Default project created!")
        
        return True
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        print("\nTo fix this:")
        print("1. Go to Firebase Console > Project Settings > Service Accounts")
        print("2. Click 'Generate new private key'")
        print("3. Save the downloaded file as 'firebase-service-account.json'")
        print("4. Replace the current mock file with the real one")
        return False

if __name__ == "__main__":
    print("Creating Firebase Admin User...")
    success = create_admin_user()
    
    if success:
        print("\nSetup complete! You can now login with:")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("\nSetup failed. Please check your Firebase configuration.")