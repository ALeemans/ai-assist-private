"""
Archive completed reminders

This script checks for reminders with status: completed or cancelled and moves them
to the archive/ subdirectory to keep the active reminders folder clean.
"""

import yaml
from pathlib import Path
import shutil

def parse_frontmatter(file_path):
    """Extract YAML frontmatter from a markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return None, content
    
    try:
        _, frontmatter_text, body = content.split('---', 2)
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter, body.strip()
    except:
        return None, content

def archive_completed_reminders():
    """Find and archive completed reminders"""
    repo_root = Path(__file__).parent.parent.parent
    categories = ['work', 'private']
    
    archived_count = 0
    
    for category in categories:
        reminder_dir = repo_root / category / 'reminders'
        archive_dir = reminder_dir / 'archive'
        
        if not reminder_dir.exists():
            continue
        
        # Ensure archive directory exists
        archive_dir.mkdir(exist_ok=True)
        
        # Check all markdown files
        for reminder_file in reminder_dir.glob('*.md'):
            if reminder_file.name == 'README.md':
                continue
            
            frontmatter, _ = parse_frontmatter(reminder_file)
            
            if frontmatter and frontmatter.get('status') in ['completed', 'cancelled']:
                # Move to archive
                archive_path = archive_dir / reminder_file.name
                shutil.move(str(reminder_file), str(archive_path))
                status = frontmatter.get('status')
                print(f"📦 Archived ({status}): {category}/reminders/{reminder_file.name}")
                archived_count += 1
    
    if archived_count == 0:
        print("✅ No completed/cancelled reminders to archive")
    else:
        print(f"\n🎉 Archived {archived_count} reminder(s)")

if __name__ == "__main__":
    print("🔍 Checking for completed/cancelled reminders to archive...\n")
    archive_completed_reminders()
