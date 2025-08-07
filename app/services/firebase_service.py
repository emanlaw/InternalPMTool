"""Firebase initialization and configuration service."""

import firebase_admin
from firebase_admin import credentials, firestore


def initialize_firebase():
    """Initialize Firebase admin SDK and return firestore client."""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate('firebase-service-account.json')
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        print("Firebase initialized successfully!")
        return db
        
    except Exception as e:
        print(f"Firebase initialization failed: {e}")
        print("ERROR: Please ensure firebase-service-account.json exists with valid credentials")
        return None


def get_firestore_client():
    """Get the firestore client, initializing if needed."""
    return initialize_firebase()