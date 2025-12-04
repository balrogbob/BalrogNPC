# Documentation Viewer Guide

**Built-in documentation browser with GitHub-style rendering**

---

## Overview

BalrogNPC includes a **built-in documentation viewer** that lets you browse all documentation without leaving the editor. No need for external browsers or markdown editors!

### Features

✅ **Full Markdown Rendering** - Headers, lists, code blocks, tables  
✅ **Document Navigation** - Back/Forward buttons, document selector  
✅ **Table of Contents** - Sidebar with clickable headings  
✅ **Search** - Find text within documents  
✅ **Clickable Links** - Jump between documents instantly  
✅ **Syntax Highlighting** - Code blocks properly formatted  
✅ **Clean Layout** - GitHub-style readable design  

---

## Opening the Viewer

### Method 1: Keyboard Shortcut (Fastest)
```
Press F1
```

### Method 2: Menu
1. Click **Help** menu
2. Select **View Documentation**

The viewer opens in a new window centered on the main editor.

---

## Navigation

### Document Selector
- **Dropdown** at top - Lists all available documents
- Click to switch between documents
- Updates title and content instantly

### Back/Forward Buttons
- **◀ Back** - Go to previous document in history
- **Forward ▶** - Return to next document
- Buttons enable/disable based on history

### Table of Contents (Sidebar)
- Shows document headings (H1, H2, H3)
- Click any heading to jump to that section
- Automatically updates when switching documents

---

## Search

### Finding Text
1. Enter search term in **Search** field
2. Click **Find** (or press Enter)
3. All matches are highlighted in yellow
4. View scrolls to first match

### Search Features
- **Case-insensitive** - Finds "NPC", "npc", "Npc"
- **Highlights all** - See every occurrence at once
- **Status message** - Shows number of matches found

**Example:**
```
Search: "wizard"
Result: "Found 8 occurrence(s) of 'wizard'"
```

---

## Document Links

### Internal Links (Between Docs)
Click any markdown link to another document:

**Example in INDEX.md:**
```markdown
[Getting Started Guide](GETTING_STARTED.md)
```

Clicking this link:
1. Loads GETTING_STARTED.md
2. Adds to navigation history
3. Updates TOC and title

### External Links
External URLs show info dialog:
```
External link: https://rathena.org
Open this in your web browser.
```

---

## Markdown Rendering

### Supported Elements

#### Headers
```markdown
# H1 Header
## H2 Header
### H3 Header
```
Rendered with proper font sizes and spacing.

#### Text Formatting
```markdown
**Bold text**
*Italic text*
`Inline code`
```

#### Code Blocks
```markdown
```python
def example():
    print("Code block")
```
```

Rendered with:
- Monospace font (Courier New)
- Gray background
- Proper indentation

#### Lists
```markdown
- Item 1
- Item 2
  - Nested item
```

Rendered with bullets and indentation.

#### Tables
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

Rendered with:
- Bold headers
- Proper alignment
- Separator lines

#### Blockquotes
```markdown
> This is a quote
```

Rendered with:
- Gray color
- Left border
- Background shading

#### Horizontal Rules
```markdown
---
```

Rendered as visual separator line.

#### Links
```markdown
[Link text](URL)
[Another Doc](OTHER_DOC.md)
```

Rendered as:
- Blue, underlined text
- Clickable
- Hover changes cursor

---

## Keyboard Shortcuts in Viewer

| Key | Action |
|-----|--------|
| `Enter` (in search) | Find text |
| `Escape` | Close viewer window |

---

## Tips & Tricks

### Tip 1: Quick Access
Press **F1** anytime to open docs - fastest way to look up commands!

### Tip 2: Link Hopping
Use internal links to navigate related topics:
1. Start at INDEX.md
2. Click topic links
3. Use Back button to return

### Tip 3: Search Everything
Search for specific commands:
- "mes" - Find message examples
- "getitem" - Find item commands
- "if" - Find conditional examples

### Tip 4: Keep Open
Leave viewer open while coding:
- Viewer is separate window
- Reference while editing
- Quick F1 to focus

### Tip 5: TOC Navigation
Use sidebar to jump to sections:
- See document structure
- Skip to relevant part
- No scrolling needed

---

## Available Documents

### All Documents Accessible

