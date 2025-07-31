#!/usr/bin/env python3
"""
Quick Firebase status check
"""

def check_firebase_status():
    print("🔥 Firebase Status Check")
    print("=" * 30)
    
    try:
        from config.firebase_config import firebase_config
        
        if firebase_config.db is None:
            print("❌ Firebase is NOT configured")
            print("   Issue: Invalid service account credentials")
            print("   Solution: Run 'python3.9 setup_firebase_credentials.py'")
            return False
        else:
            print("✅ Firebase is configured and ready")
            return True
            
    except Exception as e:
        print(f"❌ Error checking Firebase: {e}")
        return False

if __name__ == "__main__":
    check_firebase_status()