#!/usr/bin/env python3
"""
Script to create test user accounts for colleagues
"""

import json
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_test_users():
    """Create test user accounts"""
    
    # Load existing data
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No data.json file found.")
        return
    
    # Get next user ID
    existing_users = data.get('users', [])
    next_id = max([u['id'] for u in existing_users], default=0) + 1
    
    # Test users to create
    test_users = [
        {
            'username': 'testuser1',
            'password': 'test123',
            'email': 'testuser1@example.com',
            'display_name': 'Test User 1',
            'role': 'user'
        },
        {
            'username': 'testuser2', 
            'password': 'test123',
            'email': 'testuser2@example.com',
            'display_name': 'Test User 2',
            'role': 'user'
        }
    ]
    
    print("Creating test user accounts...")
    
    for user_data in test_users:
        # Check if user already exists
        if any(u['username'] == user_data['username'] for u in existing_users):
            print(f"User '{user_data['username']}' already exists, skipping...")
            continue
        
        # Create new user
        new_user = {
            'id': next_id,
            'username': user_data['username'],
            'password_hash': generate_password_hash(user_data['password']),
            'email': user_data['email'],
            'display_name': user_data['display_name'],
            'role': user_data['role'],
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        data['users'].append(new_user)
        print(f"✅ Created user: {user_data['username']} (password: {user_data['password']})")
        next_id += 1
    
    # Save updated data
    try:
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("\n🎉 Test users created successfully!")
        
        print("\n📋 Test Account Details:")
        print("=" * 40)
        for user_data in test_users:
            print(f"Username: {user_data['username']}")
            print(f"Password: {user_data['password']}")
            print(f"Email: {user_data['email']}")
            print(f"Role: {user_data['role']}")
            print("-" * 20)
        
        print("\n🔗 Login URL: http://127.0.0.1:5000/login")
        print("Share these credentials with your colleagues for testing!")
        
    except Exception as e:
        print(f"Error saving data: {e}")

if __name__ == "__main__":
    create_test_users()