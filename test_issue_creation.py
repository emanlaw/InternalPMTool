#!/usr/bin/env python3
"""
Test script to verify issue creation functionality
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.user import load_data, save_data

def test_issue_creation():
    print("Testing issue creation...")
    
    # Load current data
    data = load_data()
    print(f"Current cards: {len(data['cards'])}")
    print(f"Current projects: {len(data['projects'])}")
    
    # Create a test card
    new_card = {
        'id': max([c['id'] for c in data['cards']], default=0) + 1,
        'project_id': 1,  # Use existing project
        'title': 'Test Issue from Script',
        'description': 'This is a test issue created by the test script',
        'status': 'todo',
        'assignee': 'TestUser',
        'priority': 'Medium',
        'created_at': '2024-01-15',
        'due_date': '2024-01-20'
    }
    
    # Add the card
    data['cards'].append(new_card)
    
    # Save the data
    save_data(data)
    
    # Verify the card was added
    updated_data = load_data()
    print(f"Updated cards: {len(updated_data['cards'])}")
    
    # Find our test card
    test_card = next((c for c in updated_data['cards'] if c['title'] == 'Test Issue from Script'), None)
    
    if test_card:
        print("✅ Test card created successfully!")
        print(f"   ID: {test_card['id']}")
        print(f"   Title: {test_card['title']}")
        print(f"   Status: {test_card['status']}")
        return True
    else:
        print("❌ Test card was not found!")
        return False

if __name__ == "__main__":
    success = test_issue_creation()
    sys.exit(0 if success else 1)