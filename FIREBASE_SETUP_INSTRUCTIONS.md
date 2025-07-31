# Firebase Setup Instructions

## Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or use existing project "pm-tool-internal"
3. Enable Firestore Database in the project

## Step 2: Generate Service Account Key
1. In Firebase Console, go to Project Settings (gear icon)
2. Go to "Service accounts" tab
3. Click "Generate new private key"
4. Download the JSON file
5. Replace the content of `firebase-service-account.json` with the downloaded file

## Step 3: Set up Firestore Database
1. In Firebase Console, go to Firestore Database
2. Click "Create database"
3. Choose "Start in test mode" for now
4. Select a location (us-central1 recommended)

## Step 4: Configure Firestore Rules (Optional)
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read/write access to all documents
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

## Step 5: Test Connection
Run the test script to verify Firebase connection:
```bash
python3.9 test_firebase_connection.py
```

## Current Configuration
- Project ID: pm-tool-internal
- API Key: AIzaSyALJuHwbfgOEG0u1oigutLz713VpoZIVps
- Auth Domain: pm-tool-internal.firebaseapp.com

## Collections Structure
The app will create these collections:
- `users` - User accounts
- `projects` - Project information
- `cards` - Task/issue cards
- `comments` - Comments on cards