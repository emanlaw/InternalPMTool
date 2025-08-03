# Complete Firebase Setup Guide

## Quick Setup (Recommended)

### Step 1: Set up Firebase Credentials
```bash
python3.9 setup_firebase_credentials.py
```
Follow the interactive prompts to set up your Firebase service account key.

### Step 2: Test Firebase Connection
```bash
python3.9 test_firebase_connection.py
```
This will verify that Firebase is working correctly.

### Step 3: Migrate Existing Data
```bash
python3.9 migrate_to_firebase.py
```
This will move your existing JSON data to Firebase.

### Step 4: Start the Application
```bash
python3.9 run.py
```
Your application will now use Firebase as the primary database!

## Manual Setup

### 1. Firebase Console Setup
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project "pm-tool-internal" (or create it)
3. Enable Firestore Database:
   - Go to Firestore Database
   - Click "Create database"
   - Choose "Start in test mode"
   - Select location (us-central1 recommended)

### 2. Service Account Key
1. In Firebase Console, go to Project Settings (gear icon)
2. Go to "Service accounts" tab
3. Click "Generate new private key"
4. Download the JSON file
5. Replace the content of `firebase-service-account.json` with the downloaded content

### 3. Firestore Security Rules (Optional)
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

## Verification

After setup, verify everything works:

1. **Test Connection**: `python3.9 test_firebase_connection.py`
2. **Check Data**: Create a new issue and verify it appears in Firebase Console
3. **Analytics**: Visit `/analytics` to see Firebase data in charts

## Troubleshooting

### Common Issues

1. **"Firebase not available" error**
   - Check that `firebase-service-account.json` has valid credentials
   - Ensure Firestore is enabled in Firebase Console

2. **Permission denied errors**
   - Update Firestore security rules to allow read/write
   - Check that service account has proper permissions

3. **Data not appearing**
   - Run the migration script: `python3.9 migrate_to_firebase.py`
   - Check Firebase Console to see if data exists

### Firebase Console URLs
- Project: https://console.firebase.google.com/project/pm-tool-internal
- Firestore: https://console.firebase.google.com/project/pm-tool-internal/firestore
- Settings: https://console.firebase.google.com/project/pm-tool-internal/settings/general

## Data Structure

Firebase collections:
- `projects` - Project information
- `cards` - Task/issue cards  
- `comments` - Comments on cards
- `users` - User accounts (if needed)

## Benefits of Firebase

✅ Real-time updates
✅ Scalable database
✅ Built-in security
✅ Automatic backups
✅ Analytics and monitoring
✅ No server maintenance

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run the test scripts to identify the problem
3. Check Firebase Console for error logs
4. Ensure your internet connection is stable