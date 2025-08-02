from datetime import datetime, timedelta
from app.models.user import load_data
import json

class AnalyticsService:
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self):
        """Load data from Firebase or fallback to JSON"""
        try:
            from app.services.firebase_service import firebase_service
            from config.firebase_config import firebase_config
            
            if firebase_config.db is not None:
                # Load from Firebase
                projects = firebase_service.get_all_projects()
                cards = firebase_service.get_all_cards()
                
                # Convert Firebase data to match JSON structure
                for project in projects:
                    if isinstance(project.get('id'), str) and project['id'].startswith('PROJ-'):
                        project['id'] = int(project['id'].split('-')[1])
                
                for card in cards:
                    if isinstance(card.get('id'), str) and card['id'].startswith('CARD-'):
                        card['id'] = int(card['id'].split('-')[1])
                    if isinstance(card.get('project_id'), str):
                        if card['project_id'].startswith('PROJ-'):
                            card['project_id'] = int(card['project_id'].split('-')[1])
                        else:
                            card['project_id'] = int(card['project_id'])
                
                return {
                    'projects': projects,
                    'cards': cards,
                    'users': [],
                    'comments': []
                }
            else:
                return load_data()
        except Exception as e:
            print(f"Error loading Firebase data for analytics: {e}")
            return load_data()
    
    def get_project_health_data(self):
        """Calculate project health metrics"""
        projects = self.data.get('projects', [])
        cards = self.data.get('cards', [])
        
        project_health = []
        for project in projects:
            project_cards = [c for c in cards if c['project_id'] == project['id']]
            
            if not project_cards:
                continue
                
            total_cards = len(project_cards)
            done_cards = len([c for c in project_cards if c['status'] == 'done'])
            overdue_cards = len([c for c in project_cards if self._is_overdue(c)])
            
            progress = (done_cards / total_cards * 100) if total_cards > 0 else 0
            
            # Determine project status
            if overdue_cards > 0:
                status = 'overdue'
            elif progress < 30:
                status = 'at-risk'
            elif progress >= 100:
                status = 'completed'
            else:
                status = 'on-track'
            
            project_health.append({
                'id': project['id'],
                'name': project['name'],
                'status': status,
                'progress': round(progress, 1),
                'total_tasks': total_cards,
                'completed_tasks': done_cards,
                'overdue_tasks': overdue_cards,
                'budget': 100000,  # Mock budget data
                'spent': int(progress * 1000)  # Mock spending data
            })
        
        return project_health
    
    def get_resource_utilization_data(self):
        """Calculate resource utilization metrics"""
        cards = self.data.get('cards', [])
        
        # Group cards by assignee
        assignee_workload = {}
        for card in cards:
            assignee = card.get('assignee', 'Unassigned')
            if assignee != 'Unassigned' and assignee:
                if assignee not in assignee_workload:
                    assignee_workload[assignee] = {
                        'name': assignee,
                        'total_tasks': 0,
                        'completed_tasks': 0,
                        'in_progress_tasks': 0,
                        'overdue_tasks': 0
                    }
                
                assignee_workload[assignee]['total_tasks'] += 1
                
                if card['status'] == 'done':
                    assignee_workload[assignee]['completed_tasks'] += 1
                elif card['status'] == 'in_progress':
                    assignee_workload[assignee]['in_progress_tasks'] += 1
                
                if self._is_overdue(card):
                    assignee_workload[assignee]['overdue_tasks'] += 1
        
        # Calculate utilization percentages
        resources = []
        for assignee, data in assignee_workload.items():
            # Mock capacity calculation (40 hours per week)
            capacity = 40
            # Estimate utilization based on task load
            utilization = min(100, (data['total_tasks'] * 10))  # 10% per task
            
            resources.append({
                'name': assignee,
                'utilization': utilization,
                'capacity': capacity,
                'total_tasks': data['total_tasks'],
                'completed_tasks': data['completed_tasks'],
                'in_progress_tasks': data['in_progress_tasks'],
                'overdue_tasks': data['overdue_tasks']
            })
        
        return resources
    
    def get_performance_metrics(self):
        """Calculate performance metrics over time"""
        cards = self.data.get('cards', [])
        
        # Mock performance data - in real implementation, this would come from historical data
        performance_data = []
        
        # Generate last 6 months of data
        for i in range(6):
            date = datetime.now() - timedelta(days=30 * i)
            month_name = date.strftime('%b')
            
            # Mock calculations based on current data
            velocity = len([c for c in cards if c['status'] == 'done']) + (i * 2)
            quality_score = 85 + (i % 10)
            satisfaction_score = 88 + (i % 8)
            
            performance_data.append({
                'month': month_name,
                'velocity': min(40, velocity),
                'quality': min(100, quality_score),
                'satisfaction': min(100, satisfaction_score)
            })
        
        return list(reversed(performance_data))
    
    def get_predictive_analytics(self):
        """Calculate predictive analytics"""
        projects = self.get_project_health_data()
        
        if not projects:
            return {
                'estimated_completion': None,
                'budget_variance': 0,
                'risk_score': 0
            }
        
        # Calculate average progress
        avg_progress = sum(p['progress'] for p in projects) / len(projects)
        
        # Estimate completion date
        days_remaining = max(1, (100 - avg_progress) * 2)  # 2 days per percentage point
        estimated_completion = datetime.now() + timedelta(days=days_remaining)
        
        # Calculate budget variance
        total_budget = sum(p['budget'] for p in projects)
        total_spent = sum(p['spent'] for p in projects)
        budget_variance = ((total_spent - total_budget) / total_budget * 100) if total_budget > 0 else 0
        
        # Calculate risk score
        overdue_projects = len([p for p in projects if p['status'] == 'overdue'])
        at_risk_projects = len([p for p in projects if p['status'] == 'at-risk'])
        total_projects = len(projects)
        
        risk_score = 0
        if total_projects > 0:
            risk_score = ((overdue_projects * 2 + at_risk_projects) / total_projects * 50) + abs(budget_variance)
            risk_score = min(100, risk_score)
        
        return {
            'estimated_completion': estimated_completion.strftime('%Y-%m-%d'),
            'budget_variance': round(budget_variance, 1),
            'risk_score': round(risk_score, 0)
        }
    
    def generate_project_health_report(self):
        """Generate project health report"""
        projects = self.get_project_health_data()
        
        return {
            'title': 'Project Health Report',
            'generated_at': datetime.now().isoformat(),
            'projects': projects,
            'summary': {
                'total_projects': len(projects),
                'on_track': len([p for p in projects if p['status'] == 'on-track']),
                'at_risk': len([p for p in projects if p['status'] == 'at-risk']),
                'overdue': len([p for p in projects if p['status'] == 'overdue']),
                'completed': len([p for p in projects if p['status'] == 'completed'])
            }
        }
    
    def generate_resource_utilization_report(self):
        """Generate resource utilization report"""
        resources = self.get_resource_utilization_data()
        
        return {
            'title': 'Resource Utilization Report',
            'generated_at': datetime.now().isoformat(),
            'resources': resources,
            'summary': {
                'total_resources': len(resources),
                'over_utilized': len([r for r in resources if r['utilization'] > 90]),
                'high_utilization': len([r for r in resources if 80 < r['utilization'] <= 90]),
                'normal_utilization': len([r for r in resources if r['utilization'] <= 80])
            }
        }
    
    def generate_performance_metrics_report(self):
        """Generate performance metrics report"""
        performance_data = self.get_performance_metrics()
        
        if not performance_data:
            return {
                'title': 'Performance Metrics Report',
                'generated_at': datetime.now().isoformat(),
                'data': [],
                'summary': {}
            }
        
        avg_velocity = sum(d['velocity'] for d in performance_data) / len(performance_data)
        avg_quality = sum(d['quality'] for d in performance_data) / len(performance_data)
        avg_satisfaction = sum(d['satisfaction'] for d in performance_data) / len(performance_data)
        
        return {
            'title': 'Performance Metrics Report',
            'generated_at': datetime.now().isoformat(),
            'data': performance_data,
            'summary': {
                'average_velocity': round(avg_velocity, 1),
                'average_quality': round(avg_quality, 1),
                'average_satisfaction': round(avg_satisfaction, 1)
            }
        }
    
    def generate_risk_assessment_report(self):
        """Generate risk assessment report"""
        projects = self.get_project_health_data()
        resources = self.get_resource_utilization_data()
        predictive = self.get_predictive_analytics()
        
        risks = []
        
        # Project risks
        for project in projects:
            if project['status'] == 'overdue':
                risks.append({
                    'type': 'project',
                    'severity': 'high',
                    'description': f"Project {project['name']} is overdue with {project['overdue_tasks']} overdue tasks"
                })
            elif project['status'] == 'at-risk':
                risks.append({
                    'type': 'project',
                    'severity': 'medium',
                    'description': f"Project {project['name']} is at risk with {project['progress']}% completion"
                })
        
        # Resource risks
        for resource in resources:
            if resource['utilization'] > 90:
                risks.append({
                    'type': 'resource',
                    'severity': 'high',
                    'description': f"Resource {resource['name']} is over-utilized at {resource['utilization']}%"
                })
        
        # Budget risks
        if predictive['budget_variance'] > 10:
            risks.append({
                'type': 'budget',
                'severity': 'high',
                'description': f"Budget variance of {predictive['budget_variance']}% exceeds acceptable threshold"
            })
        
        return {
            'title': 'Risk Assessment Report',
            'generated_at': datetime.now().isoformat(),
            'risks': risks,
            'risk_score': predictive['risk_score'],
            'summary': {
                'total_risks': len(risks),
                'high_severity': len([r for r in risks if r['severity'] == 'high']),
                'medium_severity': len([r for r in risks if r['severity'] == 'medium']),
                'low_severity': len([r for r in risks if r['severity'] == 'low'])
            }
        }
    
    def _is_overdue(self, card):
        """Check if a card is overdue"""
        if not card.get('due_date'):
            return False
        
        try:
            due_date = datetime.strptime(card['due_date'], '%Y-%m-%d')
            return due_date < datetime.now() and card['status'] != 'done'
        except (ValueError, TypeError):
            return False