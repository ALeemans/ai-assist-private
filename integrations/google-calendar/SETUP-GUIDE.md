# Google Calendar Integration

Connect your Google Calendar to AI-Assist - sync reminders, view events, and more!

## Setup (5 minutes)

### Step 1: Enable Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing):
   - Click dropdown at top
   - Click "NEW PROJECT"
   - Name it "AI-Assist" or similar
   - Click "CREATE"

3. Enable Google Calendar API:
   - Go to [Enable Calendar API](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com)
   - Select your project
   - Click "ENABLE"

### Step 2: Create OAuth Credentials

1. Go to [Credentials page](https://console.cloud.google.com/apis/credentials)
2. Click "CREATE CREDENTIALS" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: `AI-Assist`
   - User support email: your email
   - Developer contact: your email
   - Click "SAVE AND CONTINUE"
   - Skip scopes (click "SAVE AND CONTINUE")
   - Add yourself as test user
   - Click "SAVE AND CONTINUE"

4. Create OAuth client:
   - Application type: **Desktop app**
   - Name: `AI-Assist Calendar`
   - Click "CREATE"

5. Download credentials:
   - Click the download icon (⬇️) next to your new credential
   - Save as `credentials.json` in this folder
   - Or click "DOWNLOAD JSON"

### Step 3: Install Dependencies

```powershell
pip install -r ../../requirements.txt
```

### Step 4: Authenticate

```powershell
python setup-google-calendar.py
```

This will:
- Open your browser
- Ask you to login to Google
- Ask to approve Calendar access
- Save token locally

**First time:** You'll see a warning "Google hasn't verified this app" - click "Advanced" → "Go to AI-Assist (unsafe)" - it's safe, it's your own app!

### Step 5: Done! 🎉

Now you can use:

```powershell
# View upcoming events
python view-events.py

# Sync reminders to Google Calendar
python sync-reminders-to-calendar.py

# Sync today's events to daily log
python sync-to-daily-log.py
```

## Available Scripts

### `view-events.py`
View your Google Calendar events in the terminal

```powershell
# View this week
python view-events.py

# View specific date range
python view-events.py --start 2026-02-01 --end 2026-02-07

# View specific calendar
python view-events.py --calendar "Work"
```

### `sync-reminders-to-calendar.py`
Create Google Calendar events from your reminder files

```powershell
# Sync all pending reminders
python sync-reminders-to-calendar.py

# Sync specific category
python sync-reminders-to-calendar.py --category work
```

### `sync-to-daily-log.py`
Pull today's calendar events into your daily log

```powershell
python sync-to-daily-log.py
```

## Troubleshooting

**"credentials.json not found"**
- Make sure you downloaded it from Google Cloud Console
- Place it in this folder (`integrations/google-calendar/`)

**"Google hasn't verified this app"**
- Normal! It's your personal app
- Click "Advanced" → "Go to AI-Assist (unsafe)"
- It's safe because you created it

**"Access denied"**
- Make sure you added yourself as a test user in OAuth consent screen
- Or publish the app (not necessary for personal use)

## Security

- Credentials stored locally in `token.json` (gitignored)
- Uses OAuth 2.0 - never stores password
- Refresh tokens auto-renew
- Only you can access your data
