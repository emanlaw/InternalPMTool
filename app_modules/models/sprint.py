from datetime import datetime, date
from typing import List, Dict, Optional

class Sprint:
    def __init__(self, id: int, name: str, project_id: int, start_date: date, end_date: date, 
                 goal: str = "", status: str = "planning", story_points: int = 0):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.start_date = start_date
        self.end_date = end_date
        self.goal = goal
        self.status = status  # planning, active, completed, cancelled
        self.story_points = story_points
        self.created_at = datetime.now()
        self.issues = []  # List of issue IDs assigned to this sprint
        
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'project_id': self.project_id,
            'start_date': self.start_date.isoformat() if isinstance(self.start_date, date) else self.start_date,
            'end_date': self.end_date.isoformat() if isinstance(self.end_date, date) else self.end_date,
            'goal': self.goal,
            'status': self.status,
            'story_points': self.story_points,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'issues': self.issues
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Sprint':
        sprint = cls(
            id=data['id'],
            name=data['name'],
            project_id=data['project_id'],
            start_date=datetime.fromisoformat(data['start_date']).date() if isinstance(data['start_date'], str) else data['start_date'],
            end_date=datetime.fromisoformat(data['end_date']).date() if isinstance(data['end_date'], str) else data['end_date'],
            goal=data.get('goal', ''),
            status=data.get('status', 'planning'),
            story_points=data.get('story_points', 0)
        )
        sprint.created_at = datetime.fromisoformat(data['created_at']) if isinstance(data['created_at'], str) else data['created_at']
        sprint.issues = data.get('issues', [])
        return sprint
    
    def get_duration_days(self) -> int:
        return (self.end_date - self.start_date).days + 1
    
    def is_active(self) -> bool:
        today = date.today()
        return self.start_date <= today <= self.end_date and self.status == 'active'
    
    def get_progress_percentage(self) -> float:
        if not self.issues:
            return 0.0
        # This would need to be calculated based on actual issue completion
        # For now, return a placeholder
        return 0.0