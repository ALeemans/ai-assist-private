# Joplin Integration Setup Guide

Complete guide to set up Joplin with Infomaniak sync and enable API access for the ai-assist repository.

## Prerequisites

- Infomaniak account with kDrive access
- Smartphone (Android/iOS)
- Desktop computer with Python environment

## Step 1: Install Joplin

### Desktop (Windows)
1. Download Joplin from https://joplinapp.org/download/
2. Run the installer
3. Launch Joplin

### Mobile (Android/iOS)
1. Open Google Play Store or Apple App Store
2. Search for "Joplin"
3. Install and open the app

## Step 2: Configure Infomaniak WebDAV Sync

### On Desktop Joplin:
1. Open Joplin
2. Go to **Tools → Options → Synchronisation**
3. Set **Synchronisation target** to "WebDAV"
4. Enter Infomaniak WebDAV details:
   - **WebDAV URL**: `https://connect.drive.infomaniak.com`
   - **WebDAV username**: Your Infomaniak email
   - **WebDAV password**: Your Infomaniak password
5. Click **Check synchronisation configuration** to test
6. Click **Apply** and **OK**
7. Click **Synchronise** button to perform first sync

### On Mobile Joplin:
1. Open Joplin app
2. Tap **☰ Menu → Configuration → Synchronisation**
3. Set **Synchronisation target** to "WebDAV"
4. Enter the same Infomaniak WebDAV details as desktop
5. Tap **Check configuration** to test
6. Tap **Synchronise** to perform first sync

**Note**: Initial sync may take a few minutes. Both devices should now see the same notebooks and notes.

## Step 3: Enable Joplin Web Clipper API

The Web Clipper Service provides the REST API we'll use for automation.

### On Desktop Joplin:
1. Go to **Tools → Options → Web Clipper**
2. **Enable Web Clipper Service** (checkbox)
3. Note the **Authorization token** (copy this!)
4. Default port is **41184** (keep as-is)
5. Click **Apply** and **OK**

**Important**: Save the authorization token - you'll need it for the configuration.

## Step 4: Create AI Assist Inbox Notebook

### On Joplin (Desktop or Mobile):
1. Click/tap **New notebook** button
2. Name it: **AI Assist Inbox**
3. This is where you'll capture quick notes on your phone

Optional: Create these tags for automatic routing:
- `quick-thought` - General ideas
- `work-note` - Work-related thoughts
- `private-note` - Personal thoughts
- `work-reminder` - Work reminders
- `private-reminder` - Personal reminders

## Step 5: Configure ai-assist Integration

1. Open `integrations/joplin/config.yaml`
2. Replace `YOUR_TOKEN_HERE` with your authorization token from Step 3
3. Verify other settings match your preferences

```yaml
api_token: "paste_your_actual_token_here"
inbox_notebook: "AI Assist Inbox"
```

## Step 6: Test the Connection

Run the test script to verify everything is working:

```powershell
& D:/HogeschoolUtrecht/GithubRepos/ai-assist/.venv/Scripts/python.exe integrations/joplin/test-connection.py
```

You should see:
- ✅ Connection successful
- List of your notebooks
- List of notes in "AI Assist Inbox"

## Step 7: Import Notes

Run the import script manually or on-demand:

```powershell
& D:/HogeschoolUtrecht/GithubRepos/ai-assist/.venv/Scripts/python.exe integrations/joplin/import-notes.py
```

## Usage Workflow

1. **Capture** - Write quick note in Joplin mobile app (in "AI Assist Inbox" notebook)
2. **Tag** - Add tag like `#quick-thought` or `#work-reminder`
3. **Sync** - Joplin automatically syncs via Infomaniak
4. **Import** - Run import script when you start ai-assist session
5. **Organize** - Notes automatically organized into folders based on tags

## Troubleshooting

### Sync not working
- Check Infomaniak credentials
- Ensure both devices are connected to internet
- Try manual sync (Synchronise button/menu)

### API connection fails
- Ensure desktop Joplin is running
- Verify Web Clipper Service is enabled
- Check token in config.yaml matches Joplin settings
- Verify port 41184 is not blocked by firewall

### Notes not importing
- Check notebook name matches exactly ("AI Assist Inbox")
- Ensure notes are synced to desktop
- Verify tags are spelled correctly

## Security Notes

- **API Token**: Keep `config.yaml` secure - contains sensitive token
- **Encryption**: Joplin supports E2EE - enable in sync settings if desired
- **Infomaniak**: Data stored in Switzerland with strong privacy laws
- Never commit your actual token to git (add config.yaml to .gitignore if needed)

## Resources

- [Joplin Documentation](https://joplinapp.org/help/)
- [Joplin API Reference](https://joplinapp.org/api/references/rest_api/)
- [Infomaniak Support](https://www.infomaniak.com/en/support)
