"""
Setup Google Calendar authentication
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying scopes, delete token.json
SCOPES = ['https://www.googleapis.com/auth/calendar']

SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_FILE = SCRIPT_DIR / 'credentials.json'
TOKEN_FILE = SCRIPT_DIR / 'token.json'

def main():
    print("📅 Google Calendar Setup for AI-Assist")
    print("=" * 50)
    print()
    
    # Check for credentials file
    if not CREDENTIALS_FILE.exists():
        print("❌ credentials.json not found!")
        print()
        print("Please follow these steps:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create a new project")
        print("3. Enable Google Calendar API")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download credentials.json to this folder")
        print()
        print("See SETUP-GUIDE.md for detailed instructions")
        return
    
    print(f"✅ Found credentials.json")
    print()
    
    creds = None
    
    # Load existing token if available
    if TOKEN_FILE.exists():
        print("📌 Found existing token.json")
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🔐 Starting authentication flow...")
            print()
            print("⚠️  A browser window will open")
            print("   Please login to your Google account and approve access")
            print()
            print("💡 If you see 'Google hasn't verified this app':")
            print("   Click 'Advanced' → 'Go to AI-Assist (unsafe)'")
            print("   (It's safe - it's your own app!)")
            print()
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        print("💾 Saving token...")
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    print("✅ Authentication successful!")
    print()
    
    # Test connection
    print("🧪 Testing connection to Google Calendar...")
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        # Get calendar list
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])
        
        print(f"✅ Connected! Found {len(calendars)} calendar(s):")
        print()
        
        for calendar in calendars[:5]:  # Show first 5
            name = calendar['summary']
            is_primary = ' (PRIMARY)' if calendar.get('primary') else ''
            print(f"   📅 {name}{is_primary}")
        
        if len(calendars) > 5:
            print(f"   ... and {len(calendars) - 5} more")
        
        print()
        print("🎉 Setup complete!")
        print()
        print("You can now use:")
        print("  - python view-events.py")
        print("  - python sync-reminders-to-calendar.py")
        print("  - python sync-to-daily-log.py")
        
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        print()
        print("Try deleting token.json and running setup again")

if __name__ == '__main__':
    main()

