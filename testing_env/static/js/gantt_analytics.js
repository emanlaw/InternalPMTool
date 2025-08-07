// Gantt Analytics JavaScript
class GanttAnalytics {
    constructor() {
        this.charts = {};
        this.data = {};
        this.init();
    }

    async init() {
        await this.loadData();
        this.updateHealthMetrics();
        this.initCharts();
        this.calculatePredictiveAnalytics();
    }

    async loadData() {
        try {
            const response = await fetch('/api/analytics/data');
            this.data = await response.json();
        } catch (error) {
            console.error('Error loading analytics data:', error);
            // Fallback to mock data for demo
            this.data = this.getMockData();
        }
    }

    getMockData() {
        return {
            projects: [
                { id: 1, name: 'Project Alpha', status: 'on-track', progress: 75, budget: 100000, spent: 65000 },
                { id: 2, name: 'Project Beta', status: 'at-risk', progress: 45, budget: 80000, spent: 55000 },
                { id: 3, name: 'Project Gamma', status: 'overdue', progress: 30, budget: 120000, spent: 90000 }
            ],
            tasks: [
                { id: 1, project_id: 1, status: 'done', assignee: 'John', hours: 40 },
                { id: 2, project_id: 1, status: 'in_progress', assignee: 'Jane', hours: 30 },
                { id: 3, project_id: 2, status: 'overdue', assignee: 'Bob', hours: 50 }
            ],
            resources: [
                { name: 'John', utilization: 85, capacity: 40 },
                { name: 'Jane', utilization: 70, capacity: 40 },
                { name: 'Bob', utilization: 95, capacity: 40 }
            ]
        };
    }

    updateHealthMetrics() {
        const projects = this.data.projects || [];
        const onTrack = projects.filter(p => p.status === 'on-track').length;
        const atRisk = projects.filter(p => p.status === 'at-risk').length;
        const overdue = projects.filter(p => p.status === 'overdue').length;
        const completed = projects.filter(p => p.status === 'completed').length;

        document.getElementById('on-track-count').textContent = onTrack;
        document.getElementById('at-risk-count').textContent = atRisk;
        document.getElementById('overdue-count').textContent = overdue;
        document.getElementById('completed-count').textContent = completed;
    }

    initCharts() {
        this.initProgressChart();
        this.initResourceChart();
        this.initPerformanceChart();
    }

