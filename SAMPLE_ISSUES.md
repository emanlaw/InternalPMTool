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

## Issue #7: Enhanced Dark Mode Theme
```
Title: [FEATURE] Enhanced Dark Mode Toggle with Better Contrast

Description:
The current light theme is hard on the eyes during long work sessions. I want a dark mode option with proper contrast and readability.

What I want:
- Dark mode toggle button in header
- Complete dark theme for all pages with proper contrast
- Brighter font colors for better readability
- Saves user preference
- Smooth theme transition
- Accessibility compliance

Enhanced Features (Based on Feedback):
- [ ] Improved font contrast - use brighter colors against dark backgrounds
- [ ] Multiple contrast levels (Normal, High Contrast)
- [ ] System theme detection (auto dark/light based on OS preference)
- [ ] Color accessibility testing (WCAG 2.1 AA compliance)
- [ ] Custom accent colors for personalization
- [ ] Theme preview before applying
- [ ] Automatic theme switching based on time of day
- [ ] Export/import theme settings

Color Specifications (Enhanced for Maximum Brightness):
- [ ] Background: #1a1a1a (very dark gray, not pure black)
- [ ] Text: #f5f5f5 (very bright light gray - much brighter than before)
- [ ] Headers: #ffffff (pure white for maximum readability)
- [ ] Secondary Text: #e8e8e8 (bright gray for descriptions)
- [ ] Links: #64b5f6 (very bright blue for high visibility)
- [ ] Borders: #555555 (brighter gray for better separation)
- [ ] Cards/Panels: #2d2d2d (dark gray with high contrast text)
- [ ] Success: #a5d6a7 (very bright green)
- [ ] Warning: #ffcc02 (very bright yellow/orange)
- [ ] Error: #ff8a80 (very bright red)
- [ ] Button Text: #ffffff (pure white on colored backgrounds)
- [ ] Input Text: #f0f0f0 (very bright for form fields)

Acceptance Criteria:
- [ ] Toggle button switches between light/dark modes
- [ ] All pages support dark theme with proper contrast
- [ ] Font colors are bright enough for easy reading
- [ ] User preference saved in browser
- [ ] Dark theme passes accessibility contrast tests
- [ ] Maintains excellent readability in all lighting conditions
- [ ] No eye strain during extended use
- [ ] All UI elements clearly visible and distinguishable
- [ ] System theme detection works on all major browsers
- [ ] Smooth transitions without flickering

Technical Requirements:
- [ ] CSS custom properties for easy theme switching
- [ ] JavaScript for system theme detection
- [ ] LocalStorage for preference persistence
- [ ] Contrast ratio testing (minimum 4.5:1 for normal text)
- [ ] Support for prefers-color-scheme media query
- [ ] Fallback for browsers without system theme support

@coding-agent please implement this enhanced feature with proper contrast
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

## Issue #13: Interactive Mind Map for Project Planning
```
Title: [FEATURE] Interactive Mind Map Visualization

Description:
I want an interactive mind map feature to visualize project structure, brainstorm ideas, and show relationships between different project components.

What I want:
- Interactive mind map canvas with drag-and-drop nodes
- Different node types for different card statuses (TODO, In Progress, Done)
- Visual connections between related cards/ideas
- Collaborative editing capabilities
- Export mind maps as images or PDF

Detailed Features:
- [ ] Canvas-based mind map editor using HTML5 Canvas or SVG
- [ ] Node creation with double-click on canvas
- [ ] Drag nodes to reposition them
- [ ] Connect nodes with lines/arrows to show relationships
- [ ] Different node shapes/colors for different statuses:
  * Red circles for TODO items
  * Yellow squares for In Progress
  * Green diamonds for Done
  * Blue hexagons for Ideas/Brainstorming
- [ ] Node editing (double-click to edit text)
- [ ] Zoom in/out and pan functionality
- [ ] Save mind maps per project
- [ ] Link mind map nodes to actual cards
- [ ] Export options (PNG, PDF, JSON)
- [ ] Import existing project structure into mind map
- [ ] Collaborative features (multiple users editing simultaneously)
- [ ] Version history for mind maps
- [ ] Templates for common project structures

Acceptance Criteria:
- [ ] Users can create new mind maps from project dashboard
- [ ] Smooth drag-and-drop interaction for nodes
- [ ] Visual indicators clearly show different statuses
- [ ] Mind maps auto-save changes
- [ ] Export functionality works properly
- [ ] Mind map integrates with existing card system
- [ ] Responsive design works on tablets
- [ ] Performance remains smooth with 100+ nodes

Technical Implementation:
- Use libraries like D3.js, Fabric.js, or Konva.js for canvas manipulation
- WebSocket integration for real-time collaboration
- File storage for mind map data (JSON format)
- Image generation for exports

Files to Create/Modify:
- templates/mindmap.html - New mind map page
- static/js/mindmap.js - Mind map functionality
- static/css/mindmap.css - Mind map styling
- app/routes/main.py - Add mind map routes
- app/routes/api.py - Add mind map API endpoints

