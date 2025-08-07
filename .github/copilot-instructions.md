# Internal PM Tool Development Instructions

Always reference these instructions first and only fallback to additional search and context gathering if the information here is incomplete or found to be in error.

## Application Overview
Internal PM Tool is a Flask-based web application for project management featuring:
- User authentication and role management
- Project management with Kanban boards
- Issue tracking and sprint management
- Firebase Firestore backend with local JSON fallback
- Multi-user collaboration features

## Quick Start (Development)

### Bootstrap and Dependencies
Run these commands to set up the development environment:
```bash
cd /path/to/InternalPMTool
pip3 install -r requirements.txt
```
**Timing:** Dependencies install in ~30 seconds. NEVER CANCEL - always wait for completion.

### Running the Application

#### Option 1: Test Environment (Recommended for Development)
```bash
python3 testing_env/test_app.py
```
- **URL:** http://127.0.0.1:5002
- **Login:** admin / admin123
- **Data:** Uses local JSON files (no Firebase required)
- **Features:** Full functionality without Firebase setup

#### Option 2: Main Application (Requires Firebase)
```bash
python3 app.py
```
- **URL:** http://127.0.0.1:5000
- **Login:** admin / admin123 (if Firebase configured)
- **Data:** Uses Firebase Firestore
- **Note:** Shows Firebase errors but still runs if credentials missing

### Development Validation
Always run this validation after making changes:
```bash
# Quick structural validation
python3 -c "
import sys; sys.path.insert(0, '.');
from app import app;
print(f'✅ App has {len(list(app.url_map.iter_rules()))} routes');
print('✅ Basic validation passed')
"
```

## Working Effectively

### Project Structure
```
InternalPMTool/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── templates/               # HTML templates (19 files)
├── static/                  # CSS/JS assets
├── testing_env/            # Test environment with local data
│   ├── test_app.py         # Test server (port 5002)
│   └── data_manager.py     # Local data management
├── scripts/                # Utility scripts
├── docs/                   # Documentation
├── data.json              # Sample/fallback data
└── firebase-service-account.json  # Firebase credentials (if using Firebase)
```

