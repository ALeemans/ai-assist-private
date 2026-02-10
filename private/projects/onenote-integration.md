---
type: project
category: private
status: planning
priority: medium
created: 2026-02-01
updated: 2026-02-01
author: Anne Leemans in collaboration with Claude Sonnet 4.5
tags: [integration, onenote, microsoft-graph, api, mobile-notes]
---

# OneNote Integration for Mobile Note Capture

## 📋 Overview

Build an integration with Microsoft OneNote using Microsoft Graph API to enable quick note capture on mobile phone. Notes captured in OneNote will be automatically imported into the ai-assist repository, allowing seamless transfer of thoughts and ideas from mobile to the knowledge base.

## 🎯 Goals

- [ ] Set up Microsoft Graph API authentication for personal Microsoft account
- [ ] Create script to read OneNote pages from a designated notebook
- [ ] Parse OneNote content into markdown format
- [ ] Automatically organize notes into appropriate folders (inbox/thoughts/reminders)
- [ ] Handle note cleanup/archiving in OneNote after import
- [ ] Test end-to-end workflow from mobile to repository

## 📝 Notes

### Current Status

Project initiated. Need to start with Microsoft Graph API setup and authentication flow for personal Microsoft account.

### Next Actions

- [ ] Research Microsoft Graph API authentication for personal accounts
- [ ] Create app registration in Microsoft Azure Portal
- [ ] Set up OAuth2 authentication flow
- [ ] Create initial script to connect to OneNote
- [ ] Design OneNote notebook structure for quick capture
- [ ] Build parser to convert OneNote content to markdown
- [ ] Create integration folder structure similar to google-calendar
- [ ] Write documentation and setup guide

### Ideas & Thoughts

**Workflow Design:**
1. User captures quick notes in designated OneNote notebook on phone
2. Each page or section represents a thought/reminder/note
3. Script runs on-demand or on schedule to fetch new notes
4. Content is parsed and converted to markdown
5. Files are created in appropriate folders based on tags/keywords
6. Processed notes are either deleted or moved to "Imported" section in OneNote

**Potential Notebook Structure:**
- "AI Assist Inbox" notebook
  - Quick Thoughts (general ideas → inbox/)
  - Work Notes (work-related → work/thoughts/)
  - Reminders (actionable items → reminders/)
  - Projects (project-related notes)

**Technical Considerations:**
- Use Microsoft Graph API with delegated permissions
- Store credentials securely (similar to Google Calendar integration)
- Handle authentication token refresh
- Parse OneNote's HTML/XML format to clean markdown
- Detect note type from keywords or tags

### Resources

- [Microsoft Graph API Documentation](https://learn.microsoft.com/en-us/graph/)
- [OneNote API Reference](https://learn.microsoft.com/en-us/graph/api/resources/onenote)
- [Microsoft Graph Python SDK](https://github.com/microsoftgraph/msgraph-sdk-python)
- [Azure App Registration](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade)

## 📅 Timeline

- **Start Date**: 2026-02-01
- **Target Completion**: 2026-02-15
- **Actual Completion**: 

## 🔗 Related

- Google Calendar integration (similar authentication pattern)
- Templates in `templates/` folder
- Inbox folder structure
