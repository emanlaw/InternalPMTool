# 🔥 Firebase Setup Instructions

## Current Issue
Your app is trying to use Firebase but has a **mock/demo service account file**. You need to replace it with your real Firebase credentials.

## ✅ Step-by-Step Fix

### 1. Get Real Firebase Service Account Key
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project: **pm-tool-internal**
3. Click **⚙️ Project Settings** (gear icon)
4. Go to **Service Accounts** tab
5. Click **Generate new private key**
6. Download the JSON file

### 2. Replace Mock File
1. Rename the downloaded file to `firebase-service-account.json`
2. Replace the current mock file in your project root
3. The file should contain your real project credentials

### 3. Create Admin User
Run this command to create the admin user:
```bash
cd scripts
python create_admin_user.py
```

### 4. Test Login
- Username: `admin`
- Password: `admin123`
- Role: `admin` (full access)

## 🔒 Security Rules
Make sure your Firestore security rules allow authenticated access:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null;
    }
    match /projects/{projectId} {
      allow read, write: if request.auth != null;
      match /cards/{cardId} {
        allow read, write: if request.auth != null;
        match /comments/{commentId} {
          allow read, write: if request.auth != null;
        }
      }
    }
    match /notifications/{notificationId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## 🚨 Current Status
- ❌ Firebase: Using mock credentials (won't work)
- ❌ Admin User: Not created
- ❌ Login: Will fail until Firebase is properly configured

## ✅ After Setup
- ✅ Firebase: Real credentials
- ✅ Admin User: Created with full privileges
- ✅ Login: Working with admin/admin123
- ✅ Multi-user: Ready for team collaboration