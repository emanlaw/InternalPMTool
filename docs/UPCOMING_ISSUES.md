# 🚀 Upcoming Issues - To Be Implemented

## ✅ COMPLETED ISSUES (CLOSED)
- ✅ Issue #1: [FEATURE] Add User Authentication - CLOSED
- ✅ Issue #2: [FEATURE] Add Due Dates to Cards - CLOSED  
- ✅ Issue #3: [FEATURE] Add Card Comments System - CLOSED
- ✅ Issue #4: [FEATURE] Add Search and Filter - CLOSED
- ✅ Issue #5: [FEATURE] Export to Excel Functionality - CLOSED
- ✅ Issue #6: [FEATURE] Email Notifications for Overdue Cards - CLOSED
- ✅ Issue #7: [FEATURE] Dark Mode Theme - CLOSED
- ✅ Issue #12: [VERSION 1.1] Issues List - CLOSED
- ✅ Issue #13: [FEATURE] Database Integration (PostgreSQL) - CLOSED
- ✅ Issue #14: [FEATURE] Interactive Mind Map for Project Planning - CLOSED
- ✅ Issue #15: [FEATURE] Interactive Gantt Chart for Sprint and Project Management - CLOSED
- ✅ Issue #16: [FEATURE] Advanced Mind Map Features - CLOSED
- ✅ Issue #17: [FEATURE] Enhanced Gantt Chart Analytics - CLOSED
- ✅ Issue #18: [BUG] Fix Issues List Status Updates and Filtering - CLOSED
- ✅ Issue #23: [FEATURE] Add Actions Dropdown for Issue Management - CLOSED
- ✅ Issue #24: [FEATURE] Create Backlog Page with Advanced Filtering - CLOSED

- ✅ Issue #26: [FEATURE] Project Archive System with Dashboard Integration - CLOSED
- ✅ Issue #10: [FEATURE] Team Collaboration Tools - CLOSED

**Note:** Issue #24 (Backlog Page) was implemented but remains OPEN on GitHub for additional enhancements.

## 🔄 OPEN ISSUES (IN PROGRESS/TODO)

### 🔵 **Issue #8:** ***Card Labels/Tags System*** - OPEN
```
Title: [FEATURE] #8 Card Labels/Tags System

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/8

Description:
I want to add colored labels/tags to cards for better organization (like "Bug", "Feature", "Urgent").

What I want:

Acceptance Criteria:

@coding-agent please implement this feature
```
### Issue #9: Enhanced Issue Creation/Editing & Backlog Placement

**Feature Title:**
Enhanced Issue Creation/Editing: Select Epic, Story, and Backlog Placement

**Description:**
Update the “Create Issue” and “Edit Issue” modals on the Issues List page to allow users to:
- Select a relevant Epic (from available epics in the project)
- Choose a Story within the chosen Epic (if the Epic contains Stories)
- Move or assign issues directly into the Product Backlog during creation/editing

**What is Being Requested?**
- Epic Selector: Dropdown list of all epics in the project
- Story Selector: After selecting an Epic, dynamically populate a dropdown with all child Stories; user may select one (optional if no stories)
- Backlog Checkbox/Option: Checkbox or dropdown to place this issue directly into the Backlog
- On editing an issue: Ability to change its Epic and Story assignment, move/remove the issue from the Backlog

**Acceptance Criteria:**
- Epic field shown and required if project has Epics
- Story field shown and enabled/required only when an Epic with child Stories is selected
- Issues are linked to the chosen Epic (and optionally Story) in the data model
- Issue is placed into the Backlog if user selects that option
- Editing an issue allows user to update Epic, Story, and Backlog placement
- UI updates are reflected immediately on the Issues List page
- Changes are persisted to backend (e.g., Firebase or DB)
- Validation prevents saving without required fields (e.g., Epic must be selected if available)
- Epic/Story selection in UI dynamically filters Stories once Epic is selected
- Issues can be removed from or moved into the Backlog via a clear UI control
- All standard issue fields (title, description, assignee, etc.) maintained
- Seamless user experience: minimizing required clicks, clear error feedback

