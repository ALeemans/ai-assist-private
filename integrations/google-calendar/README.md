# Google Calendar Integration

Scripts to sync reminders with Google Calendar.

## 🚀 Quick Setup

**See [SETUP-GUIDE.md](SETUP-GUIDE.md) for detailed step-by-step instructions!**

### Summary:

1. **Enable Google Calendar API** in Google Cloud Console
2. **Create OAuth credentials** (Desktop app)
3. **Download credentials.json** to this folder
4. **Install dependencies:** `pip install -r ../../requirements.txt`
5. **Run setup:** `python setup-google-calendar.py`

## Usage

### View Calendar Events

```powershell
# View this week
python view-events.py

# View specific date range  
python view-events.py --start 2026-02-01 --end 2026-02-07
```

### Sync Reminders to Calendar

```powershell
# Sync all pending reminders
python sync-reminders-to-calendar.py

# Sync specific category only
python sync-reminders-to-calendar.py --category work
```

## Features

- Creates calendar events from reminder files
- Uses due dates from frontmatter
- Sets reminders based on priority
- Two-way sync (optional)
