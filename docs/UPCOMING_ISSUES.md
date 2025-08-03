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

**Note:** Issue #24 (Backlog Page) was implemented but remains OPEN on GitHub for additional enhancements.

## 🔄 OPEN ISSUES (IN PROGRESS/TODO)

### Issue #8: Card Labels/Tags System - OPEN
```
Title: [FEATURE] #8 Card Labels/Tags System

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/8

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

### Issue #9: Time Tracking Features - OPEN
```
Title: [FEATURE] Time Tracking Features

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/9

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

### Issue #10: Team Collaboration Tools - OPEN
```
Title: [FEATURE] Team Collaboration Tools

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/10

Description:
I want better team collaboration features like @mentions, notifications, and activity feeds.

What I want:
- @mention users in comments
- Activity feed showing recent changes
- Real-time notifications
- Team member assignments

Acceptance Criteria:
- [ ] @mention functionality in comments
- [ ] Activity feed on dashboard
- [ ] Browser notifications for mentions
- [ ] Team member dropdown for assignments
- [ ] Real-time updates using WebSocket

@coding-agent please implement this feature
```

### Issue #25: User Registration System with Admin Control - OPEN
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

### Issue #11: Mobile Responsive Design - OPEN
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

### Issue #19: Enhanced Dark Mode Toggle with Better Contrast - OPEN
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

### Issue #20: Add Colored Labels to Cards - OPEN
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

### Issue #21: Time Tracking for Cards - OPEN
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

### Issue #22: Enhanced Team Collaboration - OPEN
```
Title: [FEATURE] Enhanced Team Collaboration

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/22

Description:
I want better team collaboration features like @mentions, notifications, and activity feeds.

What I want:
- @mention users in comments
- Activity feed showing recent changes
- Real-time notifications
- Team member assignments

Acceptance Criteria:
- [ ] @mention functionality in comments
- [ ] Activity feed on dashboard
- [ ] Browser notifications for mentions
- [ ] Team member dropdown for assignments
- [ ] Real-time updates using WebSocket

@coding-agent please implement this feature
```

tion with project targeting
- [ ] Sprint planning board (backlog to sprint assignment)
- [ ] Sprint dashboard with progress metrics
- [ ] Burndown chart visualization
- [ ] Sprint capacity planning (story points/hours)
- [ ] Sprint retrospective templates
- [ ] Velocity tracking and forecasting
- [ ] Sprint calendar integration

Advanced Features:
- [ ] Sprint templates for recurring patterns
- [ ] Automated sprint rollover for incomplete items
- [ ] Sprint comparison and analytics
- [ ] Team workload distribution in sprints
- [ ] Sprint notifications and reminders
- [ ] Export sprint reports (PDF/Excel)
- [ ] Sprint milestone integration
- [ ] Custom sprint fields and metadata

Acceptance Criteria:
- [ ] Sprint list page showing all sprints with status
- [ ] Create sprint modal with project selection
- [ ] Sprint planning interface with issue assignment
- [ ] Sprint detail page with progress tracking
- [ ] Burndown chart with daily progress
- [ ] Sprint retrospective form and history
- [ ] Velocity calculation and trending
- [ ] Sprint reports and analytics dashboard

Technical Requirements:
- [ ] Sprint model with relationships to projects/issues
- [ ] Sprint planning drag-and-drop interface
- [ ] Chart.js integration for burndown visualization
- [ ] Sprint progress calculation algorithms
- [ ] Sprint notification system
- [ ] Sprint data export functionality

@coding-agent please implement this comprehensive sprint management feature
```



### Issue #28: Enhanced Issues List Modal with Required Fields - OPEN
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

## 📊 SUMMARY
- **Total Issues**: 28
- **Completed**: 17 issues ✅ (Issues #1, #2, #3, #4, #5, #6, #7, #12, #13, #14, #15, #16, #17, #18, #23, #24, #26)
- **Open/In Progress**: 11 issues 🔄
- **Completion Rate**: 61% (17/28 completed)

**Recently Completed:**
- ✅ Issue #26: Project Archive System with Dashboard Integration (2025-08-02)

- ✅ Issue #24: Create Backlog Page with Advanced Filtering (2025-08-02)
- ✅ Issue #16: Advanced Mind Map Features (2025-08-02)
- ✅ Issue #15: Interactive Gantt Chart for Sprint and Project Management (2025-08-02)

**Open Issues on GitHub:**
- Issue #8: Card Labels/Tags System
- Issue #9: Time Tracking Features
- Issue #10: Team Collaboration Tools
- Issue #11: Mobile Responsive Design
- Issue #19: Enhanced Dark Mode Toggle with Better Contrast
- Issue #20: Add Colored Labels to Cards
- Issue #21: Time Tracking for Cards
- Issue #22: Enhanced Team Collaboration
- Issue #25: User Registration System with Admin Control
- Issue #27: Sprint Management System
- Issue #28: Enhanced Issues List Modal with Required Fields

## 🎯 NEXT PRIORITIES
1. Issue #25: User Registration System with Admin Control
2. Issue #28: Enhanced Issues List Modal with Required Fields
3. Issue #27: Sprint Management System
4. Issue #9: Time Tracking Features
5. Issue #11: Mobile Responsive Design