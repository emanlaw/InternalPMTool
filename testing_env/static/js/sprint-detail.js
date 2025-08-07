// Sprint Detail JavaScript

function initializeDragAndDrop() {
    const backlogList = document.getElementById('backlogList');
    const sprintList = document.getElementById('sprintList');
    
    if (backlogList) {
        new Sortable(backlogList, {
            group: 'shared',
            animation: 150,
            ghostClass: 'sortable-ghost',
            dragClass: 'sortable-drag',
            onEnd: function(evt) {
                handleIssueMove(evt);
            }
        });
    }
    
    if (sprintList) {
        new Sortable(sprintList, {
            group: 'shared',
            animation: 150,
            ghostClass: 'sortable-ghost',
            dragClass: 'sortable-drag',
            onEnd: function(evt) {
                handleIssueMove(evt);
            }
        });
    }
}

function handleIssueMove(evt) {
    const issueId = evt.item.dataset.issueId;
    const targetList = evt.to;
    const targetStatus = targetList.dataset.status;
    
    if (targetStatus === 'sprint') {
        // Add issue to sprint
        fetch(`/api/sprints/${sprintId}/issues`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ issue_id: parseInt(issueId) })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Issue added to sprint', 'success');
                updateIssueCounts();
            } else {
                showNotification('Error adding issue to sprint', 'error');
                // Revert the move
                evt.from.appendChild(evt.item);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error adding issue to sprint', 'error');
            evt.from.appendChild(evt.item);
        });
    } else if (targetStatus === 'backlog') {
        // Remove issue from sprint
        fetch(`/api/sprints/${sprintId}/issues/${issueId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Issue removed from sprint', 'success');
                updateIssueCounts();
            } else {
                showNotification('Error removing issue from sprint', 'error');
                evt.from.appendChild(evt.item);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error removing issue from sprint', 'error');
            evt.from.appendChild(evt.item);
        });
    }
}

function updateIssueCounts() {
    const backlogCount = document.querySelectorAll('#backlogList .issue-item').length;
    const sprintCount = document.querySelectorAll('#sprintList .issue-item').length;
    
    document.querySelector('#backlogList').parentElement.querySelector('.issue-count').textContent = backlogCount;
    document.querySelector('#sprintList').parentElement.querySelector('.issue-count').textContent = sprintCount;
}

function initializeBurndownChart() {
    const ctx = document.getElementById('burndownChart');
    if (!ctx) return;
    
    // Sample burndown data - in real implementation, this would come from the server
    const days = [];
    const idealBurndown = [];
    const actualBurndown = [];
    
    const startDate = new Date(sprintData.start_date);
    const endDate = new Date(sprintData.end_date);
    const totalDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
    const totalStoryPoints = sprintData.story_points || 50; // Default for demo
    
    for (let i = 0; i < totalDays; i++) {
        const currentDate = new Date(startDate);
        currentDate.setDate(startDate.getDate() + i);
        days.push(currentDate.toLocaleDateString());
        
        // Ideal burndown (linear)
        idealBurndown.push(totalStoryPoints - (totalStoryPoints / (totalDays - 1)) * i);
        
        // Actual burndown (sample data with some variation)
        if (i === 0) {
            actualBurndown.push(totalStoryPoints);
        } else {
            const remaining = Math.max(0, totalStoryPoints - (totalStoryPoints / totalDays) * i + Math.random() * 10 - 5);
            actualBurndown.push(Math.round(remaining));
        }
    }
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                label: 'Ideal Burndown',
                data: idealBurndown,
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false
            }, {
                label: 'Actual Burndown',
                data: actualBurndown,
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                borderWidth: 3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Story Points Remaining'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Sprint Days'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Sprint Burndown Chart'
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
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

function editSprint(sprintId) {
    showNotification('Edit sprint functionality coming soon!', 'info');
}

function exportSprintReport(sprintId) {
    window.open(`/api/sprints/${sprintId}/export`, '_blank');
}

function showRetrospectiveModal() {
    document.getElementById('retrospectiveModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function saveRetrospective() {
    const retrospectiveData = {
        went_well: document.getElementById('wentWell').value,
        improvements: document.getElementById('improvements').value,
        action_items: document.getElementById('actionItems').value
    };
    
    fetch(`/api/sprints/${sprintId}/retrospective`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(retrospectiveData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Retrospective saved successfully!', 'success');
            closeModal('retrospectiveModal');
        } else {
            showNotification('Error saving retrospective: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error saving retrospective', 'error');
    });
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

// Add drag and drop visual feedback
const style = document.createElement('style');
style.textContent = `
    .sortable-ghost {
        opacity: 0.4;
        background: #f8f9fa;
    }
    
    .sortable-drag {
        opacity: 0.8;
        transform: rotate(5deg);
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }
    
    .issue-list {
        min-height: 50px;
        border: 2px dashed transparent;
        border-radius: 8px;
        transition: border-color 0.3s ease;
    }
    
    .issue-list.sortable-over {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
    }
    
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
`;
document.head.appendChild(style);