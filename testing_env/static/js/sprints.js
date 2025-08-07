/**
 * Enhanced Sprint Management JavaScript
 * Handles sprint creation, editing, starting, and hierarchical item selection
 */

let currentSprintId = null;
let selectedEpics = [];
let selectedStories = [];
let selectedIssues = [];
let projectHierarchy = {};

// Modal Management
function showCreateSprintModal() {
    document.getElementById('createSprintModal').style.display = 'block';
    
    // Set default dates (start: today, end: 2 weeks from today)
    const today = new Date();
    const twoWeeksLater = new Date(today.getTime() + (14 * 24 * 60 * 60 * 1000));
    
    document.getElementById('startDate').value = today.toISOString().split('T')[0];
    document.getElementById('endDate').value = twoWeeksLater.toISOString().split('T')[0];
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    // Reset forms and selections when closing
    if (modalId === 'editSprintModal') {
        resetSprintPlanning();
    }
}

// Sprint Creation
async function createSprint(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const sprintData = {
        name: formData.get('name'),
        project_id: parseInt(formData.get('project_id')),
        start_date: formData.get('start_date'),
        end_date: formData.get('end_date'),
        goal: formData.get('goal') || '',
        story_points: parseInt(formData.get('story_points')) || 0
    };
    
    // Validate dates
    if (new Date(sprintData.start_date) >= new Date(sprintData.end_date)) {
        showNotification('End date must be after start date', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/sprints', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(sprintData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('Sprint created successfully!', 'success');
            closeModal('createSprintModal');
            location.reload(); // Refresh to show new sprint
        } else {
            showNotification('Error creating sprint: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error creating sprint: ' + error.message, 'error');
    }
}

// Sprint Viewing
async function viewSprint(sprintId) {
    try {
        const response = await fetch(`/api/sprints/${sprintId}/items`);
        const result = await response.json();
        
        if (result.success) {
            populateViewModal(result.sprint, result.epics, result.stories, result.issues);
            document.getElementById('viewSprintModal').style.display = 'block';
        } else {
            showNotification('Error loading sprint details: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error loading sprint details: ' + error.message, 'error');
    }
}

function populateViewModal(sprint, epics, stories, issues) {
    document.getElementById('viewSprintTitle').textContent = sprint.name;
    document.getElementById('viewSprintStatus').textContent = sprint.status.toUpperCase();
    document.getElementById('viewSprintStatus').className = `sprint-status status-${sprint.status}`;
    document.getElementById('viewSprintDuration').textContent = `${sprint.start_date} to ${sprint.end_date}`;
    document.getElementById('viewSprintGoal').textContent = sprint.goal || 'No goal set';
    document.getElementById('viewSprintPoints').textContent = sprint.story_points || 0;
    
    // Populate epics
    const epicsContainer = document.getElementById('epicsContainer');
    epicsContainer.innerHTML = '';
    if (epics.length === 0) {
        epicsContainer.innerHTML = '<div class="empty-item">No epics assigned</div>';
    } else {
        epics.forEach(epic => {
            const epicElement = createItemElement(epic, 'epic');
            epicsContainer.appendChild(epicElement);
        });
    }
    
    // Populate stories
    const storiesContainer = document.getElementById('storiesContainer');
    storiesContainer.innerHTML = '';
    if (stories.length === 0) {
        storiesContainer.innerHTML = '<div class="empty-item">No stories assigned</div>';
    } else {
        stories.forEach(story => {
            const storyElement = createItemElement(story, 'story');
            storiesContainer.appendChild(storyElement);
        });
    }
    
    // Populate issues
    const issuesContainer = document.getElementById('issuesContainer');
    issuesContainer.innerHTML = '';
    if (issues.length === 0) {
        issuesContainer.innerHTML = '<div class="empty-item">No issues assigned</div>';
    } else {
        issues.forEach(issue => {
            const issueElement = createItemElement(issue, 'issue');
            issuesContainer.appendChild(issueElement);
        });
    }
}

function createItemElement(item, type) {
    const div = document.createElement('div');
    div.className = `item-card ${type}-card`;
    
    const statusClass = item.status ? `status-${item.status}` : '';
    const points = item.story_points ? `(${item.story_points} pts)` : '';
    
    div.innerHTML = `
        <div class="item-header">
            <span class="item-title">${item.title}</span>
            <span class="item-status ${statusClass}">${item.status || 'N/A'}</span>
        </div>
        ${item.description ? `<div class="item-description">${item.description}</div>` : ''}
        ${points ? `<div class="item-points">${points}</div>` : ''}
    `;
    
    return div;
}

// Sprint Editing
async function editSprint(sprintId) {
    currentSprintId = sprintId;
    
    try {
        // Load sprint details
        const response = await fetch(`/api/sprints/${sprintId}/items`);
        const result = await response.json();
        
        if (result.success) {
            populateEditModal(result.sprint, result.epics, result.stories, result.issues);
            document.getElementById('editSprintModal').style.display = 'block';
        } else {
            showNotification('Error loading sprint for editing: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error loading sprint for editing: ' + error.message, 'error');
    }
}

function populateEditModal(sprint, epics, stories, issues) {
    // Populate form fields
    document.getElementById('editSprintName').value = sprint.name;
    document.getElementById('editSprintStatus').value = sprint.status.toUpperCase();
    document.getElementById('editStartDate').value = sprint.start_date;
    document.getElementById('editEndDate').value = sprint.end_date;
    document.getElementById('editSprintGoal').value = sprint.goal || '';
    document.getElementById('editStoryPoints').value = sprint.story_points || 0;
    
    // Set project in planning section
    document.getElementById('planningProject').value = sprint.project_id;
    
    // Initialize selected items
    selectedEpics = epics.map(e => e.id);
    selectedStories = stories.map(s => s.id);
    selectedIssues = issues.map(i => i.id);
    
    // Load project hierarchy
    loadProjectHierarchy();
    updateSelectedItemsDisplay();
}

// Project Hierarchy Loading
async function loadProjectHierarchy() {
    const projectId = document.getElementById('planningProject').value;
    
    if (!projectId) {
        document.getElementById('hierarchyTree').innerHTML = '<div class="empty-state">Select a project to see available items</div>';
        return;
    }
    
    try {
        const response = await fetch(`/api/projects/${projectId}/hierarchy`);
        const result = await response.json();
        
        if (result.success) {
            projectHierarchy = result;
            renderHierarchyTree(result);
        } else {
            showNotification('Error loading project hierarchy: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error loading project hierarchy: ' + error.message, 'error');
    }
}

function renderHierarchyTree(hierarchy) {
    const container = document.getElementById('hierarchyTree');
    container.innerHTML = '';
    
    if (hierarchy.epics.length === 0 && hierarchy.orphaned_stories.length === 0 && hierarchy.orphaned_issues.length === 0) {
        container.innerHTML = '<div class="empty-state">No items found in this project</div>';
        return;
    }
    
    // Render epics with their stories and issues
    hierarchy.epics.forEach(epic => {
        const epicElement = createHierarchyItem(epic, 'epic');
        container.appendChild(epicElement);
        
        // Render stories under epic
        if (epic.stories && epic.stories.length > 0) {
            const storiesContainer = document.createElement('div');
            storiesContainer.className = 'stories-container';
            
            epic.stories.forEach(story => {
                const storyElement = createHierarchyItem(story, 'story');
                storiesContainer.appendChild(storyElement);
                
                // Render issues under story
                if (story.issues && story.issues.length > 0) {
                    const issuesContainer = document.createElement('div');
                    issuesContainer.className = 'issues-container';
                    
                    story.issues.forEach(issue => {
                        const issueElement = createHierarchyItem(issue, 'issue');
                        issuesContainer.appendChild(issueElement);
                    });
                    
                    storyElement.appendChild(issuesContainer);
                }
            });
            
            epicElement.appendChild(storiesContainer);
        }
    });
    
    // Render orphaned stories
    if (hierarchy.orphaned_stories.length > 0) {
        const orphanedHeader = document.createElement('div');
        orphanedHeader.className = 'orphaned-header';
        orphanedHeader.innerHTML = '<h5>📖 Stories (not in epics)</h5>';
        container.appendChild(orphanedHeader);
        
        hierarchy.orphaned_stories.forEach(story => {
            const storyElement = createHierarchyItem(story, 'story');
            container.appendChild(storyElement);
        });
    }
    
    // Render orphaned issues
    if (hierarchy.orphaned_issues.length > 0) {
        const orphanedHeader = document.createElement('div');
        orphanedHeader.className = 'orphaned-header';
        orphanedHeader.innerHTML = '<h5>🎯 Issues (not in stories)</h5>';
        container.appendChild(orphanedHeader);
        
        hierarchy.orphaned_issues.forEach(issue => {
            const issueElement = createHierarchyItem(issue, 'issue');
            container.appendChild(issueElement);
        });
    }
}

function createHierarchyItem(item, type) {
    const div = document.createElement('div');
    div.className = `hierarchy-item ${type}-item`;
    div.dataset.itemId = item.id;
    div.dataset.itemType = type;
    
    const isSelected = (type === 'epic' && selectedEpics.includes(item.id)) ||
                      (type === 'story' && selectedStories.includes(item.id)) ||
                      (type === 'issue' && selectedIssues.includes(item.id));
    
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = isSelected;
    checkbox.onchange = () => toggleItemSelection(item.id, type);
    
    const icon = type === 'epic' ? '📚' : type === 'story' ? '📖' : '🎯';
    const points = item.story_points ? ` (${item.story_points} pts)` : '';
    
    div.innerHTML = `
        <div class="item-content">
            <span class="item-icon">${icon}</span>
            <span class="item-title">${item.title}${points}</span>
            <span class="item-status status-${item.status || 'todo'}">${item.status || 'todo'}</span>
        </div>
    `;
    
    div.insertBefore(checkbox, div.firstChild);
    
    return div;
}

function toggleItemSelection(itemId, type) {
    if (type === 'epic') {
        const index = selectedEpics.indexOf(itemId);
        if (index > -1) {
            selectedEpics.splice(index, 1);
        } else {
            selectedEpics.push(itemId);
        }
    } else if (type === 'story') {
        const index = selectedStories.indexOf(itemId);
        if (index > -1) {
            selectedStories.splice(index, 1);
        } else {
            selectedStories.push(itemId);
        }
    } else if (type === 'issue') {
        const index = selectedIssues.indexOf(itemId);
        if (index > -1) {
            selectedIssues.splice(index, 1);
        } else {
            selectedIssues.push(itemId);
        }
    }
    
    updateSelectedItemsDisplay();
    updateCapacityIndicator();
}

function updateSelectedItemsDisplay() {
    // Update counts
    document.getElementById('selectedEpicsCount').textContent = selectedEpics.length;
    document.getElementById('selectedStoriesCount').textContent = selectedStories.length;
    document.getElementById('selectedIssuesCount').textContent = selectedIssues.length;
    
    // Update containers
    updateSelectedContainer('selectedEpicsContainer', selectedEpics, 'epic');
    updateSelectedContainer('selectedStoriesContainer', selectedStories, 'story');
    updateSelectedContainer('selectedIssuesContainer', selectedIssues, 'issue');
}

function updateSelectedContainer(containerId, selectedIds, type) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    if (selectedIds.length === 0) {
        container.innerHTML = `<div class="empty-selection">No ${type}s selected</div>`;
        return;
    }
    
    selectedIds.forEach(id => {
        const item = findItemById(id, type);
        if (item) {
            const element = createSelectedItemElement(item, type);
            container.appendChild(element);
        }
    });
}

function findItemById(id, type) {
    if (!projectHierarchy) return null;
    
    if (type === 'epic') {
        return projectHierarchy.epics.find(e => e.id === id);
    } else if (type === 'story') {
        // Search in epic stories and orphaned stories
        for (const epic of projectHierarchy.epics) {
            const story = epic.stories?.find(s => s.id === id);
            if (story) return story;
        }
        return projectHierarchy.orphaned_stories?.find(s => s.id === id);
    } else if (type === 'issue') {
        // Search in story issues and orphaned issues
        for (const epic of projectHierarchy.epics) {
            for (const story of epic.stories || []) {
                const issue = story.issues?.find(i => i.id === id);
                if (issue) return issue;
            }
        }
        return projectHierarchy.orphaned_issues?.find(i => i.id === id);
    }
    
    return null;
}

function createSelectedItemElement(item, type) {
    const div = document.createElement('div');
    div.className = `selected-item ${type}-selected`;
    
    const icon = type === 'epic' ? '📚' : type === 'story' ? '📖' : '🎯';
    const points = item.story_points ? ` (${item.story_points} pts)` : '';
    
    div.innerHTML = `
        <span class="selected-icon">${icon}</span>
        <span class="selected-title">${item.title}${points}</span>
        <button class="remove-btn" onclick="removeSelectedItem(${item.id}, '${type}')" title="Remove from sprint">×</button>
    `;
    
    return div;
}

function removeSelectedItem(itemId, type) {
    toggleItemSelection(itemId, type);
    // Also update the checkbox in hierarchy
    const hierarchyItem = document.querySelector(`[data-item-id="${itemId}"][data-item-type="${type}"] input[type="checkbox"]`);
    if (hierarchyItem) {
        hierarchyItem.checked = false;
    }
}

function updateCapacityIndicator() {
    let totalPoints = 0;
    
    // Calculate total story points from selected items
    selectedEpics.forEach(id => {
        const epic = findItemById(id, 'epic');
        if (epic && epic.story_points) {
            totalPoints += epic.story_points;
        }
    });
    
    selectedStories.forEach(id => {
        const story = findItemById(id, 'story');
        if (story && story.story_points) {
            totalPoints += story.story_points;
        }
    });
    
    selectedIssues.forEach(id => {
        const issue = findItemById(id, 'issue');
        if (issue && issue.story_points) {
            totalPoints += issue.story_points;
        }
    });
    
    const capacity = parseInt(document.getElementById('editStoryPoints').value) || 0;
    
    document.getElementById('totalStoryPoints').textContent = totalPoints;
    document.getElementById('sprintCapacity').textContent = capacity;
    
    // Update progress bar
    const percentage = capacity > 0 ? Math.min((totalPoints / capacity) * 100, 100) : 0;
    document.getElementById('capacityProgress').style.width = percentage + '%';
    
    // Show warning if over capacity
    const warning = document.getElementById('capacityWarning');
    if (totalPoints > capacity && capacity > 0) {
        warning.style.display = 'block';
        document.getElementById('capacityProgress').style.backgroundColor = '#ff6b6b';
    } else {
        warning.style.display = 'none';
        document.getElementById('capacityProgress').style.backgroundColor = '#51cf66';
    }
}

// Sprint Starting
async function startSprint(sprintId) {
    currentSprintId = sprintId;
    
    try {
        // Load sprint details for confirmation
        const response = await fetch(`/api/sprints/${sprintId}/items`);
        const result = await response.json();
        
        if (result.success) {
            populateStartConfirmation(result.sprint, result.epics, result.stories, result.issues);
            document.getElementById('startSprintModal').style.display = 'block';
        } else {
            showNotification('Error loading sprint details: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error loading sprint details: ' + error.message, 'error');
    }
}

function populateStartConfirmation(sprint, epics, stories, issues) {
    document.getElementById('confirmSprintName').textContent = sprint.name;
    document.getElementById('confirmSprintDuration').textContent = `${sprint.start_date} to ${sprint.end_date}`;
    
    const totalItems = epics.length + stories.length + issues.length;
    document.getElementById('confirmSprintItems').textContent = `${totalItems} items (${epics.length} epics, ${stories.length} stories, ${issues.length} issues)`;
}

async function confirmStartSprint() {
    if (!currentSprintId) return;
    
    try {
        const response = await fetch(`/api/sprints/${currentSprintId}/start`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('Sprint started successfully!', 'success');
            closeModal('startSprintModal');
            location.reload(); // Refresh to show updated status
        } else {
            showNotification('Error starting sprint: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error starting sprint: ' + error.message, 'error');
    }
}

// Sprint Completion
async function completeSprint(sprintId) {
    if (!confirm('Are you sure you want to complete this sprint? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/sprints/${sprintId}/complete`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('Sprint completed successfully!', 'success');
            location.reload(); // Refresh to show updated status
        } else {
            showNotification('Error completing sprint: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Error completing sprint: ' + error.message, 'error');
    }
}

// Save Sprint Changes
async function saveSprintChanges() {
    if (!currentSprintId) return;
    
    // Get form data
    const sprintData = {
        name: document.getElementById('editSprintName').value,
        goal: document.getElementById('editSprintGoal').value,
        story_points: parseInt(document.getElementById('editStoryPoints').value) || 0,
        start_date: document.getElementById('editStartDate').value,
        end_date: document.getElementById('editEndDate').value
    };
    
    try {
        // Update sprint details
        const updateResponse = await fetch(`/api/sprints/${currentSprintId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(sprintData)
        });
        
        const updateResult = await updateResponse.json();
        
        if (!updateResult.success) {
            throw new Error(updateResult.error);
        }
        
        // Update sprint items
        const itemsData = {
            epic_ids: selectedEpics,
            story_ids: selectedStories,
            issue_ids: selectedIssues
        };
        
        const itemsResponse = await fetch(`/api/sprints/${currentSprintId}/items`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(itemsData)
        });
        
        const itemsResult = await itemsResponse.json();
        
        if (itemsResult.success) {
            showNotification('Sprint updated successfully!', 'success');
            closeModal('editSprintModal');
            location.reload(); // Refresh to show changes
        } else {
            showNotification('Error updating sprint items: ' + itemsResult.error, 'error');
        }
    } catch (error) {
        showNotification('Error saving sprint changes: ' + error.message, 'error');
    }
}

// Utility Functions
function resetSprintPlanning() {
    currentSprintId = null;
    selectedEpics = [];
    selectedStories = [];
    selectedIssues = [];
    projectHierarchy = {};
    
    document.getElementById('planningProject').value = '';
    document.getElementById('hierarchyTree').innerHTML = '';
    updateSelectedItemsDisplay();
    updateCapacityIndicator();
}

function filterSprintsByProject() {
    const projectId = document.getElementById('projectFilter').value;
    const sprintCards = document.querySelectorAll('.sprint-card');
    
    sprintCards.forEach(card => {
        const cardProjectId = card.dataset.projectId;
        
        if (!projectId || cardProjectId === projectId) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
    
    updateSprintStats();
}

function updateSprintStats() {
    const visibleSprints = document.querySelectorAll('.sprint-card[style*="block"], .sprint-card:not([style])');
    const activeSprints = Array.from(visibleSprints).filter(card => card.dataset.status === 'active');
    const completedSprints = Array.from(visibleSprints).filter(card => card.dataset.status === 'completed');
    
    document.getElementById('totalSprints').textContent = visibleSprints.length;
    document.getElementById('activeSprints').textContent = activeSprints.length;
    document.getElementById('completedSprints').textContent = completedSprints.length;
}

function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelectorAll('.notification');
    existing.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">${getNotificationIcon(type)}</span>
            <span class="notification-text">${message}</span>
        </div>
    `;
    
    const colors = {
        success: 'linear-gradient(135deg, #28a745, #20c997)',
        error: 'linear-gradient(135deg, #dc3545, #fd7e14)',
        info: 'linear-gradient(135deg, #007bff, #6f42c1)',
        warning: 'linear-gradient(135deg, #ffc107, #fd7e14)'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 0;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        background: ${colors[type] || colors.info};
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        animation: slideInRight 0.4s ease;
        min-width: 300px;
        max-width: 400px;
    `;
    
    const content = notification.querySelector('.notification-content');
    content.style.cssText = `
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 20px;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, type === 'error' ? 5000 : 3000);
}

function getNotificationIcon(type) {
    const icons = {
        success: '✓',
        error: '⚠️',
        info: 'ℹ️',
        warning: '⚠️'
    };
    return icons[type] || icons.info;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Update capacity indicator when story points change
    const storyPointsInput = document.getElementById('editStoryPoints');
    if (storyPointsInput) {
        storyPointsInput.addEventListener('input', updateCapacityIndicator);
    }
    
    // Close modals when clicking outside
    window.onclick = function(event) {
        const modals = ['createSprintModal', 'viewSprintModal', 'editSprintModal', 'startSprintModal'];
        modals.forEach(modalId => {
            const modal = document.getElementById(modalId);
            if (event.target === modal) {
                closeModal(modalId);
            }
        });
    };
});

// Add enhanced CSS styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { 
            transform: translateX(100%) scale(0.8); 
            opacity: 0; 
        }
        to { 
            transform: translateX(0) scale(1); 
            opacity: 1; 
        }
    }
    
    @keyframes slideOutRight {
        from { 
            transform: translateX(0) scale(1); 
            opacity: 1; 
        }
        to { 
            transform: translateX(100%) scale(0.8); 
            opacity: 0; 
        }
    }
    
    .modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
        animation: fadeIn 0.3s ease;
    }
    
    .modal-content {
        background-color: white;
        margin: 2% auto;
        padding: 0;
        border-radius: 12px;
        width: 95%;
        max-width: 800px;
        max-height: 90vh;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: slideUp 0.3s ease;
        overflow: hidden;
    }
    
    .modal-content.large {
        max-width: 1000px;
    }
    
    .modal-header {
        padding: 25px 30px 20px;
        border-bottom: 2px solid #f0f0f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .modal-header h2 {
        margin: 0;
        color: white;
    }
    
    .modal-body {
        max-height: 70vh;
        overflow-y: auto;
        padding: 20px 30px;
    }
    
    .close {
        color: rgba(255,255,255,0.8);
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        transition: all 0.2s ease;
    }
    
    .close:hover {
        color: white;
        background: rgba(255,255,255,0.2);
    }
    
    .modal form {
        padding: 0;
    }
    
    .form-section {
        margin-bottom: 30px;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    
    .form-section h4 {
        margin: 0 0 15px 0;
        color: #495057;
        font-weight: 600;
    }
    
    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-group label {
        display: block;
        margin-bottom: 8px;
        font-weight: 600;
        color: #495057;
    }
    
    .form-group input,
    .form-group select,
    .form-group textarea {
        width: 100%;
        padding: 12px;
        border: 2px solid #dee2e6;
        border-radius: 8px;
        font-size: 14px;
        transition: border-color 0.3s ease;
        box-sizing: border-box;
    }
    
    .form-group input:focus,
    .form-group select:focus,
    .form-group textarea:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .modal-actions {
        display: flex;
        gap: 15px;
        justify-content: flex-end;
        padding: 20px 30px 30px;
        border-top: 2px solid #f0f0f0;
        background: #f8f9fa;
    }
    
    .hierarchy-tree {
        max-height: 400px;
        overflow-y: auto;
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 10px;
        background: white;
    }
    
    .hierarchy-item {
        display: flex;
        align-items: center;
        padding: 8px;
        margin: 4px 0;
        border-radius: 6px;
        border: 1px solid #e9ecef;
        background: #fff;
        transition: all 0.2s ease;
    }
    
    .hierarchy-item:hover {
        background: #f8f9fa;
        border-color: #667eea;
    }
    
    .hierarchy-item input[type="checkbox"] {
        margin-right: 10px;
        width: auto;
    }
    
    .item-content {
        display: flex;
        align-items: center;
        gap: 8px;
        flex: 1;
    }
    
    .item-icon {
        font-size: 16px;
    }
    
    .item-title {
        flex: 1;
        font-weight: 500;
    }
    
    .item-status {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-todo { background: #ffc107; color: #212529; }
    .status-in-progress { background: #007bff; color: white; }
    .status-done { background: #28a745; color: white; }
    .status-planning { background: #6c757d; color: white; }
    .status-active { background: #17a2b8; color: white; }
    .status-completed { background: #28a745; color: white; }
    
    .stories-container,
    .issues-container {
        margin-left: 30px;
        border-left: 2px solid #dee2e6;
        padding-left: 10px;
    }
    
    .orphaned-header {
        margin: 20px 0 10px 0;
        padding: 10px 0;
        border-bottom: 1px solid #dee2e6;
    }
    
    .orphaned-header h5 {
        margin: 0;
        color: #6c757d;
        font-weight: 600;
    }
    
    .selected-items-summary {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .selected-count {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        margin-right: 15px;
        padding: 4px 8px;
        background: #667eea;
        color: white;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .selected-items-container {
        max-height: 200px;
        overflow-y: auto;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 10px;
        background: white;
    }
    
    .selected-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px;
        margin: 4px 0;
        background: #f8f9fa;
        border-radius: 6px;
        border: 1px solid #dee2e6;
    }
    
    .selected-icon {
        font-size: 14px;
    }
    
    .selected-title {
        flex: 1;
        font-size: 13px;
    }
    
    .remove-btn {
        background: #dc3545;
        color: white;
        border: none;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        cursor: pointer;
        line-height: 1;
    }
    
    .remove-btn:hover {
        background: #c82333;
    }
    
    .capacity-indicator {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .capacity-bar {
        width: 100%;
        height: 20px;
        background: #dee2e6;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .capacity-progress {
        height: 100%;
        background: #51cf66;
        transition: all 0.3s ease;
        border-radius: 10px;
    }
    
    .capacity-warning {
        display: none;
        color: #dc3545;
        font-weight: 600;
        margin-top: 10px;
    }
    
    .empty-state,
    .empty-selection,
    .empty-item {
        text-align: center;
        padding: 20px;
        color: #6c757d;
        font-style: italic;
    }
    
    .item-card {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background: white;
    }
    
    .item-header {
        display: flex;
        justify-content: between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .item-description {
        color: #6c757d;
        font-size: 14px;
        margin-bottom: 8px;
    }
    
    .item-points {
        color: #495057;
        font-weight: 600;
        font-size: 12px;
    }
    
    .epic-card { border-left: 4px solid #6f42c1; }
    .story-card { border-left: 4px solid #007bff; }
    .issue-card { border-left: 4px solid #28a745; }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
`;
document.head.appendChild(style);