// Sprint Management JavaScript

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
}

function createSprint(event) {
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
    
    fetch('/api/sprints', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(sprintData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Sprint created successfully!', 'success');
            closeModal('createSprintModal');
            location.reload();
        } else {
            showNotification('Error creating sprint: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error creating sprint', 'error');
    });
}

function viewSprint(sprintId) {
    // Fetch sprint items and show in a modal
    fetch(`/api/sprints/${sprintId}/items`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSprintViewModal(sprintId, data.items);
            } else {
                // Fallback to sprint detail page
                window.location.href = `/sprints/${sprintId}`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Fallback to sprint detail page
            window.location.href = `/sprints/${sprintId}`;
        });
}

function showSprintViewModal(sprintId, sprintItems) {
    const modalHTML = `
        <div id="viewSprintModal" class="modal">
            <div class="modal-content large">
                <div class="modal-header">
                    <h2>Sprint Overview</h2>
                    <span class="close" onclick="closeModal('viewSprintModal')">&times;</span>
                </div>
                <div class="sprint-view-content">
                    <div class="sprint-summary">
                        <div class="summary-stats">
                            <div class="stat-item">
                                <span class="stat-number">${sprintItems.epics.length}</span>
                                <span class="stat-label">Epics</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">${sprintItems.stories.length}</span>
                                <span class="stat-label">Stories</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">${sprintItems.cards.length}</span>
                                <span class="stat-label">Cards</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">${sprintItems.total_story_points}</span>
                                <span class="stat-label">Story Points</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="sprint-items-view">
                        <h3>Sprint Items</h3>
                        <div class="items-list">
                            ${renderSprintItemsView(sprintItems)}
                        </div>
                    </div>
                </div>
                <div class="modal-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('viewSprintModal')">Close</button>
                    <button type="button" class="btn btn-primary" onclick="closeModal('viewSprintModal'); window.location.href='/sprints/${sprintId}'">View Details</button>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('viewSprintModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to DOM
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    document.getElementById('viewSprintModal').style.display = 'block';
}

function renderSprintItemsView(sprintItems) {
    let html = '';
    
    // Render epics with their stories and cards
    sprintItems.epics.forEach(epic => {
        html += `
            <div class="epic-view-item">
                <div class="epic-header">
                    <span class="epic-icon">📚</span>
                    <span class="epic-title">${epic.title}</span>
                    <span class="epic-status status-${epic.status}">${epic.status}</span>
                </div>
                <div class="epic-stories">
                    ${epic.stories.map(story => `
                        <div class="story-view-item">
                            <div class="story-header">
                                <span class="story-icon">📖</span>
                                <span class="story-title">${story.title}</span>
                                <span class="story-points">${story.story_points || 0} pts</span>
                            </div>
                            <div class="story-cards">
                                ${story.cards.map(card => `
                                    <div class="card-view-item">
                                        <span class="card-icon">🎫</span>
                                        <span class="card-title">${card.title}</span>
                                        <span class="card-status status-${card.status}">${card.status}</span>
                                        ${card.assignee ? `<span class="card-assignee">@${card.assignee}</span>` : ''}
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });
    
    // Render standalone stories
    sprintItems.stories.forEach(story => {
        html += `
            <div class="story-view-item standalone">
                <div class="story-header">
                    <span class="story-icon">📖</span>
                    <span class="story-title">${story.title}</span>
                    <span class="story-points">${story.story_points || 0} pts</span>
                </div>
                <div class="story-cards">
                    ${story.cards.map(card => `
                        <div class="card-view-item">
                            <span class="card-icon">🎫</span>
                            <span class="card-title">${card.title}</span>
                            <span class="card-status status-${card.status}">${card.status}</span>
                            ${card.assignee ? `<span class="card-assignee">@${card.assignee}</span>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    });
    
    // Render standalone cards
    const standaloneCards = sprintItems.cards.filter(card => 
        !sprintItems.epics.some(epic => epic.stories.some(story => story.cards.some(c => c.id === card.id))) &&
        !sprintItems.stories.some(story => story.cards.some(c => c.id === card.id))
    );
    
    if (standaloneCards.length > 0) {
        html += `
            <div class="standalone-cards">
                <h4>Individual Cards</h4>
                ${standaloneCards.map(card => `
                    <div class="card-view-item">
                        <span class="card-icon">🎫</span>
                        <span class="card-title">${card.title}</span>
                        <span class="card-status status-${card.status}">${card.status}</span>
                        ${card.assignee ? `<span class="card-assignee">@${card.assignee}</span>` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    return html || '<p class="empty-sprint">No items assigned to this sprint yet.</p>';
}

function editSprint(sprintId) {
    // Fetch sprint data and show edit modal
    fetch(`/api/sprints/${sprintId}/items`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showEditSprintModal(sprintId, data.items);
            } else {
                showNotification('Error loading sprint data: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error loading sprint data', 'error');
        });
}

function showEditSprintModal(sprintId, sprintItems) {
    // Get sprint data from DOM or fetch it
    const sprintCard = document.querySelector(`[data-project-id] .sprint-card`);
    
    // Create edit modal HTML
    const modalHTML = `
        <div id="editSprintModal" class="modal">
            <div class="modal-content large">
                <div class="modal-header">
                    <h2>Edit Sprint</h2>
                    <span class="close" onclick="closeModal('editSprintModal')">&times;</span>
                </div>
                <div class="edit-sprint-content">
                    <div class="sprint-edit-sections">
                        <div class="sprint-basic-info">
                            <h3>Sprint Details</h3>
                            <div class="form-group">
                                <label for="editSprintName">Sprint Name</label>
                                <input type="text" id="editSprintName" placeholder="Sprint name">
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label for="editStartDate">Start Date</label>
                                    <input type="date" id="editStartDate">
                                </div>
                                <div class="form-group">
                                    <label for="editEndDate">End Date</label>
                                    <input type="date" id="editEndDate">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="editSprintGoal">Sprint Goal</label>
                                <textarea id="editSprintGoal" rows="3" placeholder="Sprint goal..."></textarea>
                            </div>
                        </div>
                        
                        <div class="sprint-planning-section">
                            <h3>Sprint Planning</h3>
                            <div class="planning-interface">
                                <div class="available-items">
                                    <h4>Available Items</h4>
                                    <div id="availableItemsTree" class="items-tree"></div>
                                </div>
                                <div class="selected-items">
                                    <h4>Sprint Items</h4>
                                    <div id="selectedItemsTree" class="items-tree"></div>
                                    <div class="sprint-stats">
                                        <div class="stat">
                                            <span class="stat-label">Total Story Points:</span>
                                            <span id="totalStoryPoints" class="stat-value">0</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal('editSprintModal')">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="saveSprintChanges(${sprintId})">Save Changes</button>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('editSprintModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to DOM
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    document.getElementById('editSprintModal').style.display = 'block';
    
    // Load project hierarchy and populate trees
    loadProjectHierarchy(sprintId);
}

function startSprint(sprintId) {
    if (confirm('Are you sure you want to start this sprint?')) {
        fetch(`/api/sprints/${sprintId}/start`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Sprint started successfully!', 'success');
                location.reload();
            } else {
                showNotification('Error starting sprint: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error starting sprint', 'error');
        });
    }
}

function completeSprint(sprintId) {
    if (confirm('Are you sure you want to complete this sprint?')) {
        fetch(`/api/sprints/${sprintId}/complete`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Sprint completed successfully!', 'success');
                location.reload();
            } else {
                showNotification('Error completing sprint: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error completing sprint', 'error');
        });
    }
}

function filterSprintsByProject() {
    const projectId = document.getElementById('projectFilter').value;
    const sprintCards = document.querySelectorAll('.sprint-card');
    
    sprintCards.forEach(card => {
        if (!projectId || card.dataset.projectId === projectId) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
    
    updateStats();
}

function updateStats() {
    const visibleCards = document.querySelectorAll('.sprint-card[style*="block"], .sprint-card:not([style])');
    const activeCards = Array.from(visibleCards).filter(card => card.dataset.status === 'active');
    const completedCards = Array.from(visibleCards).filter(card => card.dataset.status === 'completed');
    
    document.getElementById('totalSprints').textContent = visibleCards.length;
    document.getElementById('activeSprints').textContent = activeCards.length;
    document.getElementById('completedSprints').textContent = completedCards.length;
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

// Modal click outside to close
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

function loadProjectHierarchy(sprintId) {
    // Get project ID from sprint card or fetch sprint data
    const sprintCard = document.querySelector(`button[onclick="editSprint(${sprintId})"]`).closest('.sprint-card');
    const projectId = sprintCard ? sprintCard.dataset.projectId : 1;
    
    // Fetch project hierarchy
    fetch(`/api/projects/${projectId}/hierarchy`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateItemsTrees(data.hierarchy, sprintId);
            } else {
                showNotification('Error loading project hierarchy: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error loading project hierarchy', 'error');
        });
}

function populateItemsTrees(hierarchy, sprintId) {
    const availableTree = document.getElementById('availableItemsTree');
    const selectedTree = document.getElementById('selectedItemsTree');
    
    if (!availableTree || !selectedTree) return;
    
    availableTree.innerHTML = '';
    selectedTree.innerHTML = '';
    
    // Create hierarchical tree structure
    hierarchy.epics.forEach(epic => {
        const epicElement = createEpicElement(epic, sprintId);
        
        if (epic.sprint_id === sprintId) {
            selectedTree.appendChild(epicElement);
        } else {
            availableTree.appendChild(epicElement);
        }
    });
    
    // Update story points calculation
    updateStoryPointsDisplay();
}

function createEpicElement(epic, sprintId) {
    const epicDiv = document.createElement('div');
    epicDiv.className = 'tree-item epic-item';
    epicDiv.innerHTML = `
        <div class="tree-item-header">
            <input type="checkbox" class="item-checkbox" data-type="epic" data-id="${epic.id}" 
                   ${epic.sprint_id === sprintId ? 'checked' : ''} 
                   onchange="toggleItem(this)">
            <span class="tree-toggle" onclick="toggleTreeItem(this)">▼</span>
            <span class="item-title">📚 ${epic.title}</span>
        </div>
        <div class="tree-item-children">
            ${epic.stories.map(story => createStoryElement(story, sprintId)).join('')}
        </div>
    `;
    return epicDiv;
}

function createStoryElement(story, sprintId) {
    return `
        <div class="tree-item story-item">
            <div class="tree-item-header">
                <input type="checkbox" class="item-checkbox" data-type="story" data-id="${story.id}" 
                       ${story.sprint_id === sprintId ? 'checked' : ''} 
                       onchange="toggleItem(this)">
                <span class="tree-toggle" onclick="toggleTreeItem(this)">▼</span>
                <span class="item-title">📖 ${story.title}</span>
                <span class="story-points">${story.story_points || 0} pts</span>
            </div>
            <div class="tree-item-children">
                ${story.cards.map(card => createCardElement(card, sprintId)).join('')}
            </div>
        </div>
    `;
}

function createCardElement(card, sprintId) {
    return `
        <div class="tree-item card-item">
            <div class="tree-item-header">
                <input type="checkbox" class="item-checkbox" data-type="card" data-id="${card.id}" 
                       ${card.sprint_id === sprintId ? 'checked' : ''} 
                       onchange="toggleItem(this)">
                <span class="item-title">🎫 ${card.title}</span>
                <span class="card-points">${card.story_points || 0} pts</span>
                <span class="card-status status-${card.status}">${card.status}</span>
            </div>
        </div>
    `;
}

function toggleTreeItem(toggleElement) {
    const treeItem = toggleElement.closest('.tree-item');
    const children = treeItem.querySelector('.tree-item-children');
    
    if (children.style.display === 'none') {
        children.style.display = 'block';
        toggleElement.textContent = '▼';
    } else {
        children.style.display = 'none';
        toggleElement.textContent = '▶';
    }
}

function toggleItem(checkbox) {
    const itemType = checkbox.dataset.type;
    const itemId = parseInt(checkbox.dataset.id);
    const isChecked = checkbox.checked;
    
    // Update story points immediately
    updateStoryPointsDisplay();
    
    // For now, we'll rely on the checkbox state and let the user see the changes
    // The actual assignment will happen when they save
    // This is simpler and more reliable than complex DOM manipulation
}

function updateStoryPointsDisplay() {
    const totalElement = document.getElementById('totalStoryPoints');
    
    if (!totalElement) return;
    
    let total = 0;
    
    // Calculate from all checked items across both trees
    document.querySelectorAll('.item-checkbox:checked').forEach(checkbox => {
        const treeItem = checkbox.closest('.tree-item');
        const pointsElements = treeItem.querySelectorAll('.story-points, .card-points');
        
        // Get points from this specific item (not children)
        const directPointsElement = treeItem.querySelector('.tree-item-header .story-points, .tree-item-header .card-points');
        if (directPointsElement) {
            const points = parseInt(directPointsElement.textContent.replace(' pts', '')) || 0;
            total += points;
        }
    });
    
    totalElement.textContent = total;
}

function saveSprintChanges(sprintId) {
    // Collect selected items from all checked checkboxes
    const selectedItems = [];
    
    document.querySelectorAll('.item-checkbox:checked').forEach(checkbox => {
        selectedItems.push({
            type: checkbox.dataset.type,
            id: parseInt(checkbox.dataset.id)
        });
    });
    
    // Save basic sprint details and items
    const sprintData = {
        name: document.getElementById('editSprintName').value,
        start_date: document.getElementById('editStartDate').value,
        end_date: document.getElementById('editEndDate').value,
        goal: document.getElementById('editSprintGoal').value,
        items: selectedItems
    };
    
    // Update sprint via API
    fetch(`/api/sprints/${sprintId}/items`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ items: selectedItems })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Sprint updated successfully!', 'success');
            closeModal('editSprintModal');
            location.reload();
        } else {
            showNotification('Error updating sprint: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error updating sprint', 'error');
    });
}
// Add CSS animations and styles
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
        width: 90%;
        max-width: 600px;
        max-height: 90vh;
        overflow-y: auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: slideUp 0.3s ease;
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
    }
    
    .modal-header h2 {
        margin: 0;
        color: #2c3e50;
    }
    
    .close {
        color: #aaa;
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
        color: #000;
        background: #f0f0f0;
    }
    
    .modal form, .edit-sprint-content, .sprint-view-content {
        padding: 30px;
    }
    
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
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
    }
    
    /* Sprint View Modal Styles */
    .sprint-summary {
        margin-bottom: 30px;
    }
    
    .summary-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .stat-item {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 12px;
    }
    
    .stat-number {
        display: block;
        font-size: 2em;
        font-weight: bold;
        color: #2c3e50;
    }
    
    .stat-label {
        display: block;
        font-size: 0.9em;
        color: #6c757d;
        margin-top: 5px;
    }
    
    /* Items View Styles */
    .items-list {
        max-height: 400px;
        overflow-y: auto;
    }
    
    .epic-view-item, .story-view-item {
        margin-bottom: 20px;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
    }
    
    .epic-header, .story-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .epic-stories, .story-cards {
        margin-left: 20px;
    }
    
    .card-view-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        margin: 5px 0;
        background: #f8f9fa;
        border-radius: 6px;
        font-size: 0.9em;
    }
    
    .story-points, .card-status, .card-assignee {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: 500;
    }
    
    .story-points {
        background: #007bff;
        color: white;
    }
    
    .card-status.status-todo {
        background: #6c757d;
        color: white;
    }
    
    .card-status.status-in_progress {
        background: #ffc107;
        color: black;
    }
    
    .card-status.status-done {
        background: #28a745;
        color: white;
    }
    
    .card-assignee {
        background: #e9ecef;
        color: #495057;
    }
    
    /* Edit Modal Styles */
    .sprint-edit-sections {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 30px;
    }
    
    .planning-interface {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        height: 400px;
    }
    
    .available-items, .selected-items {
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
    }
    
    .available-items h4, .selected-items h4 {
        margin: 0 0 15px 0;
        color: #495057;
    }
    
    .items-tree {
        height: 300px;
        overflow-y: auto;
        border: 1px solid #f0f0f0;
        border-radius: 6px;
        padding: 10px;
    }
    
    .tree-item {
        margin: 5px 0;
    }
    
    .tree-item-header {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 5px;
        border-radius: 4px;
        cursor: pointer;
    }
    
    .tree-item-header:hover {
        background: #f8f9fa;
    }
    
    .tree-toggle {
        width: 16px;
        text-align: center;
        cursor: pointer;
        user-select: none;
    }
    
    .item-checkbox {
        margin: 0;
    }
    
    .item-title {
        flex: 1;
    }
    
    .tree-item-children {
        margin-left: 24px;
        border-left: 1px dashed #dee2e6;
        padding-left: 10px;
    }
    
    .story-item .tree-item-header {
        font-size: 0.9em;
    }
    
    .card-item .tree-item-header {
        font-size: 0.85em;
        color: #6c757d;
    }
    
    .sprint-stats {
        margin-top: 15px;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 6px;
    }
    
    .stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .stat-value {
        font-weight: bold;
        color: #007bff;
    }
    
    .empty-sprint {
        text-align: center;
        color: #6c757d;
        font-style: italic;
        padding: 40px;
    }
    
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