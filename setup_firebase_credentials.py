#!/usr/bin/env python3
"""
Interactive script to help set up Firebase credentials
"""

import json
import os

def setup_firebase_credentials():
    print("Firebase Credentials Setup")
    print("=" * 40)
    print()
    print("This script will help you set up Firebase credentials.")
    print("You need to download the service account key from Firebase Console.")
    print()
    print("Steps:")
    print("1. Go to https://console.firebase.google.com/")
    print("2. Select your project 'pm-tool-internal'")
    print("3. Go to Project Settings > Service Accounts")
    print("4. Click 'Generate new private key'")
    print("5. Download the JSON file")
    print()
    
    choice = input("Do you have the service account JSON file? (y/n): ").lower().strip()
    
    if choice != 'y':
        print()
        print("Please download the service account key first and run this script again.")
        return False
    
    print()
    json_file_path = input("Enter the path to your downloaded JSON file: ").strip()
    
    if not os.path.exists(json_file_path):
        print(f"❌ File not found: {json_file_path}")
        return False
    
    try:
        # Read the downloaded file
        with open(json_file_path, 'r') as f:
            credentials = json.load(f)
        
        # Validate required fields
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        for field in required_fields:
            if field not in credentials:
                print(f"❌ Invalid service account file: missing '{field}' field")
                return False
        
        # Write to the expected location
        with open('firebase-service-account.json', 'w') as f:
            json.dump(credentials, f, indent=2)
        
        print("✅ Firebase credentials set up successfully!")
        print()
        print("Next steps:")
        print("1. Run: python3.9 test_firebase_connection.py")
        print("2. If connection works, run: python3.9 migrate_to_firebase.py")
        print("3. Start using Firebase as your primary database!")
        
        return True
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON file")
        return False
    except Exception as e:
        print(f"❌ Error setting up credentials: {e}")
        return False

def check_current_setup():
    """Check if Firebase is already set up"""
    if not os.path.exists('firebase-service-account.json'):
        return False
    
    try:
        with open('firebase-service-account.json', 'r') as f:
            credentials = json.load(f)
        
        # Check if it's the placeholder file
        private_key = credentials.get('private_key', '')
        if 'placeholder' in private_key or credentials.get('private_key_id') == 'placeholder':
            return False
        
        return True
    except:
        return False

if __name__ == "__main__":
    if check_current_setup():
        print("✅ Firebase credentials are already set up!")
        print("Run 'python3.9 test_firebase_connection.py' to test the connection.")
    else:
        setup_firebase_credentials()