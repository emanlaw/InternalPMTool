#!/usr/bin/env python3
"""
Test status update functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_status_update():
    print("Testing status update functionality...")
    
    try:
        from app.services.firebase_service import firebase_service
        from config.firebase_config import firebase_config
        
        if firebase_config.db is None:
            print("❌ Firebase not configured")
            return False
        
        # Get all cards
        cards = firebase_service.get_all_cards()
        print(f"Found {len(cards)} cards in Firebase")
        
        if not cards:
            print("❌ No cards found to test")
            return False
        
        # Test updating the first card
        test_card = cards[0]
        original_status = test_card.get('status', 'unknown')
        new_status = 'done' if original_status != 'done' else 'todo'
        
        print(f"Testing card: {test_card['id']}")
        print(f"Original status: {original_status}")
        print(f"New status: {new_status}")
        
        # Update the status
        success = firebase_service.update_card(test_card['id'], {'status': new_status})
        
        if success:
            print("✅ Status update successful")
            
            # Verify the update
            updated_cards = firebase_service.get_all_cards()
            updated_card = next((c for c in updated_cards if c['id'] == test_card['id']), None)
            
            if updated_card and updated_card['status'] == new_status:
                print("✅ Status update verified")
                
                # Revert back to original status
                firebase_service.update_card(test_card['id'], {'status': original_status})
                print("✅ Status reverted back")
                
                return True
            else:
                print("❌ Status update not reflected")
                return False
        else:
            print("❌ Status update failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_status_update()
    sys.exit(0 if success else 1)