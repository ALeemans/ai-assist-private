"""
Sync reminder files to Google Calendar
Reads reminder markdown files and creates calendar events
Automatically routes work reminders to HU calendar and private to personal calendar
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent
TOKEN_FILE = SCRIPT_DIR / 'token.json'
CONFIG_FILE = SCRIPT_DIR / 'calendar-config.yaml'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def load_config():
    """Load calendar configuration"""
    if not CONFIG_FILE.exists():
        print("⚠️  calendar-config.yaml not found, using defaults")
        return None
    
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

def get_calendar_id_for_category(category, config):
    """Get the appropriate calendar ID for a reminder category"""
    if not config:
        return 'primary'
    
    # Get calendar key from category mapping
    calendar_key = config.get('category_mapping', {}).get(category, 'primary')
    
    # Get calendar ID from calendars section
    calendar_id = config.get('calendars', {}).get(calendar_key, {}).get('id', 'primary')
    
    return calendar_id

def get_calendar_service():
    """Get authenticated Google Calendar service"""
    if not TOKEN_FILE.exists():
        print("❌ Not authenticated. Run setup-google-calendar.py first")
        return None
    
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    return build('calendar', 'v3', credentials=creds)

def parse_reminder_file(file_path):
    """Parse a reminder markdown file and extract frontmatter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return frontmatter, body
    
    return None, content

def get_reminders(category=None):
    """Get all reminder files from work and/or private folders"""
    reminders = []
    
    categories = ['work', 'private'] if category is None else [category]
    
    for cat in categories:
        reminder_dir = REPO_ROOT / cat / 'reminders'
        if reminder_dir.exists():
            for file_path in reminder_dir.glob('*.md'):
                if file_path.name == 'README.md':
                    continue
                frontmatter, body = parse_reminder_file(file_path)
                if frontmatter and frontmatter.get('status') == 'pending':
                    reminders.append({
                        'path': file_path,
                        'frontmatter': frontmatter,
                        'body': body,
                        'category': cat
                    })
    
    return reminders

def check_event_exists(service, calendar_id, title, due_date):
    """Check if an event with the same title already exists on the due date"""
    try:
        # Search for events on the due date
        time_min = due_date.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        time_max = due_date.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            q=title,  # Search by title
            singleEvents=True
        ).execute()
        
        events = events_result.get('items', [])
        
        # Check if any event has the exact title we're looking for
        for event in events:
            if event.get('summary') == f"📌 {title}":
                return True
        
        return False
    except Exception as e:
        print(f"⚠️  Error checking for existing event: {e}")
        return False