**Technical Notes / UI Guidance:**
- Add Epic and Story dropdown fields (Story field disables/hides if no Epic or if Epic has no child stories).
- Backlog option could be a checkbox or a dropdown status.
- On the backend, maintain direct references (foreign keys or parent IDs) for Epic and Story.
- Whenever an issue is updated, ensure project-level hierarchy and integrity: issue-to-story-to-epic structure remains valid.
- Ensure support for bulk moves (drag-and-drop to Backlog, bulk-edit to change Epic/Story).

**Related Features:**
- Issue hierarchy: Epic > Story > Issue (recently implemented)
- Product Backlog (already available but needs more seamless assignments from Issues)

**Stakeholders:**
- @coding-agent
- Frontend/UI team
- Product/Project Owners

**Priority & Labels:**
- Priority: High
- Labels: enhancement, issue-creation, epic-story-link, backlog, ui/ux

### 🔵 **Issue #9:** ~~Time Tracking Features~~ - OPEN
```
Title: [FEATURE] Time Tracking Features

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/9

Description:
I want to track time spent on cards to measure productivity and estimate future work.

- Time reports and analytics
- Estimated vs actual time comparison
- [ ] Manual time entry option
- [ ] Time logs with timestamps
- [ ] Total time spent displayed on cards
- [ ] Time tracking reports page
- [ ] Estimated time field for planning

@coding-agent please implement this feature
```

### 🔵 **Issue #25:** __User Registration System with Admin Control__ - OPEN
```
Title: [FEATURE] User Registration System with Admin Control

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/25

Description:
Implement a comprehensive user registration system with admin control that allows new users to register and provides admin management capabilities.

What I want:
- Enhanced registration page with display name, email, and password fields
- Admin notification system for new registrations
- Admin dashboard to view and manage registered users
- User permission levels (Admin, Manager, User, Viewer)
- Secure registration process with validation

Core Registration Features:
- [ ] Enhanced registration form (display name, email, username, password + confirmation)
- [ ] Email validation and uniqueness check
- [ ] Password strength requirements and confirmation validation
- [ ] User account creation with pending status by default
- [ ] Client-side form validation with real-time feedback
- [ ] Registration success confirmation with admin approval notice

Admin Management Features:
- [ ] Admin dashboard at /admin/users
- [ ] View all registered users with filtering and search
- [ ] User status management (Pending, Active, Suspended, Inactive)
- [ ] User permission levels control
- [ ] Bulk user operations (Approve, Reject, Suspend multiple users)
- [ ] Real-time status and role updates via AJAX

Security Features:
- [ ] Password hashing and secure storage
- [ ] Input sanitization and validation
- [ ] User status validation during login
- [ ] Admin privilege checking
- [ ] Role-based access control

@coding-agent please implement this comprehensive feature
```

### 🔵 **Issue #11:** *Mobile Responsive Design* - OPEN
```
Title: [FEATURE] Mobile Responsive Design

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/11

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

### 🔵 **Issue #19:** **Enhanced Dark Mode Toggle with Better Contrast** - OPEN
```
Title: [FEATURE] Enhanced Dark Mode Toggle with Better Contrast

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/19

Description:
The current light theme is hard on the eyes during long work sessions. I want a dark mode option with proper contrast and readability.

What I want:
- Dark mode toggle button in header
- Complete dark theme for all pages with proper contrast
- Brighter font colors for better readability
- Saves user preference
- Smooth theme transition
- Accessibility compliance

Enhanced Features:
- [ ] Improved font contrast - use brighter colors against dark backgrounds
- [ ] Multiple contrast levels (Normal, High Contrast)
- [ ] System theme detection (auto dark/light based on OS preference)
- [ ] Color accessibility testing (WCAG 2.1 AA compliance)
- [ ] Custom accent colors for personalization

