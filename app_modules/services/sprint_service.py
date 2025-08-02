import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional
from app_modules.models.sprint import Sprint

class SprintService:
    def __init__(self, data_file: str = "data/sprints.json"):
        self.data_file = data_file
        self.ensure_data_file()
    
    def ensure_data_file(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def load_sprints(self) -> List[Sprint]:
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return [Sprint.from_dict(sprint_data) for sprint_data in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_sprints(self, sprints: List[Sprint]):
        with open(self.data_file, 'w') as f:
            json.dump([sprint.to_dict() for sprint in sprints], f, indent=2)
    
    def create_sprint(self, name: str, project_id: int, start_date: date, end_date: date, 
                     goal: str = "", story_points: int = 0) -> Sprint:
        sprints = self.load_sprints()
        new_id = max([s.id for s in sprints], default=0) + 1
        
        sprint = Sprint(
            id=new_id,
            name=name,
            project_id=project_id,
            start_date=start_date,
            end_date=end_date,
            goal=goal,
            story_points=story_points
        )
        
        sprints.append(sprint)
        self.save_sprints(sprints)
        return sprint
    
    def get_sprint_by_id(self, sprint_id: int) -> Optional[Sprint]:
        sprints = self.load_sprints()
        return next((s for s in sprints if s.id == sprint_id), None)
    
    def get_sprints_by_project(self, project_id: int) -> List[Sprint]:
        sprints = self.load_sprints()
        return [s for s in sprints if s.project_id == project_id]
    
    def get_all_sprints(self) -> List[Sprint]:
        return self.load_sprints()
    
    def update_sprint(self, sprint_id: int, **kwargs) -> Optional[Sprint]:
        sprints = self.load_sprints()
        sprint = next((s for s in sprints if s.id == sprint_id), None)
        
        if sprint:
            for key, value in kwargs.items():
                if hasattr(sprint, key):
                    if key in ['start_date', 'end_date'] and isinstance(value, str):
                        setattr(sprint, key, datetime.fromisoformat(value).date())
                    else:
                        setattr(sprint, key, value)
            
            self.save_sprints(sprints)
            return sprint
        return None
    
    def delete_sprint(self, sprint_id: int) -> bool:
        sprints = self.load_sprints()
        original_count = len(sprints)
        sprints = [s for s in sprints if s.id != sprint_id]
        
        if len(sprints) < original_count:
            self.save_sprints(sprints)
            return True
        return False
    
    def assign_issue_to_sprint(self, sprint_id: int, issue_id: int) -> bool:
        sprint = self.get_sprint_by_id(sprint_id)
        if sprint and issue_id not in sprint.issues:
            sprint.issues.append(issue_id)
            sprints = self.load_sprints()
            for i, s in enumerate(sprints):
                if s.id == sprint_id:
                    sprints[i] = sprint
                    break
            self.save_sprints(sprints)
            return True
        return False
    
    def remove_issue_from_sprint(self, sprint_id: int, issue_id: int) -> bool:
        sprint = self.get_sprint_by_id(sprint_id)
        if sprint and issue_id in sprint.issues:
            sprint.issues.remove(issue_id)
            sprints = self.load_sprints()
            for i, s in enumerate(sprints):
                if s.id == sprint_id:
                    sprints[i] = sprint
                    break
            self.save_sprints(sprints)
            return True
        return False
    
    def get_active_sprints(self) -> List[Sprint]:
        sprints = self.load_sprints()
        return [s for s in sprints if s.is_active()]
    
    def start_sprint(self, sprint_id: int) -> bool:
        return self.update_sprint(sprint_id, status='active') is not None
    
    def complete_sprint(self, sprint_id: int) -> bool:
        return self.update_sprint(sprint_id, status='completed') is not None