The viewer loads from the `docs/` folder:

**Getting Started**
- INDEX.md - Complete documentation index
- GETTING_STARTED.md - Installation & first steps
- USER_GUIDE.md - Full editor guide
- KEYBOARD_SHORTCUTS.md - All shortcuts

**rAthena Scripting**
- RATHENA_SCRIPT_GUIDE.md - 9-chapter complete guide
- QUICK_REFERENCE.md - Command reference
- SCRIPT_EXAMPLES.md - Working examples

**Tools & Features**
- NPC_WIZARD.md
- DIALOG_BUILDER.md
- FUNCTION_CREATOR.md
- SCRIPT_VALIDATOR.md
- YAML_VALIDATOR.md
- QUICK_NPC_TEMPLATES.md

**Advanced**
- SYNTAX_HIGHLIGHTING.md
- TROUBLESHOOTING.md
- FAQ.md

---

## Customization

### Window Size
Default: 900x700 pixels

The window remembers position during session (within the app run).

### Text Display
- **Font:** Arial 10pt (body), Courier New 9pt (code)
- **Colors:** GitHub-inspired theme
- **Spacing:** Optimized for readability

---

## Technical Details

### Markdown Parser
- Custom lightweight parser
- Handles most common markdown
- Inline formatting (bold, italic, code)
- Block elements (headers, lists, tables)

### Rendering Engine
- Tkinter Text widget with custom tags
- Tag-based styling for each element
- Clickable link regions
- Search highlighting overlay

### Performance
- Instant document loading
- Fast rendering (even large docs)
- Smooth scrolling
- Low memory footprint

---

## Troubleshooting

### Issue: Window doesn't open
**Cause:** tkinter not installed  
**Solution:** Reinstall Python with tkinter

### Issue: Documents not found
**Cause:** docs/ folder missing  
**Solution:** Ensure docs/ folder exists in BalrogNPC directory

### Issue: Links don't work
**Cause:** Target document not found  
**Solution:** Check filename (case-sensitive on some systems)

### Issue: Formatting looks wrong
**Cause:** Complex markdown syntax  
**Solution:** Viewer supports common markdown; advanced features may render as plain text

---

## Comparison: Built-in vs External

### Built-in Viewer (F1)
✅ Instant access  
✅ No browser needed  
✅ Integrated navigation  
✅ Stay in workflow  
✅ Document links work  

### External Browser
✅ Full markdown support  
✅ Images/videos  
✅ External link navigation  
⚠️ Need to open manually  
⚠️ Context switching  

**Recommendation:** Use built-in viewer for quick reference, browser for deep reading.

---

## Examples

### Example 1: Look Up Command
You forget `mes` syntax:
1. Press **F1**
2. Select **QUICK_REFERENCE.md**
3. Search: "mes"
4. Find: `mes "text";`

**Time saved:** 30 seconds vs opening browser

### Example 2: Follow Tutorial
Learn dialog building:
1. Press **F1**
2. Open **INDEX.md**
3. Click **[Dialog Builder Guide](DIALOG_BUILDER.md)**
4. Follow step-by-step
5. Use **Back** to return to index

**Result:** Seamless learning flow

### Example 3: Debug Error
Script validation fails:
1. Press **F1**
2. Open **TROUBLESHOOTING.md**
3. Search error message
4. Find solution
5. Close viewer, apply fix

**Result:** Fast problem solving

---

## Best Practices

### Do:
✅ Keep viewer open for reference  
✅ Use F1 for quick access  
✅ Search before browsing full docs  
✅ Follow links between related topics  
✅ Use TOC to navigate large documents  

### Don't:
❌ Close viewer after every lookup (keep it open!)  
❌ Read entire docs sequentially (use search/TOC)  
❌ Ignore internal links (they save time)  

---

## Future Enhancements

Planned features:
- Bookmark favorite sections
- Recent documents list
- Advanced search (regex)
- Export to PDF
- Custom themes
- Image support

---

## Summary

The **built-in documentation viewer** provides instant access to all BalrogNPC documentation:

- Press **F1** anytime
- Browse, search, navigate
- GitHub-style rendering
- No external tools needed

**Master this feature to become a more productive scripter!** 📖✨

---

**Press F1 now to try it!**