Color Specifications:
- [ ] Background: #1a1a1a (very dark gray, not pure black)
- [ ] Text: #f5f5f5 (very bright light gray)
- [ ] Headers: #ffffff (pure white for maximum readability)
- [ ] Links: #64b5f6 (very bright blue for high visibility)
- [ ] Cards/Panels: #2d2d2d (dark gray with high contrast text)

Technical Requirements:
- [ ] CSS custom properties for easy theme switching
- [ ] JavaScript for system theme detection
- [ ] LocalStorage for preference persistence
- [ ] Contrast ratio testing (minimum 4.5:1 for normal text)

@coding-agent please implement this enhanced feature with proper contrast
```

### 🔵 **Issue #20:** _Add Colored Labels to Cards_ - OPEN
```
Title: [FEATURE] Add Colored Labels to Cards

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/20

Description:
I want to add colored labels/tags to cards for better organization (like Bug, Feature, Urgent).

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

### 🔵 **Issue #21:** > Time Tracking for Cards - OPEN
```
Title: [FEATURE] Time Tracking for Cards

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/21

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


```
Title: [FEATURE] Enhanced Issues List Modal with Required Fields

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/28

Description:
Improve the Issues List page Add Issue modal to prevent accidental closure and enforce required field validation.

What I want:
- Modal that only closes via Create Issue or Cancel buttons
- Prevent clicking outside modal to close
- Required field validation for issue title, assignee, and target date
- Better user experience with clear validation messages

Acceptance Criteria:
- [ ] Modal cannot be closed by clicking outside the modal area
- [ ] Only "Create Issue" and "Cancel" buttons can close the modal
- [ ] Issue title field is required and validated
- [ ] Assignee field is required with dropdown selection
- [ ] Target date field is required with date picker
- [ ] Form validation prevents submission with missing required fields
- [ ] Clear error messages for validation failures
- [ ] Improved modal styling and user experience

@coding-agent please implement this feature
```

### ✅ **Issue #30:** **[BUG] Gantt Chart Shows Archived Projects** - COMPLETED
```
Title: [BUG] Gantt Chart Shows Archived Projects in Dropdown

Status: COMPLETED ✅
Completed Date: 2025-01-08
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/30

Description:
The Gantt Chart page was displaying archived projects in the project dropdown list and throughout the interface. Fixed to ensure archived projects only appear on the Archive page.

What was fixed:
✅ Gantt Chart now only shows active (non-archived) projects
✅ Project dropdown excludes archived projects
✅ Analytics exclude archived project data
✅ Project filtering is consistent across all pages
✅ Archived projects only visible on Archive page
✅ Clear separation between active and archived projects

Technical Implementation:
✅ Updated /gantt route: `projects = [p for p in data.get('projects', []) if not p.get('archived', False)]`
✅ Added JavaScript filtering: `ganttData.projects = ganttData.projects.filter(project => !project.archived);`
✅ Applied filtering to /analytics, /issues, /backlog, /stories, /epics routes
✅ Ensured consistent project filtering logic across all pages
✅ Created comprehensive test script to verify functionality

Files Modified:
- app.py: Updated gantt(), analytics(), issues_list(), backlog(), stories(), epics() routes
- templates/gantt.html: Added client-side filtering in JavaScript
- test_gantt_fix.py: Created test script to verify functionality

Test Results:
✅ All tests passed - archived projects properly filtered out
✅ Gantt Chart shows only active projects
✅ Project dropdowns exclude archived projects
✅ Analytics exclude archived project data
✅ Consistent behavior across all pages

Priority: HIGH - RESOLVED
```

### 🟢 **Issue #31:** ***[FEATURE] Enhanced Gantt Chart Date Navigation and Timeline View*** - OPEN
```
Title: [FEATURE] Enhanced Gantt Chart Date Navigation and Timeline View

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/31

Description:
Improve the Gantt Chart date indication and schedule navigation with a better timeline view similar to modern project management tools like Monday.com, Asana, or Microsoft Project.

