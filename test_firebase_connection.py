#!/usr/bin/env python3
"""
Test Firebase connection and setup
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_firebase_connection():
    print("Testing Firebase connection...")
    
    try:
        from config.firebase_config import firebase_config
        
        if firebase_config.db is None:
            print("❌ Firebase database is not initialized")
            print("Please check your firebase-service-account.json file")
            return False
        
        print("✅ Firebase database initialized successfully")
        
        # Test basic operations
        print("\nTesting basic Firestore operations...")
        
        # Test write
        test_doc_ref = firebase_config.db.collection('test').document('connection_test')
        test_doc_ref.set({
            'message': 'Firebase connection test',
            'timestamp': '2024-01-15'
        })
        print("✅ Write operation successful")
        
        # Test read
        doc = test_doc_ref.get()
        if doc.exists:
            print("✅ Read operation successful")
            print(f"   Data: {doc.to_dict()}")
        else:
            print("❌ Read operation failed")
            return False
        
        # Clean up test document
        test_doc_ref.delete()
        print("✅ Delete operation successful")
        
        print("\n🎉 Firebase is properly configured and working!")
        return True
        
    except Exception as e:
        print(f"❌ Firebase connection failed: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure firebase-service-account.json has valid credentials")
        print("2. Check that Firestore is enabled in your Firebase project")
        print("3. Verify your internet connection")
        return False

def test_firebase_service():
    print("\nTesting Firebase service...")
    
    try:
        from app.services.firebase_service import firebase_service
        
        # Test creating a project
        test_project = {
            'name': 'Test Project',
            'description': 'This is a test project'
        }
        
        created_project = firebase_service.create_project(test_project)
        print(f"✅ Project created: {created_project}")
        
        # Test creating a card
        test_card = {
            'project_id': created_project['id'],
            'title': 'Test Card',
            'description': 'This is a test card',
            'status': 'todo',
            'assignee': 'TestUser',
            'priority': 'Medium'
        }
        
        created_card = firebase_service.create_card(test_card)
        print(f"✅ Card created: {created_card}")
        
        # Test reading data
        all_projects = firebase_service.get_all_projects()
        all_cards = firebase_service.get_all_cards()
        
        print(f"✅ Found {len(all_projects)} projects and {len(all_cards)} cards")
        
        return True
        
    except Exception as e:
        print(f"❌ Firebase service test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Firebase Connection Test")
    print("=" * 50)
    
    connection_ok = test_firebase_connection()
    
    if connection_ok:
        service_ok = test_firebase_service()
        success = connection_ok and service_ok
    else:
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All Firebase tests passed!")
        print("You can now use Firebase as your primary database.")
    else:
        print("❌ Firebase tests failed.")
        print("Please follow the setup instructions in FIREBASE_SETUP_INSTRUCTIONS.md")
    print("=" * 50)
    
    sys.exit(0 if success else 1)