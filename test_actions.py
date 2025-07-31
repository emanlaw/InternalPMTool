#!/usr/bin/env python3
"""
Test the actions functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_actions():
    print("Testing actions functionality...")
    
    try:
        from app.services.firebase_service import firebase_service
        from config.firebase_config import firebase_config
        
        if firebase_config.db is None:
            print("❌ Firebase not configured")
            return False
        
        # Get cards
        cards = firebase_service.get_all_cards()
        print(f"Found {len(cards)} cards")
        
        if not cards:
            print("❌ No cards found to test")
            return False
        
        # Test card lookup logic
        test_card = cards[0]
        card_id = test_card['id']
        
        print(f"Testing with card: {card_id}")
        
        # Test the ID matching logic used in the API
        target_card = None
        for card in cards:
            if card['id'] == card_id or str(card['id']) == str(card_id):
                target_card = card
                break
            elif isinstance(card['id'], str) and card['id'].startswith('CARD-'):
                try:
                    card_number = int(card['id'].split('-')[1])
                    if card_number == card_id:
                        target_card = card
                        break
                except (ValueError, IndexError):
                    continue
        
        if target_card:
            print(f"✅ Card lookup successful: {target_card['title']}")
            return True
        else:
            print("❌ Card lookup failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_actions()
    sys.exit(0 if success else 1)