---
type: project
category: private
status: planning
priority: medium
created: 2026-02-01
updated: 2026-02-02
author: Anne Leemans in collaboration with Claude Sonnet 4.5
tags: [integration, joplin, api, mobile-notes, privacy, european]
---

# Joplin Integration for Mobile Note Capture

## 📋 Overview

Build an integration with Joplin using its REST API to enable quick note capture on mobile phone. Notes captured in Joplin will be automatically imported into the ai-assist repository, allowing seamless transfer of thoughts and ideas from mobile to the knowledge base.

**Why Joplin?**
- Open source, privacy-focused alternative to Microsoft OneNote
- Full REST API for automation
- End-to-end encryption support
- Cross-platform (Windows, Mac, Linux, Android, iOS)
- European sync options (Nextcloud, WebDAV, self-hosted)
- No vendor lock-in

## 🎯 Goals

- [ ] Install and set up Joplin on desktop and mobile
- [ ] Configure European sync solution (Nextcloud or WebDAV)
- [ ] Set up Joplin Web Clipper API (REST API runs on localhost:41184)
- [ ] Create script to read notes from designated notebook via API
- [ ] Parse Joplin markdown content
- [ ] Automatically organize notes into appropriate folders (inbox/thoughts/reminders)
- [ ] Handle note cleanup/archiving in Joplin after import
- [ ] Test end-to-end workflow from mobile to repository

## 📝 Notes

### Current Status

Infomaniak account created. Ready to configure Joplin sync and build API integration.

### Joplin API Overview

**Base URL**: `http://localhost:41184` (when Joplin is running)

**Authentication**: Token-based (get from Joplin > Tools > Options > Web Clipper)

**Key Endpoints**:
- `GET /notes` - List all notes
- `POST /notes` - Create note
- `GET /notes/{id}` - Get specific note (with body)
- `PUT /notes/{id}` - Update note
- `DELETE /notes/{id}` - Delete note
- `GET /folders` - List notebooks
- `GET /tags` - List tags

**Response Format**: JSON with markdown content in `body` field

### Next Actions

- [ ] Install Joplin on desktop
- [ ] Install Joplin on mobile (Android/iOS)
- [ ] Research European sync options (Nextcloud recommended)
- [ ] Set up synchronization between devices
- [ ] Enable Web Clipper API and get authentication token
- [ ] Create initial connection script to test API
- [ ] Design Joplin notebook structure for quick capture
- [ ] Build import script to fetch and process notes
- [ ] Create integration folder structure: `integrations/joplin/`
- [ ] Write documentation and setup guide

### Workflow Design

**Mobile → Desktop Flow:**
1. User captures quick notes in designated Joplin notebook on phone
2. Notes sync via Nextcloud/WebDAV to desktop Joplin
3. Script queries Joplin API for new notes in "AI Assist Inbox" notebook
4. Content is parsed (already in markdown!)
5. Files are created in appropriate folders based on tags/keywords
6. Processed notes are moved to "Imported" notebook or deleted

**Joplin Notebook Structure:**
- **"AI Assist Inbox"** notebook
  - Tag: `#quick-thought` → `inbox/`
  - Tag: `#work-note` → `work/thoughts/`
  - Tag: `#reminder` → `private/reminders/` or `work/reminders/`
  - Tag: `#project` → Append to existing project file

**Technical Advantages**:
- Notes already in markdown format (minimal parsing needed)
- Local API = fast, no cloud dependencies during import
- Can use tags for automatic categorization
- Encryption support for sensitive notes
- European sync options align with privacy goals

### Sync Options (European Focus)

**SELECTED: Infomaniak kDrive (Swiss WebDAV)**
- ✅ Swiss company (data protection)
- ✅ WebDAV support built-in
- ✅ European data centers
- ✅ Account already created

Other options:
1. **Nextcloud** 
   - European providers available
   - WebDAV + file sync
   
2. **Joplin Server** (Self-hosted)
   - Official Joplin sync server
   - Can host on European VPS

### Resources

- [Joplin Website](https://joplinapp.org/)
- [Joplin API Documentation](https://joplinapp.org/api/references/rest_api/)
- [Joplin GitHub](https://github.com/laurent22/joplin)
- [Sync Options Guide](https://joplinapp.org/help/apps/sync/)
- Python requests library for API calls

## 📅 Timeline

- **Start Date**: 2026-02-01 (originally OneNote)
- **Switched to Joplin**: 2026-02-02
- **Target Completion**: 2026-02-15
- **Actual Completion**: 

## 🔗 Related

- [European Cloud Migration](european-cloud-migration.md) - Part of moving away from US tech
- Google Calendar integration (similar API pattern)
- Templates in `templates/` folder
- Inbox folder structure
