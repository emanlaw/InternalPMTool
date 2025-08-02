// Advanced Mind Map Functionality
class AdvancedMindMap extends MindMap {
    constructor(canvasId) {
        super(canvasId);
        this.history = [];
        this.historyIndex = -1;
        this.clipboard = null;
        this.searchResults = [];
        this.setupAdvancedFeatures();
    }
    
    setupAdvancedFeatures() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        
        // Auto-save functionality
        setInterval(() => this.autoSave(), 30000); // Auto-save every 30 seconds
        
        // Add legend
        this.addLegend();
        
        // Welcome message
        setTimeout(() => {
            this.showNotification('Mind map ready! Double-click to create nodes 🎉', 'info');
        }, 500);
        
        // Update legend when nodes change
        this.originalDraw = this.draw;
        this.draw = () => {
            this.originalDraw();
            this.updateLegend();
        };
    }
    
    updateLegend() {
        const legend = document.querySelector('.node-type-legend');
        if (legend) {
            legend.remove();
            this.addLegend();
        }
    }
    
    handleKeyboard(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'z':
                    e.preventDefault();
                    this.undo();
                    break;
                case 'y':
                    e.preventDefault();
                    this.redo();
                    break;
                case 'c':
                    e.preventDefault();
                    this.copy();
                    break;
                case 'v':
                    e.preventDefault();
                    this.paste();
                    break;
                case 's':
                    e.preventDefault();
                    this.save();
                    break;
                case 'f':
                    e.preventDefault();
                    this.showSearchDialog();
                    break;
            }
        }
        
        if (e.key === 'Delete' && this.selectedNode) {
            this.deleteNode(this.selectedNode);
        }
    }
    
    saveState() {
        const state = {
            nodes: JSON.parse(JSON.stringify(this.nodes)),
            connections: JSON.parse(JSON.stringify(this.connections))
        };
        
        // Remove future history if we're not at the end
        this.history = this.history.slice(0, this.historyIndex + 1);
        this.history.push(state);
        this.historyIndex++;
        
        // Limit history size
        if (this.history.length > 50) {
            this.history.shift();
            this.historyIndex--;
        }
    }
    
    undo() {
        if (this.historyIndex > 0) {
            this.historyIndex--;
            const state = this.history[this.historyIndex];
            this.nodes = JSON.parse(JSON.stringify(state.nodes));
            this.connections = JSON.parse(JSON.stringify(state.connections));
            this.draw();
        }
    }
    
    redo() {
        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            const state = this.history[this.historyIndex];
            this.nodes = JSON.parse(JSON.stringify(state.nodes));
            this.connections = JSON.parse(JSON.stringify(state.connections));
            this.draw();
        }
    }
    
    copy() {
        if (this.selectedNode) {
            this.clipboard = JSON.parse(JSON.stringify(this.selectedNode));
        }
    }
    
    paste() {
        if (this.clipboard) {
            const newNode = JSON.parse(JSON.stringify(this.clipboard));
            newNode.id = this.nodeIdCounter++;
            newNode.x += 50;
            newNode.y += 50;
            this.nodes.push(newNode);
            this.selectedNode = newNode;
            this.saveState();
            this.draw();
        }
    }
    
    createNodeAt(x, y) {
        this.saveState();
        super.createNodeAt(x, y);
    }
    
    deleteNode(node) {
        this.saveState();
        super.deleteNode(node);
    }
    
    editNode(node) {
        this.saveState();
        super.editNode(node);
    }
    
    autoSave() {
        const projectId = document.getElementById('projectSelect').value;
        if (projectId && this.nodes.length > 0) {
            // Show subtle auto-save indicator
            let indicator = document.querySelector('.auto-save-indicator');
            if (!indicator) {
                indicator = document.createElement('div');
                indicator.className = 'auto-save-indicator';
                indicator.style.cssText = `
                    position: fixed;
                    bottom: 20px;
                    left: 20px;
                    background: rgba(40, 167, 69, 0.9);
                    color: white;
                    padding: 8px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: 500;
                    z-index: 100;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                `;
                indicator.innerHTML = '💾 Auto-saving...';
                document.body.appendChild(indicator);
            }
            
            indicator.style.opacity = '1';
            
            this.save(true); // Silent save
            
            setTimeout(() => {
                indicator.style.opacity = '0';
            }, 2000);
        }
    }
    
    save(silent = false) {
        const projectId = document.getElementById('projectSelect').value;
        if (!projectId) {
            if (!silent) this.showNotification('Please select a project first', 'error');
            return;
        }
        
        if (!silent) this.showNotification('Saving mind map...', 'info');
        
        const data = {
            project_id: parseInt(projectId),
            nodes: this.nodes,
            connections: this.connections
        };
        
        fetch('/api/save_mindmap', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                if (!silent) {
                    this.showNotification('Mind map saved successfully! ✓', 'success');
                }
            } else {
                this.showNotification('Error saving: ' + result.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.showNotification('Network error while saving', 'error');
        });
    }
    
    showNotification(message, type = 'info') {
        // Remove existing notifications
        const existing = document.querySelectorAll('.mindmap-notification');
        existing.forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = `mindmap-notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${this.getNotificationIcon(type)}</span>
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
            backdrop-filter: blur(10px);
            animation: slideInRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
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
        
        const icon = notification.querySelector('.notification-icon');
        icon.style.cssText = `
            font-size: 20px;
            flex-shrink: 0;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, type === 'error' ? 5000 : 3000);
    }
    
    getNotificationIcon(type) {
        const icons = {
            success: '✓',
            error: '⚠️',
            info: 'ℹ️',
            warning: '⚠️'
        };
        return icons[type] || icons.info;
    }
    
    showSearchDialog() {
        const dialog = document.createElement('div');
        dialog.className = 'search-dialog';
        dialog.innerHTML = `
            <div class="search-dialog-content">
                <h3>Search Nodes</h3>
                <input type="text" id="searchInput" placeholder="Enter search term..." />
                <div class="search-results" id="searchResults"></div>
                <div class="search-actions">
                    <button onclick="this.parentElement.parentElement.parentElement.remove()">Close</button>
                </div>
            </div>
        `;
        
        dialog.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        `;
        
        const content = dialog.querySelector('.search-dialog-content');
        content.style.cssText = `
            background: white;
            padding: 20px;
            border-radius: 8px;
            width: 400px;
            max-width: 90vw;
        `;
        
        document.body.appendChild(dialog);
        
        const searchInput = dialog.querySelector('#searchInput');
        const searchResults = dialog.querySelector('#searchResults');
        
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const results = this.nodes.filter(node => 
                node.text.toLowerCase().includes(term)
            );
            
            searchResults.innerHTML = '';
            results.forEach(node => {
                const item = document.createElement('div');
                item.textContent = node.text;
                item.style.cssText = `
                    padding: 8px;
                    cursor: pointer;
                    border-bottom: 1px solid #eee;
                `;
                item.addEventListener('click', () => {
                    this.selectedNode = node;
                    this.panToNode(node);
                    this.draw();
                    dialog.remove();
                });
                searchResults.appendChild(item);
            });
        });
        
        searchInput.focus();
    }
    
    panToNode(node) {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        this.panX = centerX - node.x * this.zoom;
        this.panY = centerY - node.y * this.zoom;
    }
    
    addLegend() {
        const legend = document.createElement('div');
        legend.className = 'node-type-legend';
        legend.innerHTML = `
            <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #495057;">Node Types</h4>
            <div class="legend-item">
                <div class="legend-color todo"></div>
                <span>TODO</span>
                <small style="color: #6c757d;">(${this.nodes.filter(n => n.type === 'todo').length})</small>
            </div>
            <div class="legend-item">
                <div class="legend-color in_progress"></div>
                <span>In Progress</span>
                <small style="color: #6c757d;">(${this.nodes.filter(n => n.type === 'in_progress').length})</small>
            </div>
            <div class="legend-item">
                <div class="legend-color done"></div>
                <span>Done</span>
                <small style="color: #6c757d;">(${this.nodes.filter(n => n.type === 'done').length})</small>
            </div>
            <div class="legend-item">
                <div class="legend-color idea"></div>
                <span>Idea</span>
                <small style="color: #6c757d;">(${this.nodes.filter(n => n.type === 'idea').length})</small>
            </div>
            <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #dee2e6; font-size: 12px; color: #6c757d;">
                Total: ${this.nodes.length} nodes
            </div>
        `;
        
        this.canvas.parentElement.appendChild(legend);
    }
    
    exportToJSON() {
        const data = {
            nodes: this.nodes,
            connections: this.connections,
            metadata: {
                created: new Date().toISOString(),
                nodeCount: this.nodes.length,
                connectionCount: this.connections.length
            }
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'mindmap.json';
        link.click();
        URL.revokeObjectURL(url);
    }
    
    importFromJSON() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        
        input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const data = JSON.parse(e.target.result);
                        if (data.nodes && data.connections) {
                            this.saveState();
                            this.nodes = data.nodes;
                            this.connections = data.connections;
                            this.nodeIdCounter = Math.max(...this.nodes.map(n => n.id), 0) + 1;
                            this.draw();
                            this.showNotification('Mind map imported successfully!', 'success');
                        } else {
                            this.showNotification('Invalid mind map file format', 'error');
                        }
                    } catch (error) {
                        this.showNotification('Error reading file: ' + error.message, 'error');
                    }
                };
                reader.readAsText(file);
            }
        });
        
        input.click();
    }
    
    generateSummary() {
        const summary = {
            totalNodes: this.nodes.length,
            nodesByType: {},
            totalConnections: this.connections.length,
            isolatedNodes: [],
            completionRate: 0
        };
        
        // Count nodes by type
        this.nodes.forEach(node => {
            summary.nodesByType[node.type] = (summary.nodesByType[node.type] || 0) + 1;
        });
        
        // Calculate completion rate
        const doneNodes = summary.nodesByType['done'] || 0;
        const totalActionableNodes = (summary.nodesByType['todo'] || 0) + 
                                   (summary.nodesByType['in_progress'] || 0) + 
                                   doneNodes;
        
        if (totalActionableNodes > 0) {
            summary.completionRate = Math.round((doneNodes / totalActionableNodes) * 100);
        }
        
        // Find isolated nodes
        const connectedNodeIds = new Set();
        this.connections.forEach(conn => {
            connectedNodeIds.add(conn.from);
            connectedNodeIds.add(conn.to);
        });
        
        summary.isolatedNodes = this.nodes.filter(node => !connectedNodeIds.has(node.id));
        
        return summary;
    }
}

// Enhanced global functions
function exportToJSON() {
    if (window.mindmap && window.mindmap.exportToJSON) {
        window.mindmap.exportToJSON();
    }
}

function importFromJSON() {
    if (window.mindmap && window.mindmap.importFromJSON) {
        window.mindmap.importFromJSON();
    }
}

function showMindMapSummary() {
    if (window.mindmap && window.mindmap.generateSummary) {
        const summary = window.mindmap.generateSummary();
        
        const dialog = document.createElement('div');
        dialog.className = 'summary-dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <h3>📊 Mind Map Summary</h3>
                <div class="summary-stats">
                    <div class="stat-card">
                        <div class="stat-number">${summary.totalNodes}</div>
                        <div class="stat-label">Total Nodes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${summary.totalConnections}</div>
                        <div class="stat-label">Connections</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${summary.completionRate}%</div>
                        <div class="stat-label">Completion Rate</div>
                    </div>
                </div>
                
                <div class="type-breakdown">
                    <h4>Node Types</h4>
                    ${Object.entries(summary.nodesByType).map(([type, count]) => `
                        <div class="type-item">
                            <div class="legend-color ${type}"></div>
                            <span>${type.replace('_', ' ').toUpperCase()}: ${count}</span>
                        </div>
                    `).join('')}
                </div>
                
                ${summary.isolatedNodes.length > 0 ? `
                    <div class="isolated-warning">
                        ⚠️ ${summary.isolatedNodes.length} isolated node(s) found
                    </div>
                ` : ''}
                
                <div class="dialog-actions">
                    <button class="btn btn-primary" onclick="this.parentElement.parentElement.parentElement.remove()">Close</button>
                </div>
            </div>
        `;
        
        dialog.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            animation: fadeIn 0.3s ease;
        `;
        
        document.body.appendChild(dialog);
    }
}

// Enhanced CSS animations
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
    
    @keyframes bounceIn {
        0% {
            transform: scale(0.3);
            opacity: 0;
        }
        50% {
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    .mindmap-notification {
        animation: slideInRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .node-creation-dialog {
        animation: bounceIn 0.5s ease;
    }
    
    /* Enhanced hover effects */
    .btn:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .fab:hover {
        transform: scale(1.15) rotate(180deg);
        box-shadow: 0 15px 35px rgba(0,123,255,0.4);
    }
    
    /* Loading spinner for better UX */
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
        margin-right: 8px;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);