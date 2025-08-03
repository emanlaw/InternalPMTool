# Project Context for Amazon Q

## 📋 Project Overview
**Name:** Internal PM Tool  
**Type:** Flask web application for project management  
**Target:** Multi-user team collaboration  
**Current Status:** Production-ready, Firebase-enabled  

## 🏗️ Architecture
- **Backend:** Flask (Python)
- **Database:** Firebase Firestore (hierarchical structure)
- **Authentication:** Flask-Login
- **Frontend:** HTML/CSS/JavaScript (no framework)
- **Deployment:** Local development, cloud-ready

## 🔥 Firebase Structure
```
projects/
├── {projectId}/
│   ├── name, description, created_at
│   └── cards/
│       ├── {cardId}/
│       │   ├── title, status, priority, assignee, due_date
│       │   └── comments/
│       │       └── {commentId}/
│       │           └── author, content, created_at
users/
└── {userId}/
    └── username, password_hash, email, email_notifications
```

## 🛠️ Tech Stack
```
Flask==2.3.3
Flask-Login==0.6.3
Werkzeug==2.3.7
firebase-admin==6.2.0
```

## 📁 Key Files
- `app.py` - Main Flask application (Firebase-enabled)
- `firebase-service-account.json` - Firebase credentials
- `templates/` - HTML templates
- `static/` - CSS/JS assets
- `data.json` - Legacy storage (now using Firebase)

## 🔧 Cross-Platform Issues Solved
- **Import conflicts:** Renamed `app/` directory to `app_modules/`
- **Windows compatibility:** Fixed path handling and dependencies
- **Firebase integration:** Migrated from JSON to Firestore
- **Template errors:** Added missing helper functions

## 🚀 Core Features
- ✅ User authentication (login/register/logout)
- ✅ Project management
- ✅ Kanban boards with drag-drop
- ✅ Issues list with search/filter
- ✅ Card comments system
- ✅ Due date tracking with overdue indicators
- ✅ Firebase dashboard and migration tools
- ✅ Export to Excel functionality

## 🔐 Firebase Security Rules
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
  }
}
```

## 🎯 Current Development Status
- **Database:** Fully migrated to Firebase Firestore
- **Multi-user:** Ready for team collaboration
- **Cross-platform:** Works on both Mac and Windows
- **Production:** All core features implemented and tested

## 🔄 Recent Major Changes
1. **Firebase Migration:** Moved from JSON file storage to Firestore
2. **Hierarchical Structure:** Cards nested under projects, comments under cards
3. **Windows Compatibility:** Fixed all cross-platform issues
4. **Template Functions:** Restored all missing helper functions

## 🚨 Known Issues
- None currently - all major issues resolved

## 🎮 How to Run
```bash
pip install -r requirements.txt
python app.py
# Access: http://127.0.0.1:5000
# Default login: admin/admin123
```

## 📝 Quick Start for Amazon Q
When starting on a new device, use this context:
"I'm working on a Flask PM tool with Firebase Firestore. It has hierarchical data structure (projects/cards/comments), user authentication, and full CRUD operations. All cross-platform issues are resolved. Current setup is production-ready."