#!/usr/bin/env python3
"""
Migrate sprints data from local files to Firebase
"""

import json
import os
import firebase_admin
from firebase_admin import credentials, firestore

def migrate_sprints_to_firebase():
    """Migrate sprints from local JSON to Firebase"""
    
    # Initialize Firebase if not already done
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate('firebase-service-account.json')
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized successfully!")
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        return False
    
    # Load sprints from local file
    sprints_file = 'data/sprints.json'
    try:
        with open(sprints_file, 'r') as f:
            sprints = json.load(f)
        print(f"📁 Loaded {len(sprints)} sprints from local file")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error loading sprints file: {e}")
        return False
    
    if not sprints:
        print("ℹ️ No sprints to migrate")
        return True
    
    # Migrate each sprint to Firebase
    success_count = 0
    for sprint in sprints:
        try:
            sprint_copy = sprint.copy()
            sprint_id = sprint_copy.pop('id')
            
            # Save to Firebase
            db.collection('sprints').document(str(sprint_id)).set(sprint_copy)
            print(f"✅ Migrated sprint {sprint_id}: {sprint['name']}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error migrating sprint {sprint.get('id', 'unknown')}: {e}")
    
    print(f"\n🎉 Migration completed: {success_count}/{len(sprints)} sprints migrated successfully")
    return success_count == len(sprints)

def verify_firebase_sprints():
    """Verify sprints are in Firebase"""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate('firebase-service-account.json')
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        
        sprints = []
        for doc in db.collection('sprints').stream():
            sprint_data = doc.to_dict()
            sprint_data['id'] = int(doc.id)
            sprints.append(sprint_data)
        
        print(f"\n📊 Firebase verification:")
        print(f"Total sprints in Firebase: {len(sprints)}")
        
        for sprint in sprints:
            print(f"  - Sprint {sprint['id']}: {sprint['name']} ({sprint['status']})")
        
        return len(sprints) > 0
        
    except Exception as e:
        print(f"❌ Error verifying Firebase sprints: {e}")
        return False

if __name__ == "__main__":
    print("Migrating Sprints to Firebase")
    print("=" * 40)
    
    # Migrate sprints
    success = migrate_sprints_to_firebase()
    
    if success:
        # Verify migration
        verify_firebase_sprints()
        print("\n✅ Sprint migration to Firebase completed successfully!")
        print("Now the Sprint Management page should show sprints from Firebase.")
    else:
        print("\n❌ Sprint migration failed.")