    initProgressChart() {
        const ctx = document.getElementById('progressChart').getContext('2d');
        const projects = this.data.projects || [];
        
        this.charts.progress = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: projects.map(p => p.name),
                datasets: [{
                    data: projects.map(p => p.progress),
                    backgroundColor: [
                        '#28a745',
                        '#ffc107',
                        '#dc3545',
                        '#17a2b8'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    initResourceChart() {
        const ctx = document.getElementById('resourceChart').getContext('2d');
        const resources = this.data.resources || [];
        
        this.charts.resource = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: resources.map(r => r.name),
                datasets: [{
                    label: 'Utilization %',
                    data: resources.map(r => r.utilization),
                    backgroundColor: resources.map(r => 
                        r.utilization > 90 ? '#dc3545' : 
                        r.utilization > 80 ? '#ffc107' : '#28a745'
                    )
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    initPerformanceChart() {
        const ctx = document.getElementById('performanceChart').getContext('2d');
        
        // Mock performance data over time
        const performanceData = [
            { month: 'Jan', velocity: 25, quality: 85, satisfaction: 90 },
            { month: 'Feb', velocity: 30, quality: 88, satisfaction: 85 },
            { month: 'Mar', velocity: 28, quality: 92, satisfaction: 88 },
            { month: 'Apr', velocity: 35, quality: 90, satisfaction: 92 },
            { month: 'May', velocity: 32, quality: 87, satisfaction: 89 },
            { month: 'Jun', velocity: 38, quality: 94, satisfaction: 95 }
        ];
        
        this.charts.performance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: performanceData.map(d => d.month),
                datasets: [
                    {
                        label: 'Velocity',
                        data: performanceData.map(d => d.velocity),
                        borderColor: '#007bff',
                        tension: 0.1
                    },
                    {
                        label: 'Quality Score',
                        data: performanceData.map(d => d.quality),
                        borderColor: '#28a745',
                        tension: 0.1
                    },
                    {
                        label: 'Satisfaction',
                        data: performanceData.map(d => d.satisfaction),
                        borderColor: '#ffc107',
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    calculatePredictiveAnalytics() {
        const projects = this.data.projects || [];
        
        // Calculate estimated completion
        const avgProgress = projects.reduce((sum, p) => sum + p.progress, 0) / projects.length;
        const estimatedDays = Math.ceil((100 - avgProgress) * 2); // Simple calculation
        const estimatedDate = new Date();
        estimatedDate.setDate(estimatedDate.getDate() + estimatedDays);
        
        document.getElementById('estimated-completion').textContent = 
            estimatedDate.toLocaleDateString();
        
        // Calculate budget variance
        const totalBudget = projects.reduce((sum, p) => sum + p.budget, 0);
        const totalSpent = projects.reduce((sum, p) => sum + p.spent, 0);
        const variance = ((totalSpent - totalBudget) / totalBudget * 100).toFixed(1);
        
        document.getElementById('budget-variance').textContent = `${variance}%`;
        document.getElementById('budget-variance').className = 
            `h4 ${variance > 0 ? 'text-danger' : 'text-success'}`;
        
        // Calculate risk score
        const overdueTasks = this.data.tasks?.filter(t => t.status === 'overdue').length || 0;
        const totalTasks = this.data.tasks?.length || 1;
        const riskScore = Math.min(100, (overdueTasks / totalTasks * 100 + Math.abs(variance))).toFixed(0);
        
        document.getElementById('risk-score').textContent = `${riskScore}/100`;
        document.getElementById('risk-score').className = 
            `h4 ${riskScore > 70 ? 'text-danger' : riskScore > 40 ? 'text-warning' : 'text-success'}`;
    }
}

// Report generation functions
async function generateReport() {
    const reportType = document.getElementById('reportType').value;
    
    try {
        const response = await fetch(`/api/analytics/report/${reportType}`);
        const reportData = await response.json();
        
        document.getElementById('reportContent').innerHTML = formatReport(reportData, reportType);
        
        const modal = new bootstrap.Modal(document.getElementById('reportModal'));
        modal.show();
    } catch (error) {
        console.error('Error generating report:', error);
        alert('Error generating report. Please try again.');
    }
}

function formatReport(data, type) {
    switch (type) {
        case 'project-health':
            return formatProjectHealthReport(data);
        case 'resource-utilization':
            return formatResourceUtilizationReport(data);
        case 'performance-metrics':
            return formatPerformanceMetricsReport(data);
        case 'risk-assessment':
            return formatRiskAssessmentReport(data);
        default:
            return '<p>Report type not supported</p>';
    }
}

function formatProjectHealthReport(data) {
    return `
        <h4>Project Health Report</h4>
        <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Project</th>
                        <th>Status</th>
                        <th>Progress</th>
                        <th>Budget Utilization</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.projects?.map(p => `
                        <tr>
                            <td>${p.name}</td>
                            <td><span class="badge bg-${getStatusColor(p.status)}">${p.status}</span></td>
                            <td>${p.progress}%</td>
                            <td>${((p.spent / p.budget) * 100).toFixed(1)}%</td>
                        </tr>
                    `).join('') || '<tr><td colspan="4">No data available</td></tr>'}
                </tbody>
            </table>
        </div>
    `;
}

function formatResourceUtilizationReport(data) {
    return `
        <h4>Resource Utilization Report</h4>
        <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Resource</th>
                        <th>Utilization</th>
                        <th>Capacity</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.resources?.map(r => `
                        <tr>
                            <td>${r.name}</td>
                            <td>${r.utilization}%</td>
                            <td>${r.capacity}h</td>
                            <td><span class="badge bg-${getUtilizationColor(r.utilization)}">${getUtilizationStatus(r.utilization)}</span></td>
                        </tr>
                    `).join('') || '<tr><td colspan="4">No data available</td></tr>'}
                </tbody>
            </table>
        </div>
    `;
}

function formatPerformanceMetricsReport(data) {
    return `
        <h4>Performance Metrics Report</h4>
        <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
        <div class="row">
            <div class="col-md-4">
                <h6>Average Velocity</h6>
                <p class="h4">32 points/sprint</p>
            </div>
            <div class="col-md-4">
                <h6>Quality Score</h6>
                <p class="h4">89%</p>
            </div>
            <div class="col-md-4">
                <h6>Team Satisfaction</h6>
                <p class="h4">91%</p>
            </div>
        </div>
    `;
}

function formatRiskAssessmentReport(data) {
    return `
        <h4>Risk Assessment Report</h4>
        <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
        <div class="alert alert-warning">
            <h6>High Risk Items:</h6>
            <ul>
                <li>Project Beta is 2 weeks behind schedule</li>
                <li>Resource Bob is over-utilized at 95%</li>
                <li>Budget variance of +12% across all projects</li>
            </ul>
        </div>
    `;
}

function getStatusColor(status) {
    const colors = {
        'on-track': 'success',
        'at-risk': 'warning',
        'overdue': 'danger',
        'completed': 'info'
    };
    return colors[status] || 'secondary';
}

function getUtilizationColor(utilization) {
    if (utilization > 90) return 'danger';
    if (utilization > 80) return 'warning';
    return 'success';
}

function getUtilizationStatus(utilization) {
    if (utilization > 90) return 'Over-utilized';
    if (utilization > 80) return 'High';
    return 'Normal';
}

function scheduleReport() {
    alert('Report scheduling feature coming soon!');
}

function downloadReport() {
    const content = document.getElementById('reportContent').innerHTML;
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>Analytics Report</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body class="p-4">
                ${content}
            </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

// Initialize analytics when page loads
document.addEventListener('DOMContentLoaded', function() {
    new GanttAnalytics();
});