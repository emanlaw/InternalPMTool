#!/usr/bin/env python3
"""
Data Manager - handles loading and saving data from separate files
"""

import json
import os
from datetime import datetime

class DataManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.files = {
            'users': 'users.json',
            'projects': 'projects.json', 
            'epics': 'epics.json',
            'stories': 'stories.json',
            'cards': 'cards.json',
            'comments': 'comments.json',
            'sprints': 'sprints.json'
        }
        
    def load_data(self):
        """Load all data from separate files"""
        data = {}
        
        for key, filename in self.files.items():
            filepath = os.path.join(self.data_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    content = f.read().strip()
                    if content:
                        data[key] = json.loads(content)
                    else:
                        data[key] = []
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading {filepath}: {e}")
                data[key] = []
                # Create empty file
                self._save_file(key, [])
        
        # Add missing collections if not exist
        if 'notifications' not in data:
            data['notifications'] = []
        if 'sprints' not in data:
            data['sprints'] = []
            
        return data
    
    def save_data(self, data):
        """Save data to separate files"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        for key in self.files.keys():
            if key in data:
                self._save_file(key, data[key])
    
    def _save_file(self, key, data_list):
        """Save individual data file"""
        filepath = os.path.join(self.data_dir, self.files[key])
        with open(filepath, 'w') as f:
            json.dump(data_list, f, indent=2)
    
    def backup_data(self):
        """Create backup of all data files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f'backup_{timestamp}'
        os.makedirs(backup_dir, exist_ok=True)
        
        data = self.load_data()
        backup_file = os.path.join(backup_dir, f'data_backup_{timestamp}.json')
        
        with open(backup_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return backup_file