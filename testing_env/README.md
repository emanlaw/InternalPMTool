# Testing Environment

This is an isolated testing environment for developing new features without affecting the main application.

## Setup

1. **Start the testing server:**
   ```bash
   cd testing_env
   python3 test_app.py
   ```

2. **Access the testing app:**
   - URL: http://127.0.0.1:5002
   - Login: admin / admin123

## Features

- ✅ Isolated from main app (runs on port 5001)
- ✅ Uses local JSON files for data storage
- ✅ Same UI templates as main app
- ✅ Simplified authentication
- ✅ Epic/Story dropdown functionality
- ✅ Issue creation with Epic/Story selection

## Data Structure

- `data/projects.json` - Projects
- `data/epics.json` - Epics linked to projects
- `data/stories.json` - Stories linked to epics
- `data/cards.json` - Issues/cards linked to stories
- `data/users.json` - Users

## Testing Epic/Story Dropdowns

1. Go to Issues page: http://127.0.0.1:5002/issues
2. Click "Add Issue"
3. Select "Sample Project" from Project dropdown
4. Epic dropdown should populate with "Sample Project - Main Epic"
5. Select Epic → Story dropdown should populate with "Sample Project - Main Story"
6. Create issue and verify it appears in the table

## Development Workflow

1. Make changes in testing environment
2. Test thoroughly on port 5002
3. Once confirmed working, apply changes to main app
4. Main app continues running on port 5000 unaffected