### Key Files to Monitor
- **app.py** - Main application logic, Firebase integration
- **testing_env/test_app.py** - Local development server
- **templates/base.html** - Base template for UI changes
- **static/** - CSS/JS for frontend modifications
- **data.json** - Sample data structure reference

### Build and Test Process
There is NO complex build process. This is a standard Flask application:

1. **Install dependencies:** `pip3 install -r requirements.txt` (30 seconds)
2. **Run application:** `python3 app.py` OR `python3 testing_env/test_app.py`
3. **No compilation needed** - Python/Flask serves files directly
4. **No test suite** - Manual testing via browser required

**NEVER CANCEL:** While builds are fast (~30 seconds), always wait for pip install to complete.

## Firebase Configuration

### Without Firebase (Local Development)
Use the test environment for development without Firebase setup:
```bash
python3 testing_env/test_app.py
# Runs on port 5002, uses data.json for storage
```

### With Firebase (Production/Full Features)
1. **Download Firebase service account key** from Firebase Console
2. **Save as `firebase-service-account.json`** in project root
3. **Run main app:** `python3 app.py`

If Firebase credentials are missing, the app shows error messages but continues to run with limited functionality.

## Validation Scenarios

### Manual Testing Workflow
After making changes, ALWAYS test these scenarios:

#### Basic Functionality Test:
1. **Start app:** `python3 testing_env/test_app.py`
2. **Login:** Navigate to http://127.0.0.1:5002, login with admin/admin123
3. **Dashboard:** Verify dashboard loads with project stats
4. **Projects:** Create a new project, verify it appears
5. **Issues:** Add new issue/card, verify it saves
6. **Kanban:** Drag and drop cards between columns

#### Core Features Test:
- **Authentication:** Login/logout functionality
- **Project Management:** Create, edit, archive projects  
- **Issue Tracking:** Add, edit, move issues between statuses
- **User Interface:** Navigation, forms, responsive design

### Route Validation
The app defines 66+ routes. Key routes that must work:
- `/login` - User authentication
- `/dashboard` - Main dashboard
- `/issues` - Issue list and management
- `/kanban` - Kanban board view
- `/api/*` - JSON API endpoints

## Common Tasks

### Adding New Features
1. **Always develop in test environment first:** Use port 5002
2. **Modify templates:** Update HTML in `templates/` directory
3. **Add routes:** Add to `app.py` or test_app.py
4. **Test immediately:** Reload browser, verify functionality
5. **Check both environments:** Test in both test and main app

### Debugging Issues
1. **Check console output:** Flask shows detailed error messages
2. **Use test environment:** Simpler debugging without Firebase
3. **Verify templates:** Check template syntax and includes
4. **Check static files:** Ensure CSS/JS files are properly linked

### Database Changes
- **Test environment:** Modify `data.json` directly
- **Firebase environment:** Use Firebase Console or migration scripts
- **Always backup data** before structural changes

### Creating New Issues
When creating a new GitHub issue, follow this structure template:

```markdown
### 🔵 Issue #XX: [TYPE] Title - STATUS

Title: [TYPE] Brief Description

Status: OPEN/IN_PROGRESS/COMPLETED
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/XX

Description:
Brief overview of what needs to be implemented or fixed.

What I want:
- High-level feature requirements
- User-facing functionality goals
- Integration requirements

Current Issues:
- [ ] Specific problem 1
- [ ] Specific problem 2
- [ ] Missing functionality

Desired Features:
- [ ] Feature requirement 1 with details
- [ ] Feature requirement 2 with details
- [ ] UI/UX improvements needed

Technical Requirements:
- [ ] Backend changes needed
- [ ] Frontend template updates
- [ ] API endpoints to create
- [ ] Database schema changes

API Endpoints Needed:
- [ ] GET /api/resource - Description
- [ ] POST /api/resource - Description
- [ ] PUT /api/resource/{id} - Description

Acceptance Criteria:
- [ ] Functional requirement 1
- [ ] Functional requirement 2
- [ ] Performance/quality requirements

Priority: HIGH/MEDIUM/LOW
Estimated Effort: Small (1-2 days) / Medium (2-4 days) / Large (4-6 days)
Labels: enhancement, feature-type, priority-level
```

**Issue Types:**
- `[FEATURE]` - New functionality
- `[BUG]` - Bug fixes
- `[REFACTOR]` - Code organization/cleanup
- `[ENHANCEMENT]` - Improvements to existing features

**Common Labels:**
- Priority: `high-priority`, `medium-priority`, `low-priority`
- Type: `enhancement`, `bug`, `refactor`, `documentation`
- Area: `ui/ux`, `backend`, `frontend`, `api`, `database`
- Component: `sprint-management`, `issue-tracking`, `authentication`, `kanban`

## Known Issues and Workarounds

### Docker Build Fails
Docker build fails due to SSL certificate issues in CI environment:
```bash
docker build . -t internal-pm-tool
# ERROR: SSL certificate verification failed
```
**Workaround:** Use local Python development instead of Docker.

### Scripts Directory Import Issues  
Scripts in `scripts/` folder cannot import app module:
```bash
python3 scripts/run.py
# ModuleNotFoundError: No module named 'app'
```
**Workaround:** Run from project root: `python3 app.py`

### Missing Firebase Credentials
App shows Firebase errors but continues running:
```
Firebase initialization failed: [Errno 2] No such file or directory
```
**Workaround:** Use test environment or add proper Firebase credentials.

## Timing and Performance

### Command Timing (Measured)
- **Dependency install:** 29 seconds (pip3 install -r requirements.txt)
- **App startup:** 2-3 seconds
- **Page load:** <1 second (local development)
- **Docker build:** 17 seconds (but fails due to SSL issues)

### Timeout Recommendations
- **pip install:** Set timeout to 60 seconds minimum
- **App startup:** 30 seconds timeout sufficient
- **Docker build:** DO NOT USE - fails in CI environment

## Additional Information

### Technology Stack
- **Backend:** Flask 2.3.3, Python 3.8+
- **Database:** Firebase Firestore (with JSON fallback)
- **Authentication:** Flask-Login
- **Frontend:** HTML/CSS/JavaScript (no framework)
- **Dependencies:** See requirements.txt (4 main packages)

### Development Tips
- **Use test environment for rapid development** (port 5002)
- **Main app requires Firebase for full functionality** (port 5000)
- **Templates use Jinja2** - standard Flask templating
- **Static files served from /static/** directory
- **No build step required** - direct file serving

Always validate changes in the test environment before testing with Firebase integration.

## Data Structure Reference

### Sample Data Available
The repository includes sample data in `data.json`:
- **4 sample projects** (including 2 archived)
- **6 sample cards/issues** with different statuses
- **Sample users** with admin/admin123 credentials
- **Complete data structure examples** for reference

### Data Schema
```json
{
  "projects": [{"id": 1, "name": "Project", "description": "...", "archived": false}],
  "cards": [{"id": 1, "project_id": 1, "title": "Task", "status": "todo", "assignee": "user", "priority": "High"}],
  "users": [{"id": 1, "username": "admin", "password_hash": "...", "role": "admin"}],
  "epics": [{"id": 1, "project_id": 1, "name": "Epic", "description": "..."}],
  "stories": [{"id": 1, "epic_id": 1, "project_id": 1, "title": "Story"}],
  "comments": [{"id": 1, "card_id": 1, "author": "user", "content": "...", "created_at": "..."}]
}
```

## Quick Troubleshooting

### Application Won't Start
```bash
# Check Python version (3.8+ required)
python3 --version

# Reinstall dependencies 
pip3 install -r requirements.txt

# Try test environment instead
python3 testing_env/test_app.py
```

### Import Errors
```bash
# Run from project root directory
cd /path/to/InternalPMTool
python3 app.py

# NOT from subdirectories like scripts/
```

### Port Already in Use
```bash
# Check what's using the port
lsof -i :5000  # or :5002 for test environment

# Kill the process or use different port
# Edit app.run(port=5001) in the Python files
```

### Template Errors
- **Check template syntax:** Jinja2 templates in `templates/` directory
- **Verify includes:** Templates extend `base.html`
- **Check static files:** CSS/JS served from `static/` directory

### Firebase Connection Issues
- **Development:** Use test environment (port 5002) instead
- **Production:** Verify `firebase-service-account.json` exists and is valid
- **Troubleshoot:** Check Firebase Console for project status

## Command Reference Summary

```bash
# Essential Commands (copy-paste ready)
pip3 install -r requirements.txt                    # Install dependencies (30s)
python3 testing_env/test_app.py                     # Start test environment
python3 app.py                                      # Start main application
python3 -c "from app import app; print('✅ Routes:', len(list(app.url_map.iter_rules())))"  # Validate structure
```

Use test environment (port 5002) for most development work. Only use main app (port 5000) when testing Firebase integration.