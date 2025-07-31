#!/usr/bin/env python3
"""
Migrate existing JSON data to Firebase
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.user import load_data
from datetime import datetime

def migrate_data_to_firebase():
    print("Starting data migration to Firebase...")
    
    try:
        from app.services.firebase_service import firebase_service
        from config.firebase_config import firebase_config
        
        if firebase_config.db is None:
            print("❌ Firebase not configured. Please set up Firebase credentials first.")
            return False
        
        # Load existing JSON data
        json_data = load_data()
        print(f"Found {len(json_data['projects'])} projects and {len(json_data['cards'])} cards in JSON")
        
        # Migrate projects
        print("\\nMigrating projects...")
        for project in json_data['projects']:\n            try:\n                firebase_project = {\n                    'name': project['name'],\n                    'description': project.get('description', '')\n                }\n                created_project = firebase_service.create_project(firebase_project)\n                print(f\"✅ Migrated project: {project['name']} -> {created_project['id']}\")\n            except Exception as e:\n                print(f\"❌ Failed to migrate project {project['name']}: {e}\")\n        \n        # Get all Firebase projects to map IDs\n        firebase_projects = firebase_service.get_all_projects()\n        project_id_map = {}\n        \n        # Create mapping from JSON project names to Firebase IDs\n        for json_project in json_data['projects']:\n            for firebase_project in firebase_projects:\n                if firebase_project['name'] == json_project['name']:\n                    project_id_map[json_project['id']] = firebase_project['id']\n                    break\n        \n        print(f\"\\nProject ID mapping: {project_id_map}\")\n        \n        # Migrate cards\n        print(\"\\nMigrating cards...\")\n        for card in json_data['cards']:\n            try:\n                # Map the project ID\n                firebase_project_id = project_id_map.get(card['project_id'])\n                if not firebase_project_id:\n                    print(f\"⚠️  Skipping card '{card['title']}' - no matching project found\")\n                    continue\n                \n                firebase_card = {\n                    'project_id': firebase_project_id,\n                    'title': card['title'],\n                    'description': card.get('description', ''),\n                    'status': card['status'],\n                    'assignee': card.get('assignee', ''),\n                    'priority': card['priority'],\n                    'due_date': card.get('due_date', '')\n                }\n                created_card = firebase_service.create_card(firebase_card)\n                print(f\"✅ Migrated card: {card['title']} -> {created_card['id']}\")\n            except Exception as e:\n                print(f\"❌ Failed to migrate card {card['title']}: {e}\")\n        \n        # Migrate comments if any\n        if json_data.get('comments'):\n            print(\"\\nMigrating comments...\")\n            # Note: This would require mapping card IDs as well\n            print(\"⚠️  Comment migration not implemented yet (requires card ID mapping)\")\n        \n        print(\"\\n🎉 Data migration completed!\")\n        \n        # Verify migration\n        firebase_projects = firebase_service.get_all_projects()\n        firebase_cards = firebase_service.get_all_cards()\n        \n        print(f\"\\nVerification:\")\n        print(f\"Firebase now has {len(firebase_projects)} projects and {len(firebase_cards)} cards\")\n        \n        return True\n        \n    except Exception as e:\n        print(f\"❌ Migration failed: {str(e)}\")\n        import traceback\n        traceback.print_exc()\n        return False\n\ndef backup_json_data():\n    \"\"\"Create a backup of the current JSON data\"\"\"\n    import shutil\n    from datetime import datetime\n    \n    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')\n    backup_filename = f\"data_backup_{timestamp}.json\"\n    \n    try:\n        shutil.copy('data.json', backup_filename)\n        print(f\"✅ JSON data backed up to {backup_filename}\")\n        return True\n    except Exception as e:\n        print(f\"❌ Failed to backup JSON data: {e}\")\n        return False\n\nif __name__ == \"__main__\":\n    print(\"=\" * 60)\n    print(\"Firebase Data Migration Tool\")\n    print(\"=\" * 60)\n    \n    # Create backup first\n    print(\"Step 1: Creating backup of JSON data...\")\n    backup_ok = backup_json_data()\n    \n    if not backup_ok:\n        print(\"❌ Backup failed. Aborting migration.\")\n        sys.exit(1)\n    \n    # Perform migration\n    print(\"\\nStep 2: Migrating data to Firebase...\")\n    success = migrate_data_to_firebase()\n    \n    print(\"\\n\" + \"=\" * 60)\n    if success:\n        print(\"🎉 Migration completed successfully!\")\n        print(\"Your data is now stored in Firebase.\")\n        print(\"\\nNext steps:\")\n        print(\"1. Test the application to ensure everything works\")\n        print(\"2. If satisfied, you can remove the JSON backup files\")\n    else:\n        print(\"❌ Migration failed.\")\n        print(\"Your original JSON data is safe in the backup file.\")\n        print(\"Please check the Firebase setup and try again.\")\n    print(\"=\" * 60)\n    \n    sys.exit(0 if success else 1)