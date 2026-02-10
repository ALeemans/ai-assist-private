---
type: reminder
category: private
status: cancelled
priority: medium
created: 2026-02-01
due: 2026-02-02
updated: 2026-02-02
tags: [integration, joplin, api, setup, privacy]
---

# Set Up Joplin Integration

## 📌 What

Begin setting up Joplin notes app with REST API integration to enable mobile note capture and automatic import into the ai-assist repository.

## ❓ Why

This will allow quick capture of thoughts and ideas on mobile phone using Joplin (open-source, privacy-focused), which will then be automatically organized into the knowledge base. Switched from OneNote to align with European/privacy-focused tech migration.

## ✅ Completion Criteria

- [x] Install Joplin on desktop
- [x] Install Joplin on mobile
- [ ] Set up European sync solution (Infomaniak Nextcloud)
- [ ] Enable Joplin Web Clipper API and get token
- [ ] Test basic API connection

## 📝 Notes

First step in the Joplin integration project. Joplin has a local REST API (localhost:41184) that runs when the app is open. Notes are already in markdown format, making import easier than OneNote.

**Advantages over OneNote:**
- Open source, no vendor lock-in
- Local API, no cloud authentication needed
- Already markdown (no conversion)
- European sync options
- End-to-end encryption support

## 🔗 Related

- Project: [joplin-integration.md](../projects/joplin-integration.md)
- Project: [european-cloud-migration.md](../projects/european-cloud-migration.md)
- Reference: Google Calendar integration setup
