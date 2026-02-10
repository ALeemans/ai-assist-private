"""
List all your Google Calendars
Shows calendar names and IDs
"""

from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / 'token.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    if not TOKEN_FILE.exists():
        print("❌ Not authenticated. Run setup-google-calendar.py first")
        return
    
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    
    print("📅 Your Google Calendars")
    print("=" * 70)
    print()
    
    try:
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])
        
        if not calendars:
            print("No calendars found")
            return
        
        for i, calendar in enumerate(calendars, 1):
            name = calendar['summary']
            cal_id = calendar['id']
            is_primary = ' ⭐ PRIMARY' if calendar.get('primary') else ''
            color = calendar.get('backgroundColor', '')
            
            print(f"[{i}] {name}{is_primary}")
            print(f"    ID: {cal_id}")
            if color:
                print(f"    Color: {color}")
            print()
        
        print("=" * 70)
        print()
        print("💡 To use a specific calendar:")
        print("   python sync-reminders-to-calendar.py --calendar 'Calendar Name'")
        print("   or")
        print("   python sync-reminders-to-calendar.py --calendar 'calendar-id@example.com'")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
