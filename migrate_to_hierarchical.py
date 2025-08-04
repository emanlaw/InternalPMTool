#!/usr/bin/env python3
"""
Migration script to convert flat project structure to hierarchical structure:
Project > Epic > Story > Issue > Sub-Issue

This script will:
1. Create default epics for each project
2. Create default stories under each epic
3. Move existing cards/issues under stories
4. Preserve all existing data
"""

import json
from datetime import datetime

def migrate_data():
    """Migrate existing flat structure to hierarchical structure"""
    
    # Load existing data
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No data.json file found. Nothing to migrate.")
        return
    
    print("Starting migration to hierarchical structure...")
    
    # Initialize new collections if they don't exist
    if 'epics' not in data:
        data['epics'] = []
    if 'stories' not in data:
        data['stories'] = []
    
    # Get existing data
    projects = data.get('projects', [])
    cards = data.get('cards', [])
    
    print(f"Found {len(projects)} projects and {len(cards)} cards to migrate")
    
    # Create default epics and stories for each project
    epic_id_counter = max([e.get('id', 0) for e in data['epics']], default=0)
    story_id_counter = max([s.get('id', 0) for s in data['stories']], default=0)
    
    for project in projects:
        project_id = project['id']
        project_name = project['name']
        
        # Check if project already has epics
        existing_epics = [e for e in data['epics'] if e['project_id'] == project_id]
        if existing_epics:
            print(f"Project '{project_name}' already has epics, skipping...")
            continue
        
        print(f"Migrating project: {project_name}")
        
        # Create default epic for this project
        epic_id_counter += 1
        default_epic = {
            'id': epic_id_counter,
            'project_id': project_id,
            'title': f"{project_name} - Main Epic",
            'description': f"Default epic created during migration for {project_name}",
            'status': 'active',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': 'migration_script'
        }
        data['epics'].append(default_epic)
        
        # Create default story under this epic
        story_id_counter += 1
        default_story = {
            'id': story_id_counter,
            'epic_id': epic_id_counter,
            'project_id': project_id,
            'title': f"{project_name} - Main Story",
            'description': f"Default story created during migration for {project_name}",
            'status': 'in_progress',
            'story_points': 0,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': 'migration_script'
        }
        data['stories'].append(default_story)
        
        # Update all cards for this project to belong to the default story
        project_cards = [c for c in cards if c.get('project_id') == project_id]
        for card in project_cards:
            card['epic_id'] = epic_id_counter
            card['story_id'] = story_id_counter
            print(f"  - Migrated card: {card['title']}")
    
    # Create backup of original data
    backup_filename = f"data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open('data.json', 'r') as f:
            original_data = f.read()
        with open(backup_filename, 'w') as f:
            f.write(original_data)
        print(f"Backup created: {backup_filename}")
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")
    
    # Save migrated data
    try:
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("Migration completed successfully!")
        print(f"Created {len(data['epics'])} epics and {len(data['stories'])} stories")
        
        # Print summary
        print("\nMigration Summary:")
        for project in projects:
            project_id = project['id']
            project_epics = [e for e in data['epics'] if e['project_id'] == project_id]
            project_stories = [s for s in data['stories'] if s['project_id'] == project_id]
            project_cards = [c for c in cards if c.get('project_id') == project_id]
            
            print(f"  {project['name']}:")
            print(f"    - Epics: {len(project_epics)}")
            print(f"    - Stories: {len(project_stories)}")
            print(f"    - Issues: {len(project_cards)}")
        
    except Exception as e:
        print(f"Error saving migrated data: {e}")
        print("Migration failed!")
        return False
    
    return True

def verify_migration():
    """Verify that the migration was successful"""
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No data.json file found for verification.")
        return False
    
    print("\nVerifying migration...")
    
    # Check that all cards have epic_id and story_id
    cards = data.get('cards', [])
    orphaned_cards = []
    
    for card in cards:
        if not card.get('epic_id') or not card.get('story_id'):
            orphaned_cards.append(card)
    
    if orphaned_cards:
        print(f"Warning: Found {len(orphaned_cards)} cards without proper hierarchy:")
        for card in orphaned_cards:
            print(f"  - {card['title']} (ID: {card['id']})")
        return False
    
    # Check that all stories have epic_id
    stories = data.get('stories', [])
    orphaned_stories = []
    
    for story in stories:
        if not story.get('epic_id'):
            orphaned_stories.append(story)
    
    if orphaned_stories:
        print(f"Warning: Found {len(orphaned_stories)} stories without epic:")
        for story in orphaned_stories:
            print(f"  - {story['title']} (ID: {story['id']})")
        return False
    
    print("✅ Migration verification passed!")
    print(f"✅ All {len(cards)} cards are properly linked to stories")
    print(f"✅ All {len(stories)} stories are properly linked to epics")
    
    return True

if __name__ == "__main__":
    print("🔄 Hierarchical Structure Migration Tool")
    print("=" * 50)
    
    # Run migration
    success = migrate_data()
    
    if success:
        # Verify migration
        verify_migration()
        print("\n🎉 Migration completed successfully!")
        print("\nNext steps:")
        print("1. Test the application with the new hierarchical structure")
        print("2. Create new epics and stories as needed")
        print("3. Organize existing issues under appropriate stories")
    else:
        print("\n❌ Migration failed. Please check the errors above.")