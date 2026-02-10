# Azure DevOps Integration

Scripts to connect with Azure DevOps and create work items from your project notes.

## Available Scripts

### `create_user_story.py`

Creates user stories in Azure DevOps with authentication via Azure Identity.

**Usage:**

```powershell
# Interactive mode (prompts for title and description)
python create_user_story.py

# Provide title and description directly
python create_user_story.py --title "Fix login bug" --description "Users can't login"

# Override config settings
python create_user_story.py --feature 12345 --tag "BugFix" --assigned-to "John Doe"

# Full example with all options
python create_user_story.py \
  --title "New feature" \
  --description "Detailed description here" \
  --feature 99999 \
  --iteration "DevOps DenA\Sprint 5" \
  --tag "Feature" \
  --state "New" \
  --assigned-to "Anne Leemans"
```

**Configuration:**

Edit `config.yaml` to set your defaults:
- Organization
- Project
- Default Feature ID
- Default Iteration Path
- Default Tag, State, Assigned To

All config values can be overridden via command-line arguments.

**Requirements:**
```powershell
pip install requests azure-identity pyyaml
```

## Future Enhancements

### ~~Phase 1: Dynamic Configuration~~ ✅ DONE
- [x] Move hardcoded config to external config file (YAML)
- [x] Support multiple projects/features via command-line args
- [x] Allow config override per work item

### Phase 2: Project File Integration
- [ ] Read title/description from project markdown files
- [ ] Parse frontmatter metadata to set DevOps fields
- [ ] Auto-link created work items back to project files
- [ ] Bulk create from multiple project files

### Phase 3: Advanced Features
- [ ] Two-way sync: Update project status from DevOps state
- [ ] Create user stories from project goals section
- [ ] Link reminders to DevOps tasks
- [ ] Generate acceptance criteria from project checklists

## Example: Future Project-to-DevOps Workflow

```powershell
# Create user story from project file
python create-from-project.py --file "..\..\work\projects\dashboard-redesign.md"

# Bulk create from all projects in planning status
python create-from-project.py --status planning --category work
```