What I want:
- Better date navigation with timeline controls
- Improved date indication and visual timeline
- Modern schedule navigation interface
- Zoom levels for different time periods (days, weeks, months)
- Clear date markers and grid lines

Current Issues:
- [ ] Basic date display lacks visual clarity
- [ ] No timeline navigation controls
- [ ] Missing zoom functionality for different time scales
- [ ] Poor date indication on project bars
- [ ] No interactive date selection

Desired Features:
- [ ] Timeline header with clear date markers
- [ ] Zoom controls (Day/Week/Month/Quarter view)
- [ ] Interactive date navigation (prev/next buttons)
- [ ] Today indicator line
- [ ] Weekend highlighting
- [ ] Milestone markers
- [ ] Date range selector
- [ ] Mini calendar for quick navigation

Inspiration from Market Leaders:
- [ ] Monday.com style timeline header
- [ ] Asana's zoom and navigation controls
- [ ] Microsoft Project's date grid system
- [ ] Smartsheet's timeline interface
- [ ] TeamGantt's date navigation

Technical Requirements:
- [ ] Update gantt.html with modern timeline header
- [ ] Add JavaScript for zoom and navigation controls
- [ ] Implement responsive date scaling
- [ ] Add CSS for better visual date indicators
- [ ] Create interactive timeline controls
- [ ] Ensure mobile-friendly date navigation

Acceptance Criteria:
- [ ] Timeline header shows clear date markers
- [ ] Zoom controls work smoothly (Day/Week/Month)
- [ ] Navigation buttons allow easy date browsing
- [ ] Today indicator is clearly visible
- [ ] Date selection is intuitive and responsive
- [ ] Visual design matches modern PM tools
- [ ] Works well on both desktop and mobile

@coding-agent please implement this enhanced timeline feature
```

### 🔵 **Issue #32:** `Enhanced Product Backlog Item Creation with Required Fields` - OPEN
```
Title: [FEATURE] Enhanced Product Backlog Item Creation with Required Fields

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/32

Description:
Enhance the Product Backlog page with improved item creation similar to the Issues creation process, with mandatory field validation and better user experience.

What I want:
- Enhanced backlog item creation modal with required fields
- Project selection dropdown (mandatory)
- Backlog item title field (mandatory)
- Assignee selection dropdown (mandatory)
- Form validation to prevent submission with missing required fields
- Better user experience similar to issue creation

Current Issues:
- [ ] Basic backlog item creation lacks required field validation
- [ ] No mandatory project selection
- [ ] Missing assignee requirement
- [ ] Inconsistent UX compared to issue creation
- [ ] No form validation for required fields

Desired Features:
- [ ] Modal with required field validation
- [ ] Project dropdown with active projects only
- [ ] Assignee dropdown with team members
- [ ] Backlog item title with character validation
- [ ] Priority selection (optional)
- [ ] Story points estimation (optional)
- [ ] Description field (optional)
- [ ] Due date picker (optional)

Acceptance Criteria:
- [ ] Project selection is mandatory and validated
- [ ] Backlog item title is required (minimum 3 characters)
- [ ] Assignee selection is mandatory from team members
- [ ] Form prevents submission with missing required fields
- [ ] Clear error messages for validation failures
- [ ] Modal cannot be closed by clicking outside
- [ ] Only "Create Item" and "Cancel" buttons close modal
- [ ] Success message after item creation
- [ ] Consistent styling with issue creation modal

Technical Requirements:
- [ ] Update backlog.html with enhanced creation modal
- [ ] Add client-side form validation JavaScript
- [ ] Implement server-side validation in backend
- [ ] Add required field indicators in form
- [ ] Ensure responsive design for mobile devices
- [ ] Add loading states during form submission

Optional Enhancements:
- [ ] Bulk backlog item creation
- [ ] Template-based item creation
- [ ] Import from CSV functionality
- [ ] Auto-save draft functionality