@coding-agent please implement this feature
```

## Issue #14: Interactive Gantt Chart for Sprint and Project Management
```
Title: [FEATURE] Interactive Gantt Chart for Project Timeline

Description:
I want a comprehensive Gantt chart feature to visualize project timelines, track sprint progress, manage dependencies, and provide overall project navigation.

What I want:
- Interactive Gantt chart showing all project tasks
- Sprint-based timeline visualization
- Task dependencies and critical path
- Progress tracking with visual indicators
- Resource allocation and workload management
- Multi-project view capabilities

Detailed Features:
- [ ] Interactive Gantt chart with timeline view
- [ ] Task bars showing duration and progress
- [ ] Drag-and-drop to reschedule tasks
- [ ] Sprint swimlanes for Agile methodology
- [ ] Dependency arrows between related tasks
- [ ] Critical path highlighting
- [ ] Progress indicators on task bars:
  * Green for completed tasks
  * Blue for in-progress tasks
  * Red for overdue tasks
  * Gray for not started
- [ ] Milestone markers for important deadlines
- [ ] Resource allocation view (who's working on what)
- [ ] Workload balancing indicators
- [ ] Zoom levels (day, week, month, quarter view)
- [ ] Filter by project, assignee, priority, or status
- [ ] Export to PDF, PNG, or MS Project format
- [ ] Baseline comparison (planned vs actual)
- [ ] Sprint burndown integration
- [ ] Time tracking integration
- [ ] Automatic scheduling based on dependencies
- [ ] What-if scenario planning
- [ ] Risk indicators for delayed tasks

Sprint Management Features:
- [ ] Sprint planning view with capacity planning
- [ ] Sprint backlog drag-and-drop from product backlog
- [ ] Sprint burndown charts
- [ ] Velocity tracking across sprints
- [ ] Sprint retrospective data integration
- [ ] Release planning with multiple sprints

Multi-Project Features:
- [ ] Portfolio view showing all projects
- [ ] Cross-project dependencies
- [ ] Resource conflicts highlighting
- [ ] Master timeline with all projects
- [ ] Project comparison and prioritization

Acceptance Criteria:
- [ ] Gantt chart loads quickly with 500+ tasks
- [ ] Smooth drag-and-drop rescheduling
- [ ] Dependencies update automatically when tasks move
- [ ] Sprint view clearly shows sprint boundaries
- [ ] Critical path calculation is accurate
- [ ] Export functions work properly
- [ ] Mobile-responsive design for tablets
- [ ] Real-time updates when multiple users edit
- [ ] Integration with existing card system
- [ ] Undo/redo functionality for changes

Technical Implementation:
- Use libraries like DHTMLX Gantt, Frappe Gantt, or custom D3.js implementation
- WebSocket for real-time collaboration
- Efficient data structures for large datasets
- Background processing for complex calculations
- Caching for performance optimization

Files to Create/Modify:
- templates/gantt.html - New Gantt chart page
- templates/sprint_planning.html - Sprint planning interface
- static/js/gantt.js - Gantt chart functionality
- static/js/sprint.js - Sprint management features
- static/css/gantt.css - Gantt chart styling
- app/routes/main.py - Add Gantt and sprint routes
- app/routes/api.py - Add Gantt API endpoints
- app/models/sprint.py - Sprint data model
- app/services/gantt_service.py - Gantt calculations and logic

@coding-agent please implement this feature
```

## Issue #15: Advanced Mind Map Features
```
Title: [FEATURE] Advanced Mind Map Capabilities

Description:
Extend the basic mind map with advanced features for complex project visualization and strategic planning.

Advanced Features:
- [ ] Mind map templates for different methodologies:
  * Agile/Scrum project structure
  * Waterfall project phases
  * Design thinking process
  * Risk assessment maps
  * Stakeholder analysis
- [ ] Smart auto-layout algorithms
- [ ] Mind map layers (show/hide different aspects)
- [ ] Integration with external tools (Jira, Trello, GitHub)
- [ ] AI-powered suggestions for node connections
- [ ] Presentation mode for stakeholder meetings
- [ ] Mind map analytics and insights
- [ ] Custom node types with icons and metadata
- [ ] Conditional formatting based on data
- [ ] Time-based mind map evolution (show changes over time)

@coding-agent please implement this feature
```

## Issue #16: Enhanced Gantt Chart Analytics
```
Title: [FEATURE] Gantt Chart Analytics and Reporting

Description:
Add comprehensive analytics and reporting capabilities to the Gantt chart for better project insights.

Analytics Features:
- [ ] Project health dashboard
- [ ] Predictive analytics for project completion
- [ ] Resource utilization reports
- [ ] Budget tracking integration
- [ ] Risk assessment and mitigation tracking
- [ ] Performance metrics and KPIs
- [ ] Automated project status reports
- [ ] Trend analysis and forecasting
- [ ] Comparative analysis between projects
- [ ] Custom report builder
- [ ] Scheduled report delivery via email
- [ ] Interactive dashboards with drill-down capabilities

@coding-agent please implement this feature
```