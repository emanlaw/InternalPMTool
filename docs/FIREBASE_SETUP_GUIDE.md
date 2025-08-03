# 🔥 Firebase Setup Guide for PM Tool

## Step 1: Create Firebase Project

1. **Go to Firebase Console**: https://console.firebase.google.com/
2. **Click "Create a project"**
3. **Enter project name**: `pm-tool-internal` (or your preferred name)
4. **Enable Google Analytics** (optional but recommended)
5. **Click "Create project"**

## Step 2: Enable Firestore Database

1. **In Firebase Console**, go to **"Firestore Database"**
2. **Click "Create database"**
3. **Choose "Start in test mode"** (we'll add security rules later)
4. **Select location** closest to your users
5. **Click "Done"**

## Step 3: Enable Authentication

1. **Go to "Authentication"** in Firebase Console
2. **Click "Get started"**
3. **Go to "Sign-in method" tab**
4. **Enable "Email/Password"** authentication
5. **Save changes**

## Step 4: Get Firebase Configuration

1. **Go to Project Settings** (gear icon)
2. **Scroll down to "Your apps"**
3. **Click "Web app" icon** (</>) 
4. **Register app name**: `PM Tool Web`
5. **Copy the Firebase config object** - you'll need this!

```javascript
// Your Firebase config will look like this:
const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-app-id"
};
```

## Step 5: Install Firebase Dependencies

```bash
pip install firebase-admin
pip install pyrebase4
```

## Step 6: Download Service Account Key

1. **Go to Project Settings > Service accounts**
2. **Click "Generate new private key"**
3. **Download the JSON file**
4. **Save it as `firebase-service-account.json`** in your project root
5. **Add to .gitignore** to keep it secure

## Step 7: Create Firebase Configuration Files

I'll create the necessary configuration files for you next!

## Security Notes:
- ⚠️ Never commit service account keys to Git
- ⚠️ Use environment variables for sensitive data
- ⚠️ Set up proper Firestore security rules
- ⚠️ Enable Firebase App Check for production