@coding-agent please implement this enhanced backlog creation feature
```

### 🔵 **Issue #34:** **[FEATURE] Enhanced Sprint Management with Epic/Story/Issue Selection** - OPEN
```
Title: [FEATURE] Enhanced Sprint Management with Epic/Story/Issue Selection

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/34

Description:
Enhance the Sprint Management page with advanced functionality for viewing, starting, and editing sprints with hierarchical Epic/Story/Issue selection capabilities.

What I want:
- View function: Dropdown showing epics assigned to the sprint
- Start function: Confirmation dialog when starting a sprint
- Edit function: Comprehensive sprint editing interface with hierarchical selection
- Sprint planning with Epic > Story > Issue hierarchy
- Drag-and-drop or checkbox selection for sprint items

Current Issues:
- [ ] View button only shows placeholder text
- [ ] Start button has no confirmation dialog
- [ ] Edit button shows placeholder message
- [ ] No epic/story/issue assignment to sprints
- [ ] No hierarchical sprint planning interface

Desired Features:

**View Function:**
- [ ] Dropdown/expandable view showing assigned epics
- [ ] Each epic shows its stories and issues
- [ ] Progress indicators for epic/story completion
- [ ] Sprint burndown visualization
- [ ] Issue status breakdown (todo/in-progress/done)

**Start Function:**
- [ ] Confirmation dialog: "Are you sure you want to start this sprint?"
- [ ] Sprint status changes from 'planning' to 'active'
- [ ] Start date validation (cannot start past sprints)
- [ ] Notification to team members about sprint start
- [ ] Sprint metrics initialization

**Edit Function:**
- [ ] Modal popup with sprint editing interface
- [ ] Basic sprint details (name, dates, goal, story points)
- [ ] Hierarchical epic/story/issue selection tree
- [ ] Expandable epic nodes showing stories
- [ ] Expandable story nodes showing issues
- [ ] Checkbox selection for epics/stories/issues
- [ ] Drag-and-drop support for adding/removing items
- [ ] Real-time story points calculation
- [ ] Sprint capacity warnings

**Sprint Planning Interface:**
- [ ] Left panel: Available epics/stories/issues
- [ ] Right panel: Selected sprint items
- [ ] Search and filter functionality
- [ ] Bulk selection options
- [ ] Story points estimation display
- [ ] Sprint capacity indicator

Technical Requirements:
- [ ] Update sprints.html with enhanced action buttons
- [ ] Create sprint view modal with epic dropdown
- [ ] Implement start sprint confirmation dialog
- [ ] Build comprehensive sprint edit modal
- [ ] Add hierarchical tree component for epic/story/issue selection
- [ ] Implement drag-and-drop functionality
- [ ] Add real-time story points calculation
- [ ] Create sprint item assignment API endpoints
- [ ] Update sprint status management
- [ ] Add sprint progress tracking

API Endpoints Needed:
- [ ] GET /api/sprints/{id}/items - Get sprint assigned items
- [ ] POST /api/sprints/{id}/items - Add items to sprint
- [ ] DELETE /api/sprints/{id}/items/{itemId} - Remove item from sprint
- [ ] PUT /api/sprints/{id}/start - Start sprint
- [ ] PUT /api/sprints/{id} - Update sprint details
- [ ] GET /api/projects/{id}/hierarchy - Get project epic/story/issue tree

Acceptance Criteria:
- [ ] View button shows dropdown with assigned epics and their stories/issues
- [ ] Start button shows confirmation dialog and updates sprint status
- [ ] Edit button opens comprehensive sprint planning interface
- [ ] Users can select/unselect epics, stories, and issues for sprint
- [ ] Real-time story points calculation during sprint planning
- [ ] Sprint capacity warnings when overloaded
- [ ] Hierarchical tree view with expand/collapse functionality
- [ ] Drag-and-drop support for intuitive sprint planning
- [ ] Changes are saved to Firebase for multi-user access
- [ ] Sprint progress tracking and visualization

