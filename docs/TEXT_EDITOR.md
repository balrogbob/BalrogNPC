# Text Editor Features

**Complete guide to BalrogNPC's text editing capabilities**

---

## Overview

BalrogNPC provides a clean, simple text editing interface optimized for rAthena script development. All standard text editing features are available through keyboard shortcuts and menu items.

---

## Basic File Operations

### New File

**Create a new empty file**

- **Menu:** File → New
- **Shortcut:** `Ctrl+N`
- **Action:** Clears current content and starts a fresh document
- **Title updates to:** "BalrogNPC - Untitled"

**Workflow:**
1. Press `Ctrl+N`
2. Start typing your script
3. Save when ready (`Ctrl+S`)

---

### Open File

**Open an existing file from disk**

- **Menu:** File → Open
- **Shortcut:** `Ctrl+O`
- **Supported formats:**
  - `.txt` - Plain text
  - `.npc` - rAthena script files
  - `.yml`, `.yaml` - YAML database files
  - All files (`*.*`)

**Workflow:**
1. Press `Ctrl+O`
2. Browse to file location
3. Select file
4. Click "Open"
5. File content loads into editor

---

### Save File

**Save current content to disk**

- **Menu:** File → Save
- **Shortcut:** `Ctrl+S`
- **Encoding:** UTF-8

**First save (new file):**
1. Press `Ctrl+S`
2. Choose location
3. Enter filename
4. Click "Save"
5. Title bar updates with filename

**Subsequent saves:**
1. Press `Ctrl+S`
2. File saves immediately to existing location

**Best practice:** Save frequently! Press `Ctrl+S` after every significant change.

---

### Save As

**Save to a new location or filename**

- **Menu:** File → Save As
- **Use when:**
  - Creating a copy of current file
  - Changing filename
  - Moving file to different folder

---

## Text Editing

### Cut, Copy, Paste

**Standard clipboard operations**

| Operation | Shortcut | Menu |
|-----------|----------|------|
| **Cut** | `Ctrl+X` | Edit → Cut |
| **Copy** | `Ctrl+C` | Edit → Copy |
| **Paste** | `Ctrl+V` | Edit → Paste |

**Workflow:**
1. Select text (click and drag)
2. Press shortcut
3. Move cursor to destination
4. Paste (`Ctrl+V`)

---

### Undo

**Revert last change**

- **Shortcut:** `Ctrl+Z`
- **Menu:** Edit → Undo
- **Multiple levels:** Press repeatedly to undo multiple changes

**Tip:** Made a mistake? Press `Ctrl+Z` immediately!

---

### Select All

**Select entire document**

- **Shortcut:** `Ctrl+A`
- **Menu:** Edit → Select All
- **Use for:**
  - Copying entire script
  - Replacing all content
  - Deleting everything

---

### Delete Selection

**Remove selected text**

- **Menu:** Edit → Delete
- **Keyboard:** `Delete` key
- **Also works:** `Backspace` key

---

## View Options

### Word Wrap

**Toggle line wrapping**

- **Menu:** Format → Word Wrap
- **When enabled:**
  - Long lines wrap to window width
  - No horizontal scrolling needed
  - Easier to read long dialog strings

- **When disabled:**
  - Lines extend horizontally
  - Horizontal scrollbar appears
  - See full line structure

**Recommendation:** Enable for NPCs with long dialog, disable for structured code.

---

### Font Size

**Adjust text size**

- **Menu:** Format → Font...
- **Options:** Slider from 6 to 24 points
- **Default:** 10 points

**Workflow:**
1. Click Format → Font...
2. Drag slider to desired size
3. Click OK
4. Editor updates immediately

**Common sizes:**
- 8-9: Small, fit more on screen
- 10-11: Default, comfortable
- 12-14: Larger, easier on eyes
- 16+: Presentation mode

---

## Navigation Features

### Line Numbers

**Line numbers display on left side**

- Always visible
- Auto-updates as you type
- Helps with:
  - Error messages (references line numbers)
  - Navigation to specific lines
  - Code organization

See [Line Numbers & Navigation](LINE_NUMBERS.md) for more.

---

### Go To Line

**Jump to specific line number**

- **Shortcut:** `Ctrl+G`
- **Menu:** Edit → Go To Line

**Workflow:**
1. Press `Ctrl+G`
2. Enter line number
3. Press OK
4. Cursor jumps to that line

**Use when:**
- Error message references line number
- Navigating large files
- Jumping to specific NPC

See [Line Numbers & Navigation](LINE_NUMBERS.md) for more.

---

### Find & Replace

**Search and replace text**

- **Shortcut:** `Ctrl+F`
- **Menu:** Edit → Find & Replace

**Features:**
- Find Next/Previous
- Replace Next/All
- Case sensitive option
- Whole word matching
- Regular expressions
- Highlight all matches

See [Find & Replace](FIND_REPLACE.md) for complete guide.

---

## Best Practices

### Save Frequently
✅ Press `Ctrl+S` every few minutes  
✅ Save before testing scripts  
✅ Save before using rAthena Tools  

### Use Undo Liberally
✅ Experiment with changes  
✅ Press `Ctrl+Z` if something breaks  
✅ Multiple levels available  

### Enable Word Wrap for Dialogs
✅ Long NPC messages easier to read  
✅ Disable for code structure  

### Adjust Font for Comfort
✅ Find size that's comfortable  
✅ Change based on task (coding vs reviewing)  

---

## Keyboard Shortcuts Summary

| Action | Shortcut |
|--------|----------|
| New file | `Ctrl+N` |
| Open file | `Ctrl+O` |
| Save file | `Ctrl+S` |
| Cut | `Ctrl+X` |
| Copy | `Ctrl+C` |
| Paste | `Ctrl+V` |
| Undo | `Ctrl+Z` |
| Select All | `Ctrl+A` |
| Find & Replace | `Ctrl+F` |
| Go To Line | `Ctrl+G` |

See [Keyboard Shortcuts](KEYBOARD_SHORTCUTS.md) for complete list.

---

## Tips & Tricks

### Tip 1: Save Often
Use `Ctrl+S` like a reflex. Save after every few changes!

### Tip 2: Multiple Instances
Need to edit multiple files? Launch BalrogNPC multiple times.

### Tip 3: Word Wrap Toggle
Toggle word wrap on/off to see code structure clearly.

### Tip 4: Font Size for Task
- Coding: 10-11pt
- Reading: 12-14pt
- Presenting: 16+pt

### Tip 5: Use Go To Line
Error at line 47? Press `Ctrl+G`, enter 47, go there instantly.

---

## Related Features

- [Find & Replace](FIND_REPLACE.md) - Advanced search
- [Line Numbers & Navigation](LINE_NUMBERS.md) - Navigation tools
- [Keyboard Shortcuts](KEYBOARD_SHORTCUTS.md) - All shortcuts
- [Syntax Highlighting](SYNTAX_HIGHLIGHTING.md) - Color coding

---

**Master these basics to become a productive BalrogNPC user!** ⌨️✨
