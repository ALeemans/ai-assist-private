"""
View Google Calendar events
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / 'token.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Get authenticated Google Calendar service"""
    if not TOKEN_FILE.exists():
        print("❌ Not authenticated. Run setup-google-calendar.py first")
        return None
    
    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    return build('calendar', 'v3', credentials=creds)

def view_events(calendar_id='primary', start_date=None, end_date=None, max_results=20):
    """View events from Google Calendar"""
    
    service = get_calendar_service()
    if not service:
        return
    
    # Set date range
    if not start_date:
        start_date = datetime.now()
    if not end_date:
        end_date = start_date + timedelta(days=7)
    
    # Convert to RFC3339 format
    time_min = start_date.isoformat() + 'Z'
    time_max = end_date.isoformat() + 'Z'
    
    print("📅 Google Calendar Events")
    print("=" * 50)
    print(f"Calendar: {calendar_id}")
    print(f"Range: {start_date.date()} to {end_date.date()}")
    print()
    
    try:
        # Get events
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            print("📭 No events found")
            return
        
        # Display events grouped by date
        current_date = None
        
        for event in events:
            # Get start time
            start = event['start'].get('dateTime', event['start'].get('date'))
            
            # Parse datetime
            if 'T' in start:  # DateTime
                event_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                event_date = event_dt.date()
                event_time = event_dt.strftime("%H:%M")
            else:  # All-day
                event_dt = datetime.fromisoformat(start)
                event_date = event_dt.date()
                event_time = None
            
            # Print date header if changed
            if event_date != current_date:
                current_date = event_date
                print()
                day_name = event_date.strftime("%A")
                print(f"╔══ {day_name}, {event_date} ══")
            
            # Print event
            summary = event.get('summary', '(No title)')
            
            if event_time:
                print(f"║  {event_time} 📅 {summary}")
            else:
                print(f"║  All day 📅 {summary}")
            
            # Additional details
            if event.get('location'):
                print(f"║         📍 {event['location']}")
            if event.get('description'):
                desc = event['description'][:60] + "..." if len(event['description']) > 60 else event['description']
                print(f"║         💬 {desc}")
        
        print()
        print(f"\n📊 Total: {len(events)} event(s)")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='View Google Calendar events')
    
    parser.add_argument('--calendar', '-c', default='primary',
                       help='Calendar ID or name (default: primary)')
    parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    parser.add_argument('--max', type=int, default=20,
                       help='Max results (default: 20)')
    
    args = parser.parse_args()
    
    # Parse dates
    start_date = datetime.strptime(args.start, "%Y-%m-%d") if args.start else datetime.now()
    end_date = datetime.strptime(args.end, "%Y-%m-%d") if args.end else start_date + timedelta(days=7)
    
    view_events(args.calendar, start_date, end_date, args.max)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
