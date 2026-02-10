# Joplin Integration

Automatically import notes from Joplin into the ai-assist knowledge base.

## Overview

This integration enables quick note capture on mobile via Joplin, which syncs to desktop through Infomaniak kDrive (Swiss WebDAV), and automatically imports notes into the appropriate folders based on tags.

## Workflow

1. **Capture** - Write notes in Joplin mobile app (in "AI Assist Inbox" notebook)
2. **Tag** - Add tags like `#quick-thought`, `#work-reminder`, etc.
3. **Sync** - Notes automatically sync via Infomaniak WebDAV
4. **Import** - Run `import-notes.py` to organize notes into repository
5. **Archive** - Imported notes moved to "Imported" notebook in Joplin

## Files

- `config.yaml` - Configuration (API token, notebook names, tag mapping)
- `SETUP-GUIDE.md` - Complete setup instructions
- `test-connection.py` - Test API connection and list notebooks/notes
- `import-notes.py` - Import and organize notes from Joplin

## Quick Start

1. Follow [SETUP-GUIDE.md](SETUP-GUIDE.md) to:
   - Install Joplin on desktop and mobile
   - Configure Infomaniak WebDAV sync
   - Enable Web Clipper API
   - Get API token

2. Update `config.yaml` with your API token

3. Test connection:
   ```powershell
   & D:/HogeschoolUtrecht/GithubRepos/ai-assist/.venv/Scripts/python.exe integrations/joplin/test-connection.py
   ```

4. Import notes:
   ```powershell
   & D:/HogeschoolUtrecht/GithubRepos/ai-assist/.venv/Scripts/python.exe integrations/joplin/import-notes.py
   ```

## Tag Mapping

Tags in Joplin automatically route notes to the right folder:

- `quick-thought` → `inbox/`
- `work-note` → `work/thoughts/`
- `private-note` → `private/thoughts/`
- `work-reminder` → `work/reminders/`
- `private-reminder` → `private/reminders/`

Notes without matching tags go to `inbox/` by default.

## Security

- API runs locally (localhost:41184) - no remote access
- Data synced via Infomaniak (Swiss, GDPR compliant)
- API token stored in `config.yaml` (keep secure)
- Optional: Enable E2EE in Joplin sync settings

## Requirements

- Joplin desktop app (running)
- Python packages: `requests`, `pyyaml`
- Infomaniak kDrive account for sync
