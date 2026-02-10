# AI-Assist: Your Second Brain Repository 🧠

Welcome to your personal knowledge management and task tracking system! This repository serves as the central hub for all your thoughts, ideas, projects, and reminders.

## 🚀 Quick Start (Morning Routine)

1. Open this workspace in VS Code
2. Check `inbox/` for unsorted items
3. Review `daily-logs/` for today's entry
4. Check `work/reminders/` and `private/reminders/` for pending tasks

## 📁 Structure Overview

```
work/          → Work-related content
private/       → Personal content  
inbox/         → Quick capture (sort later)
daily-logs/    → Daily journal entries
integrations/  → External tool connections
templates/     → File templates for consistency
```

## 🎯 How to Use

### Capture a Quick Thought
1. Create a new file in `inbox/`
2. Later, move to appropriate folder (work/thoughts or private/thoughts)

### Start a New Project
1. Copy `templates/project.md`
2. Save to `work/projects/` or `private/projects/`
3. Fill in the details

### Add a Reminder
1. Copy `templates/reminder.md`
2. Save to `work/reminders/` or `private/reminders/`
3. Set priority and due date

### Daily Log
- Each workday, create or update today's log in `daily-logs/YYYY/MM/`
- Use `templates/daily-log.md` as starting point

## 🔗 Integrations

- **Azure DevOps**: Scripts in `integrations/devops/` to create work items
- **Google Calendar**: Sync reminders with `integrations/google-calendar/`

## 💡 Tips

- Use frontmatter (YAML) for metadata (tags, dates, priority)
- GitHub Copilot learns from your entries to provide better context
- Keep files organized by moving from inbox to proper folders
- Update project status regularly

---

*Last updated: 2026-01-30*
