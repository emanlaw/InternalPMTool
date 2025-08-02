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
            this.save(true); // Silent save
        }
    }
    
    save(silent = false) {
        const projectId = document.getElementById('projectSelect').value;
        if (!projectId) {
            if (!silent) alert('Please select a project first');
            return;
        }
        
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
                    this.showNotification('Mind map saved successfully!', 'success');
                }
            } else {
                if (!silent) {
                    this.showNotification('Error saving mind map: ' + result.error, 'error');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (!silent) {
                this.showNotification('Error saving mind map', 'error');
            }
        });
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 6px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
            ${type === 'success' ? 'background: #36b37e;' : 
              type === 'error' ? 'background: #ff5630;' : 'background: #0079bf;'}
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        }, 3000);
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
            <div class="legend-item">
                <div class="legend-color todo"></div>
                <span>TODO</span>
            </div>
            <div class="legend-item">
                <div class="legend-color in_progress"></div>
                <span>In Progress</span>
            </div>
            <div class="legend-item">
                <div class="legend-color done"></div>
                <span>Done</span>
            </div>
            <div class="legend-item">
                <div class="legend-color idea"></div>
                <span>Idea</span>
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
            isolatedNodes: []
        };
        
        // Count nodes by type
        this.nodes.forEach(node => {
            summary.nodesByType[node.type] = (summary.nodesByType[node.type] || 0) + 1;
        });
        
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
        alert(`Mind Map Summary:
Total Nodes: ${summary.totalNodes}
Total Connections: ${summary.totalConnections}
Isolated Nodes: ${summary.isolatedNodes.length}

Nodes by Type:
${Object.entries(summary.nodesByType).map(([type, count]) => `${type}: ${count}`).join('\n')}`);
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);