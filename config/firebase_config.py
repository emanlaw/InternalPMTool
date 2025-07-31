import os
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

class FirebaseConfig:
    def __init__(self):
        # Firebase Admin SDK (for server-side operations)
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate('firebase-service-account.json')
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except Exception as e:
            print(f"Firebase not available, using JSON: {e}")
            self.db = None
        
        # Pyrebase config (for client-side operations)
        self.firebase_config = {
            "apiKey": "AIzaSyALJuHwbfgOEG0u1oigutLz713VpoZIVps",
            "authDomain": "pm-tool-internal.firebaseapp.com",
            "projectId": "pm-tool-internal",
            "storageBucket": "pm-tool-internal.firebasestorage.app",
            "messagingSenderId": "484464547872",
            "appId": "1:484464547872:web:2f41292118389abfbb8445",
            "databaseURL": ""  # Not needed for Firestore
        }
        
        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.auth = self.firebase.auth()

# Global Firebase instance
firebase_config = FirebaseConfig()