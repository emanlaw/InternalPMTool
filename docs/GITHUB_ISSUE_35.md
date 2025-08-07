### 🔵 Issue #35: [FEATURE] Enhanced Issue Creation/Editing: Select Epic, Story, and Backlog Placement - OPEN

Title: [FEATURE] Enhanced Issue Creation/Editing: Select Epic, Story, and Backlog Placement

Status: OPEN
GitHub Issue: https://github.com/emanlaw/InternalPMTool/issues/35

Description:
Enhance the issue creation and editing interface to include Epic and Story selection capabilities, with options for automatic backlog placement and improved hierarchical organization.

What I want:
- Enhanced issue creation form with Epic/Story selection dropdowns
- Improved issue editing interface with hierarchical context
- Automatic backlog placement options during issue creation
- Better integration between issues, stories, and epics
- Streamlined workflow for issue organization

Current Issues:
- [ ] Issue creation form lacks Epic selection
- [ ] No Story association during issue creation
- [ ] Missing backlog placement options
- [ ] Issue editing doesn't show hierarchical context
- [ ] No clear Epic > Story > Issue relationship visualization

Desired Features:

**Enhanced Issue Creation:**
- [ ] Epic selection dropdown in issue creation form
- [ ] Story selection dropdown (filtered by selected Epic)
- [ ] "Add to Backlog" checkbox option
- [ ] Sprint assignment dropdown (optional)
- [ ] Hierarchical context display during creation
- [ ] Real-time story points impact calculation

**Improved Issue Editing:**
- [ ] Current Epic/Story context display
- [ ] Ability to reassign Epic/Story relationships
- [ ] Move between Epics/Stories functionality
- [ ] Backlog status toggle
- [ ] Sprint reassignment capabilities
- [ ] Issue dependency visualization

**Backlog Management:**
- [ ] Automatic backlog placement when "Add to Backlog" is checked
- [ ] Backlog prioritization during issue creation
- [ ] Visual indicators for backlog items
- [ ] Bulk backlog operations
- [ ] Backlog grooming interface

**Hierarchical Visualization:**
- [ ] Epic > Story > Issue breadcrumb navigation
- [ ] Parent/child relationship indicators
- [ ] Issue context in list views
- [ ] Hierarchical filtering options
- [ ] Cross-reference links between related items

Technical Requirements:
- [ ] Update issue creation modal with Epic/Story dropdowns
- [ ] Enhance issue editing interface with hierarchical context
- [ ] Implement backlog placement functionality
- [ ] Add Epic/Story filtering logic for dropdowns
- [ ] Create hierarchical relationship management
- [ ] Update issue list views with Epic/Story context
- [ ] Implement real-time story points calculation
- [ ] Add backlog status tracking
- [ ] Create issue dependency visualization
- [ ] Update API endpoints for hierarchical data

API Endpoints Needed:
- [ ] GET /api/projects/{id}/epics - Get available epics for selection
- [ ] GET /api/epics/{id}/stories - Get stories for selected epic
- [ ] POST /api/issues - Enhanced issue creation with Epic/Story
- [ ] PUT /api/issues/{id}/epic - Update issue Epic assignment
- [ ] PUT /api/issues/{id}/story - Update issue Story assignment
- [ ] PUT /api/issues/{id}/backlog - Toggle backlog status
- [ ] GET /api/issues/{id}/hierarchy - Get issue hierarchical context
- [ ] POST /api/backlog/prioritize - Prioritize backlog items

Acceptance Criteria:
- [ ] Issue creation form includes Epic and Story selection dropdowns
- [ ] Story dropdown filters based on selected Epic
- [ ] "Add to Backlog" option automatically places issues in backlog
- [ ] Issue editing shows current Epic/Story relationships
- [ ] Users can reassign Epic/Story relationships during editing
- [ ] Issue list views display Epic/Story context
- [ ] Backlog placement is properly tracked and visualized
- [ ] Hierarchical relationships are maintained in database
- [ ] Real-time story points calculation updates Epic/Story totals
- [ ] Cross-navigation between Epics, Stories, and Issues works seamlessly

Priority: HIGH
Estimated Effort: Medium (2-4 days)
Labels: enhancement, issue-tracking, ui/ux, high-priority, hierarchical-management

## Implementation Notes:
- Build upon existing colored labels feature (#38)
- Integrate with sprint management system (#34)
- Ensure compatibility with Kanban board functionality
- Maintain Firebase/local JSON compatibility
- Focus on user experience and intuitive workflows

@coding-agent please implement this enhanced issue creation/editing system with Epic/Story selection and backlog placement capabilities.
