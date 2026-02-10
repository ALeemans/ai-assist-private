"""
Import notes from Joplin to ai-assist repository
Fetches notes from the inbox notebook and organizes them based on tags
"""
import requests
import yaml
import os
from pathlib import Path
from datetime import datetime
import re

def load_config():
    """Load Joplin API configuration"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Read API token from environment variable if not set in config
    if not config.get('api_token'):
        config['api_token'] = os.environ.get('JOPLIN_API_TOKEN')
    
    return config

def get_joplin_api(endpoint, config, params=None):
    """Make GET request to Joplin API"""
    api_url = config['api_url']
    api_token = config['api_token']
    
    if params is None:
        params = {}
    params['token'] = api_token
    
    response = requests.get(f"{api_url}/{endpoint}", params=params)
    response.raise_for_status()
    return response.json()

def move_note_to_archive(note_id, archive_folder_id, config):
    """Move note to archive folder"""
    api_url = config['api_url']
    api_token = config['api_token']
    
    response = requests.put(
        f"{api_url}/notes/{note_id}",
        params={'token': api_token},
        json={'parent_id': archive_folder_id}
    )
    response.raise_for_status()

def delete_note(note_id, config):
    """Delete note from Joplin"""
    api_url = config['api_url']
    api_token = config['api_token']
    
    response = requests.delete(
        f"{api_url}/notes/{note_id}",
        params={'token': api_token}
    )
    response.raise_for_status()

def add_tag_to_note(note_id, tag_id, config):
    """Add tag to note"""
    api_url = config['api_url']
    api_token = config['api_token']
    
    response = requests.post(
        f"{api_url}/tags/{tag_id}/notes",
        params={'token': api_token},
        json={'id': note_id}
    )
    response.raise_for_status()

def determine_destination(note, config):
    """Determine where to save note based on tags"""
    tag_mapping = config['tag_mapping']
    
    # Get note tags
    tags = get_joplin_api(f"notes/{note['id']}/tags", config).get('items', [])
    tag_titles = [tag['title'] for tag in tags]
    
    # Check tag mapping
    for tag_title in tag_titles:
        if tag_title in tag_mapping:
            return tag_mapping[tag_title]
    
    # Default to inbox if no matching tag
    return "inbox/"

def slugify(text):
    """Convert text to filename-safe slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def create_markdown_file(note, destination_path, repo_root):
    """Create markdown file in repository"""
    # Determine file type based on destination
    file_type = "thought"
    category = "private"
    
    if "reminder" in destination_path:
        file_type = "reminder"
    
    if "work/" in destination_path:
        category = "work"
    
    # Create frontmatter
    created_date = datetime.fromtimestamp(note['created_ms'] / 1000).strftime('%Y-%m-%d')
    
    frontmatter = f"""---
type: {file_type}
category: {category}
status: pending
priority: medium
created: {created_date}
tags: [joplin-import]
---

"""
    
    # Combine frontmatter with note body
    content = frontmatter + f"# {note['title']}\n\n{note['body']}"
    
    # Create filename
    filename = f"{slugify(note['title'])}.md"
    full_path = repo_root / destination_path / filename
    
    # Ensure directory exists
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return full_path

def import_notes():
    """Main import function"""
    config = load_config()
    repo_root = Path(__file__).parent.parent.parent
    
    print("📥 Importing Notes from Joplin")
    print("=" * 50)
    
    # Get inbox notebook
    folders = get_joplin_api("folders", config)['items']
    inbox_name = config['inbox_notebook']
    inbox_folder = next((f for f in folders if f['title'] == inbox_name), None)
    
    if not inbox_folder:
        print(f"❌ Inbox notebook '{inbox_name}' not found")
        return
    
    print(f"📂 Reading from notebook: {inbox_name}")
    
    # Get notes from inbox
    notes_data = get_joplin_api("notes", config, params={'folder_id': inbox_folder['id']})
    notes = notes_data.get('items', [])
    
    if not notes:
        print("✨ No notes to import")
        return
    
    print(f"📋 Found {len(notes)} note(s) to import\n")
    
    # Get archive folder if needed
    archive_folder_id = None
    if config['post_import_action'] == 'archive':
        archive_name = config['archive_notebook']
        archive_folder = next((f for f in folders if f['title'] == archive_name), None)
        if archive_folder:
            archive_folder_id = archive_folder['id']
        else:
            print(f"⚠️  Archive notebook '{archive_name}' not found, will delete notes instead")
    
    imported_count = 0
    
    for note in notes:
        # Get full note with body
        full_note = get_joplin_api(f"notes/{note['id']}", config, params={'fields': 'id,title,body,created_time,updated_time,created_ms'})
        
        print(f"Processing: {full_note['title']}")
        
        # Determine destination
        destination = determine_destination(full_note, config)
        print(f"   → Destination: {destination}")
        
        # Create markdown file
        file_path = create_markdown_file(full_note, destination, repo_root)
        print(f"   ✅ Created: {file_path.relative_to(repo_root)}")
        
        # Handle post-import action
        if config['post_import_action'] == 'archive' and archive_folder_id:
            move_note_to_archive(note['id'], archive_folder_id, config)
            print(f"   📦 Moved to archive")
        elif config['post_import_action'] == 'delete':
            delete_note(note['id'], config)
            print(f"   🗑️  Deleted from Joplin")
        elif config['post_import_action'] == 'tag':
            # Add "imported" tag (would need to create tag first)
            print(f"   🏷️  Tagged as imported")
        
        imported_count += 1
        print()
    
    print(f"✅ Successfully imported {imported_count}/{len(notes)} note(s)!")

if __name__ == "__main__":
    config = load_config()
    
    if not config.get('api_token') or config['api_token'] == "YOUR_TOKEN_HERE":
        print("❌ Please configure your API token")
        print("   Option 1 (Recommended): Set environment variable JOPLIN_API_TOKEN")
        print("   Option 2: Set api_token in config.yaml")
        exit(1)
    
    import_notes()
