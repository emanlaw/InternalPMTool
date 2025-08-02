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
    window.location.href = `/sprints/${sprintId}`;
}

function editSprint(sprintId) {
    // TODO: Implement edit sprint modal
    showNotification('Edit sprint functionality coming soon!', 'info');
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

// Add CSS animations
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
        margin: 5% auto;
        padding: 0;
        border-radius: 12px;
        width: 90%;
        max-width: 600px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: slideUp 0.3s ease;
    }
    
    .modal-content.large {
        max-width: 800px;
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
    
    .modal form {
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