def create_calendar_event(service, reminder, config=None):
    """Create a Google Calendar event from a reminder"""
    frontmatter = reminder['frontmatter']
    category = reminder['category']
    
    # Get the appropriate calendar for this category
    calendar_id = get_calendar_id_for_category(category, config)
    calendar_name = config.get('calendars', {}).get(
        config.get('category_mapping', {}).get(category, 'primary'), {}
    ).get('name', calendar_id) if config else calendar_id
    
    # Get title from frontmatter or filename
    title = frontmatter.get('title', reminder['path'].stem.replace('-', ' ').title())
    
    # Get due date
    due_date = frontmatter.get('due')
    if not due_date:
        print(f"⚠️  Skipping {reminder['path'].name} - no due date")
        return None
    
    # Parse due date
    try:
        if isinstance(due_date, str):
            due_dt = datetime.strptime(due_date, '%Y-%m-%d')
        else:
            due_dt = datetime.combine(due_date, datetime.min.time())
    except:
        print(f"⚠️  Skipping {reminder['path'].name} - invalid due date: {due_date}")
        return None
    
    # Check if event already exists
    if check_event_exists(service, calendar_id, title, due_dt):
        print(f"⏭️  Skipped '{title}' - already exists in calendar")
        return None
    
    # Get timezone from config
    timezone = config.get('defaults', {}).get('timezone', 'Europe/Amsterdam') if config else 'Europe/Amsterdam'
    
    # Set reminder time - check for custom due_time field first
    due_time = frontmatter.get('due_time')
    if due_time:
        # Parse custom time (e.g., "20:00")
        time_parts = due_time.split(':')
        hour = int(time_parts[0])
        minute = int(time_parts[1]) if len(time_parts) > 1 else 0
        due_dt = due_dt.replace(hour=hour, minute=minute)
    else:
        # Default: Set reminder time based on priority
        priority = frontmatter.get('priority', 'medium')
        if priority == 'critical':
            due_dt = due_dt.replace(hour=9, minute=0)  # 9 AM
        elif priority == 'high':
            due_dt = due_dt.replace(hour=10, minute=0)  # 10 AM
        else:
            due_dt = due_dt.replace(hour=12, minute=0)  # Noon
    
    # Set event duration - check for custom duration_minutes field
    duration_minutes = frontmatter.get('duration_minutes', 60)  # Default 1 hour
    end_dt = due_dt + timedelta(minutes=duration_minutes)
    
    # Set reminder notifications - check for custom reminder_minutes_before field
    reminder_minutes_before = frontmatter.get('reminder_minutes_before')
    if reminder_minutes_before:
        reminder_overrides = [{'method': 'popup', 'minutes': reminder_minutes_before}]
    else:
        reminder_overrides = [
            {'method': 'popup', 'minutes': 24 * 60},  # 1 day before
            {'method': 'popup', 'minutes': 60},        # 1 hour before
        ]
    
    # Set color - check for custom calendar_color field
    calendar_color = frontmatter.get('calendar_color', '').lower()
    color_map = {
        'red': '11',
        'orange': '6',
        'yellow': '5',
        'green': '10',
        'blue': '9',
        'purple': '3',
        'gray': '8',
        'peacock': '7'
    }
    
    if calendar_color and calendar_color in color_map:
        color_id = color_map[calendar_color]
    else:
        # Default: color based on priority
        priority = frontmatter.get('priority', 'medium')
        color_id = '11' if priority == 'critical' else '9' if priority == 'high' else '7'
    
    # Prepare event
    event = {
        'summary': f"📌 {title}",
        'description': reminder['body'],
        'start': {
            'dateTime': due_dt.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': reminder_overrides,
        },
        'colorId': color_id,
    }
    
    # Add tags
    tags = frontmatter.get('tags', [])
    if tags:
        event['description'] = f"Tags: {', '.join(tags)}\n\n{event['description']}"
    
    # Create event
    try:
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"✅ Created event for '{title}' in {calendar_name}")
        return created_event
    except Exception as e:
        print(f"❌ Error creating event: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Sync reminders to Google Calendar')
    
    parser.add_argument('--category', choices=['work', 'private'], 
                       help='Sync only specific category')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be synced without creating events')
    
    args = parser.parse_args()
    
    print("📅 Sync Reminders to Google Calendar")
    print("=" * 50)
    print()
    
    # Load config
    config = load_config()
    
    if config:
        print("📋 Calendar Mapping:")
        for category, calendar_key in config.get('category_mapping', {}).items():
            calendar_name = config.get('calendars', {}).get(calendar_key, {}).get('name', calendar_key)
            print(f"   {category} → {calendar_name}")
        print()
    
    # Get calendar service
    service = get_calendar_service()
    if not service:
        return
    
    # Get reminders
    reminders = get_reminders(args.category)
    print(f"📋 Found {len(reminders)} pending reminder(s)\n")
    
    if not reminders:
        print("📭 No pending reminders to sync")
        return
    
    # Process each reminder
    created_count = 0
    for reminder in reminders:
        frontmatter = reminder['frontmatter']
        category = reminder['category']
        title = frontmatter.get('title', reminder['path'].stem.replace('-', ' ').title())
        due = frontmatter.get('due', 'No due date')
        priority = frontmatter.get('priority', 'medium')
        
        # Get target calendar
        calendar_id = get_calendar_id_for_category(category, config)
        calendar_name = config.get('calendars', {}).get(
            config.get('category_mapping', {}).get(category, 'primary'), {}
        ).get('name', calendar_id) if config else calendar_id
        
        print(f"{'[DRY RUN] ' if args.dry_run else ''}Creating: {title}")
        print(f"          Category: {category} → {calendar_name}")
        print(f"          Due: {due} | Priority: {priority}")
        
        if not args.dry_run:
            event = create_calendar_event(service, reminder, config)
            if event:
                created_count += 1
                print(f"          ✅ Created: {event.get('htmlLink')}")
        
        print()
    
    if not args.dry_run:
        print(f"🎉 Successfully created {created_count}/{len(reminders)} event(s)!")
    else:
        print(f"🔍 Would create {len(reminders)} event(s)")
        print("\nRun without --dry-run to actually create events")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
