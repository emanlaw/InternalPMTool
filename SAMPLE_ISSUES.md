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

## Issue #5: Export to Excel Functionality
```
Title: [FEATURE] Export Issues to Excel

Description:
I want to export all issues/cards to an Excel file for reporting and offline analysis.

What I want:
- Export button on Issues page
- Download Excel file with all card data
- Include all important columns
- Professional formatting

Acceptance Criteria:
- [ ] Export button downloads Excel file immediately
- [ ] File contains: Title, Status, Priority, Assignee, Due Date, Created Date, Comments Count
- [ ] File opens properly in Excel/Google Sheets
- [ ] Filename includes current date
- [ ] Works with filtered results

@coding-agent please implement this feature
```

## Issue #6: Email Notifications for Overdue Cards
```
Title: [FEATURE] Email Notifications System

Description:
As a project manager, I want to receive email notifications when cards are overdue, so I can follow up with team members.

What I want:
- Daily email digest of overdue cards
- Email settings in user profile
- Professional email templates
- Option to enable/disable notifications

Acceptance Criteria:
- [ ] Users can set email preferences
- [ ] Daily email sent with overdue cards list
- [ ] Email includes card details and direct links
- [ ] Users can unsubscribe from notifications
- [ ] Email template looks professional

@coding-agent please implement this feature
```

## Issue #7: Dark Mode Theme
```
Title: [FEATURE] Dark Mode Toggle

Description:
The current light theme is hard on the eyes during long work sessions. I want a dark mode option.

What I want:
- Dark mode toggle button in header
- Complete dark theme for all pages
- Saves user preference
- Smooth theme transition

Acceptance Criteria:
- [ ] Toggle button switches between light/dark modes
- [ ] All pages support dark theme
- [ ] User preference saved in browser
- [ ] Dark theme is easy on the eyes
- [ ] Maintains good contrast and readability

@coding-agent please implement this feature
```

## Issue #8: Card Labels/Tags System
```
Title: [FEATURE] Add Colored Labels to Cards

Description:
I want to add colored labels/tags to cards for better organization (like "Bug", "Feature", "Urgent").

What I want:
- Add labels when creating/editing cards
- Predefined label types with colors
- Show labels on cards with colors
- Filter by labels in issues list

Acceptance Criteria:
- [ ] Label selector in card creation modal
- [ ] Predefined labels: Bug (red), Feature (blue), Urgent (orange), Enhancement (green)
- [ ] Labels displayed as colored badges on cards
- [ ] Filter dropdown for labels in issues list
- [ ] Multiple labels per card supported

@coding-agent please implement this feature
```

## Issue #9: Time Tracking Features
```
Title: [FEATURE] Time Tracking for Cards

Description:
I want to track time spent on cards to measure productivity and estimate future work.

What I want:
- Start/stop timer on cards
- Log time manually
- Time reports and analytics
- Estimated vs actual time comparison

Acceptance Criteria:
- [ ] Timer widget in card details modal
- [ ] Manual time entry option
- [ ] Time logs with timestamps
- [ ] Total time spent displayed on cards
- [ ] Time tracking reports page
- [ ] Estimated time field for planning

@coding-agent please implement this feature
```

## Issue #10: Team Collaboration Tools
```
Title: [FEATURE] Enhanced Team Collaboration

Description:
I want better team collaboration features like @mentions, notifications, and activity feeds.

What I want:
- @mention users in comments
- Activity feed showing recent changes
- User profiles with avatars
- Real-time notifications

Acceptance Criteria:
- [ ] @username mentions in comments trigger notifications
- [ ] Activity feed on dashboard showing recent card changes
- [ ] User profile pages with avatar upload
- [ ] In-app notification system
- [ ] Email notifications for mentions

@coding-agent please implement this feature
```

## Issue #11: Mobile Responsive Design
```
Title: [FEATURE] Mobile-Friendly Interface

Description:
The current interface doesn't work well on mobile devices. I want a responsive design that works on phones and tablets.

What I want:
- Mobile-optimized navigation
- Touch-friendly Kanban board
- Responsive tables and modals
- Mobile-first design approach

Acceptance Criteria:
- [ ] Interface works perfectly on phones (320px+)
- [ ] Tablet-optimized layout (768px+)
- [ ] Touch-friendly drag and drop
- [ ] Mobile navigation menu
- [ ] All modals work on mobile
- [ ] Fast loading on mobile networks

@coding-agent please implement this feature
```

## Issue #12: Database Integration (PostgreSQL)
```
Title: [FEATURE] Migrate from JSON to PostgreSQL Database

Description:
The current JSON file storage is not scalable. I want to migrate to a proper PostgreSQL database for better performance and reliability.

What I want:
- PostgreSQL database setup
- Migrate all existing data
- Improved performance
- Data backup and recovery

Acceptance Criteria:
- [ ] PostgreSQL database schema created
- [ ] All JSON data migrated successfully
- [ ] Database connection pooling
- [ ] Improved query performance
- [ ] Database migrations system
- [ ] Backup and restore procedures
- [ ] All existing features work with database

@coding-agent please implement this feature
```