Priority: HIGH
Estimated Effort: Large (4-6 days)
Labels: enhancement, sprint-management, ui/ux, high-priority

@coding-agent please implement this enhanced sprint management system
```

### ✅ **Issue #33:** **[FEATURE] Implement Hierarchical Project Structure: Project > Epic > Story > Issue > Sub-Issue** - COMPLETED
```
Title: [FEATURE] Implement Hierarchical Project Structure: Project > Epic > Story > Issue > Sub-Issue

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/33

Description:
Implement a proper hierarchical project management structure to better organize work items and improve sprint planning capabilities.

Current Structure:
- Projects contain Cards/Issues (flat structure)

Proposed Hierarchy:
Project (highest level)
├── Epic (large feature/initiative)
│   ├── Story (user story/feature)
│   │   ├── Issue (task/bug)
│   │   │   └── Sub-Issue (optional subtasks)
│   │   └── Issue
│   └── Story
└── Epic

Sprint Integration:
- Sprints can pick entire Epics or individual Stories
- Flexible sprint planning based on capacity
- Better tracking of epic/story completion

Data Structure Changes:
- [ ] Create Epic model with project relationship
- [ ] Create Story model with epic relationship
- [ ] Update Issue model to belong to Story
- [ ] Add Sub-Issue model for task breakdown
- [ ] Update Firebase schema for hierarchical data

New Pages & Features:
- [ ] Stories page (/stories) for story management
- [ ] Epic management within projects
- [ ] Hierarchical navigation and breadcrumbs
- [ ] Story creation and editing interface
- [ ] Epic-to-story assignment interface

Sprint Planning Updates:
- [ ] Sprint planning board with epic/story selection
- [ ] Drag-and-drop from epics/stories to sprints
- [ ] Sprint capacity planning by story points
- [ ] Epic progress tracking across sprints

UI/UX Improvements:
- [ ] Hierarchical tree view for project structure
- [ ] Epic/Story/Issue status indicators
- [ ] Progress bars for epic completion
- [ ] Filtering by epic/story in all views

Database Schema:
projects/
├── {projectId}/
│   ├── epics/
│   │   ├── {epicId}/
│   │   │   └── stories/
│   │   │       ├── {storyId}/
│   │   │       │   └── issues/
│   │   │       │       ├── {issueId}/
│   │   │       │       │   └── sub_issues/
│   │   │       │       │       └── {subIssueId}/

Acceptance Criteria:
- [ ] All existing functionality preserved during migration
- [ ] New hierarchical structure fully functional
- [ ] Sprint planning works with new structure
- [ ] Data migration script for existing projects
- [ ] Comprehensive testing of all levels

Priority: High
Estimated Effort: Large (3-5 days)

@coding-agent please implement this hierarchical structure
```

## 📊 SUMMARY
- **Total Issues**: 32
- **Completed**: 20 issues ✅ (Issues #1, #2, #3, #4, #5, #6, #7, #10, #12, #13, #14, #15, #16, #17, #18, #23, #24, #26, #30, #33)
- **Open/In Progress**: 12 issues 🔄
- **Completion Rate**: 63% (20/32 completed)

**Recently Completed:**
- ✅ Issue #30: [BUG] Gantt Chart Shows Archived Projects (2025-01-08)
- ✅ Issue #33: Hierarchical Project Structure (Project > Epic > Story > Issue) (2025-08-04)
- ✅ Issue #26: Project Archive System with Dashboard Integration (2025-08-02)

- ✅ Issue #24: Create Backlog Page with Advanced Filtering (2025-08-02)
- ✅ Issue #16: Advanced Mind Map Features (2025-08-02)
- ✅ Issue #15: Interactive Gantt Chart for Sprint and Project Management (2025-08-02)

### 🔵 **Issue #35:** [FEATURE] Enhanced Issue Creation/Editing: Select Epic, Story, and Backlog Placement - OPEN
```
Title: [FEATURE] Issue #35: Enhanced Issue Creation/Editing: Select Epic, Story, and Backlog Placement

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/35

