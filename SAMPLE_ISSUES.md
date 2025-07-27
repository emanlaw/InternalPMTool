# 🤖 Sample Issues for AI Coding Agents

Copy these into GitHub Issues to get AI agents to implement features:

## Issue #1: Add User Authentication
```
Title: [FEATURE] Add User Authentication System

Description:
Implement user login/logout functionality for the PM Tool.

Requirements:
- [ ] Login page with username/password form
- [ ] Session management using Flask-Login
- [ ] Protect routes (require login to access dashboard/issues/kanban)
- [ ] Simple user registration
- [ ] Logout functionality with redirect

Acceptance Criteria:
- [ ] Users can register with username/password
- [ ] Users can login and access protected pages
- [ ] Session persists across browser refresh
- [ ] Logout clears session and redirects to login

Files to Modify:
- app.py - Add auth routes and session management
- templates/login.html - New login page
- templates/register.html - New registration page
- templates/base.html - Add login/logout links
- requirements.txt - Add Flask-Login

@coding-agent please implement this feature
```

## Issue #2: Add Due Dates to Cards
```
Title: [FEATURE] Add Due Dates to Kanban Cards

Description:
Add due date functionality to cards with visual indicators for overdue items.

Requirements:
- [ ] Due date field in card creation modal
- [ ] Due date picker (HTML5 date input)
- [ ] Visual indicators (red border for overdue cards)
- [ ] Due date display on cards
- [ ] Sort/filter by due date in issues list

Acceptance Criteria:
- [ ] Cards can have optional due dates
- [ ] Overdue cards show red border/indicator
- [ ] Due dates visible on both Kanban and Issues views
- [ ] Issues list can be filtered by due date

Files to Modify:
- app.py - Update card model to include due_date
- templates/kanban.html - Add due date to card creation and display
- templates/issues.html - Show due dates in table
- templates/base.html - Add due date styling

@coding-agent please implement this feature
```

## Issue #3: Add Card Comments System
```
Title: [FEATURE] Add Comments to Cards

Description:
Allow users to add comments to cards for better collaboration.

Requirements:
- [ ] Comment section on card details
- [ ] Add new comments with timestamp
- [ ] Display all comments for a card
- [ ] Simple comment storage in JSON

Acceptance Criteria:
- [ ] Click card to open details modal
- [ ] Comments section shows all comments
- [ ] Can add new comments
- [ ] Comments show timestamp and author

Files to Modify:
- app.py - Add comment routes and data structure
- templates/kanban.html - Add card detail modal
- templates/issues.html - Add comment functionality
- Add new API endpoints for comments

@coding-agent please implement this feature
```

## Issue #4: Add Search and Filter
```
Title: [FEATURE] Add Search and Filter Functionality

Description:
Add search and filter capabilities across issues and cards.

Requirements:
- [ ] Search bar in issues list
- [ ] Filter by status, priority, assignee
- [ ] Real-time search (JavaScript)
- [ ] Clear filters button

Acceptance Criteria:
- [ ] Search works across title and description
- [ ] Multiple filters can be applied
- [ ] Search results update in real-time
- [ ] URL reflects current filters

Files to Modify:
- templates/issues.html - Add search/filter UI
- app.py - Add search API endpoint
- templates/base.html - Add search styling
- Add JavaScript for real-time search

@coding-agent please implement this feature
```