Description:
Update the “Create Issue” and “Edit Issue” modals on the Issues List page to allow users to:
- Select a relevant Epic (from available epics in the project)
- Choose a Story within the chosen Epic (if the Epic contains Stories)
- Move or assign issues directly into the Product Backlog during creation/editing

What I want:
- Epic Selector: Dropdown list of all epics in the project
- Story Selector: After selecting an Epic, dynamically populate a dropdown with all child Stories; user may select one (optional if no stories)
- Backlog Checkbox/Option: Checkbox or dropdown to place this issue directly into the Backlog
- On editing an issue: Ability to change its Epic and Story assignment, move/remove the issue from the Backlog

Acceptance Criteria:
- Epic field shown and required if project has Epics
- Story field shown and enabled/required only when an Epic with child Stories is selected
- Issues are linked to the chosen Epic (and optionally Story) in the data model
- Issue is placed into the Backlog if user selects that option
- Editing an issue allows user to update Epic, Story, and Backlog placement
- UI updates are reflected immediately on the Issues List page
- Changes are persisted to backend (e.g., Firebase or DB)
- Validation prevents saving without required fields (e.g., Epic must be selected if available)
- Epic/Story selection in UI dynamically filters Stories once Epic is selected
- Issues can be removed from or moved into the Backlog via a clear UI control
- All standard issue fields (title, description, assignee, etc.) maintained
- Seamless user experience: minimizing required clicks, clear error feedback

Technical Notes / UI Guidance:
- Add Epic and Story dropdown fields (Story field disables/hides if no Epic or if Epic has no child stories).
- Backlog option could be a checkbox or a dropdown status.
- On the backend, maintain direct references (foreign keys or parent IDs) for Epic and Story.
- Whenever an issue is updated, ensure project-level hierarchy and integrity: issue-to-story-to-epic structure remains valid.
- Ensure support for bulk moves (drag-and-drop to Backlog, bulk-edit to change Epic/Story).

Related Features:
- Issue hierarchy: Epic > Story > Issue (recently implemented)
- Product Backlog (already available but needs more seamless assignments from Issues)

Stakeholders:
- @coding-agent
- Frontend/UI team
- Product/Project Owners

Priority & Labels:
- Priority: High
- Labels: enhancement, epic-story-link, backlog, ui/ux
```

**Open Issues on GitHub:**
- Issue #8: Card Labels/Tags System
- Issue #9: Time Tracking Features
- Issue #10: Team Collaboration Tools
- Issue #11: Mobile Responsive Design
- Issue #19: Enhanced Dark Mode Toggle with Better Contrast
- Issue #20: Add Colored Labels to Cards
- Issue #21: Time Tracking for Cards
- Issue #25: User Registration System with Admin Control
- Issue #27: Sprint Management System
- Issue #28: Enhanced Issues List Modal with Required Fields
- Issue #30: [BUG] Gantt Chart Shows Archived Projects
- Issue #31: [FEATURE] Enhanced Gantt Chart Date Navigation and Timeline View
- Issue #32: [FEATURE] Enhanced Product Backlog Item Creation with Required Fields
 
 Issue #35: [FEATURE] Enhanced Issue Creation/Editing: Select Epic, Story, and Backlog Placement


## 🎯 NEXT PRIORITIES
1. Issue #34: [FEATURE] Enhanced Sprint Management with Epic/Story/Issue Selection (HIGH PRIORITY)
2. Issue #32: [FEATURE] Enhanced Product Backlog Item Creation (HIGH PRIORITY)
3. Issue #31: [FEATURE] Enhanced Gantt Chart Date Navigation (HIGH PRIORITY)
4. Issue #28: [FEATURE] Enhanced Issues List Modal with Required Fields (HIGH PRIORITY)
5. Issue #9: Time Tracking Features
6. Issue #11: Mobile Responsive Design