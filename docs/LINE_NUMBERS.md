# Line Numbers & Navigation

**Line-based navigation and reference tools**

---

## Overview

BalrogNPC displays line numbers on the left side of the editor, making it easy to navigate large files and reference specific locations.

---

## Line Number Display

### Always Visible

Line numbers are **always shown** on the left side of the editor:

```
1  prontera,150,150,4	script	MyNPC	111,{
2      mes "Hello!";
3      close;
4  }
```

---

### What Line Numbers Show

- **Current line count** - Total lines in document
- **Line references** - For error messages
- **Code organization** - Visual structure
- **Navigation aid** - Jump to specific lines

---

### Auto-Update

Line numbers update automatically as you:
- Add lines (typing, pasting)
- Delete lines
- Insert blank lines

---

## Go To Line

### Quick Navigation

**Jump to any line number instantly**

- **Shortcut:** `Ctrl+G`
- **Menu:** Edit → Go To Line

---

### Using Go To Line

**Workflow:**
1. Press `Ctrl+G`
2. Dialog appears: "Go to line:"
3. Enter line number
4. Press OK (or Enter)
5. Cursor jumps to that line
6. Line is highlighted

**Example:**
```
Error message: "Syntax error at line 47"
Action: Press Ctrl+G, enter 47, jump to error
```

---

### When to Use

**Error messages:**
```
Script validator: "Missing semicolon at line 23"
→ Ctrl+G, enter 23, find and fix
```

**Code reviews:**
```
Teammate: "Check the logic at line 100"
→ Ctrl+G, enter 100, review code
```

**Large files:**
```
Need to edit NPC at line 500 in 1000-line file
→ Ctrl+G, enter 500, instant navigation
```

---

## Line-Based Editing

### Current Line Reference

**See current line number:**
- Look at line numbers on left
- Cursor position shows current line

**Example:**
```
Cursor on line 15
Line number "15" is highlighted or bolded
```

---

### Multi-Line Selection

**Select multiple lines:**

1. Click at start line
2. Hold Shift
3. Click at end line
4. All lines selected

**Or use keyboard:**
1. Position cursor
2. Hold Shift
3. Press ↓ (down arrow) repeatedly
4. Lines select as you move

---

### Delete Entire Line

**Remove complete line:**

1. Position cursor on line
2. Select All (`Ctrl+A` on that line)
3. Press Delete or Backspace

**Or:**
1. Click at line start
2. Hold Shift
3. Press End (selects line)
4. Press Delete

---

## Navigation Techniques

### Scroll to Top

**Go to first line:**
- Press `Ctrl+Home`
- Or: Ctrl+G, enter 1

---

### Scroll to Bottom

**Go to last line:**
- Press `Ctrl+End`
- Or: Scroll down

---

### Page Up/Down

**Move by screen:**
- **Page Up** - Scroll up one screen
- **Page Down** - Scroll down one screen

---

### Arrow Keys

**Move by line/character:**
- **↑/↓** - Previous/next line
- **←/→** - Previous/next character
- **Ctrl+←/→** - Previous/next word

---

## Line Number Uses

### Use 1: Error Location

**Script validator shows:**
```
Line 47: Missing semicolon
Line 52: Unbalanced brackets
```

**Action:**
- Ctrl+G → 47 → Fix
- Ctrl+G → 52 → Fix

---

### Use 2: Code Organization

**Visual structure:**
```
Lines 1-10:   Header comments
Lines 11-50:  Main NPC
Lines 51-80:  Helper function
Lines 81-100: OnInit handler
```

You can see at a glance where each section is.

---

### Use 3: Collaboration

**Team communication:**
```
Dev 1: "I changed the dialog at line 35"
Dev 2: Ctrl+G → 35 → See changes
```

---

### Use 4: Bookmarking

**Mental bookmarks:**
```
"The item check is at line 120"
"Quest completion is at line 200"
Later: Ctrl+G → 120 or 200
```

---

## Best Practices

### Practice 1: Use Go To Line for Errors
When validator or server shows line numbers, use Ctrl+G immediately.

### Practice 2: Note Important Lines
Remember line numbers of key sections for quick navigation.

### Practice 3: Organize by Sections
Group related code, note line ranges for each section.

### Practice 4: Comment Line Numbers
In complex scripts, add comments with line references:
```
// Main dialog starts at line 50
// Quest logic at line 150
```

---

## Tips & Tricks

### Tip 1: Ctrl+G for Everything
Faster than scrolling through large files!

### Tip 2: Relative Line Numbers
Count from current position: "10 lines down" = current + 10.

### Tip 3: Line Numbers in Comments
```
// TODO: Fix logic at line 75
```

### Tip 4: Quick Line Count
Look at last line number to see total lines.

### Tip 5: Select Multiple Lines Fast
Click first line, Shift+Click last line.

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Go To Line | `Ctrl+G` |
| Start of line | `Home` |
| End of line | `End` |
| Start of file | `Ctrl+Home` |
| End of file | `Ctrl+End` |
| Up one line | `↑` |
| Down one line | `↓` |
| Page up | `Page Up` |
| Page down | `Page Down` |
| Select to line end | `Shift+End` |
| Select to line start | `Shift+Home` |

---

## Common Workflows

### Workflow 1: Fix Validation Error

```
1. Run script validator
2. See: "Error at line 47"
3. Press Ctrl+G
4. Enter 47
5. Fix error
6. Save (Ctrl+S)
```

---

### Workflow 2: Navigate Large Script

```
1. Open 500-line script
2. Need to edit line 300
3. Press Ctrl+G
4. Enter 300
5. Instant navigation
6. Make changes
```

---

### Workflow 3: Review Code Section

```
1. Want to review lines 100-150
2. Press Ctrl+G, enter 100
3. Read and scroll
4. Note any issues
5. Make changes as needed
```

---

## Related Features

- [Text Editor Features](TEXT_EDITOR.md) - Basic editing
- [Find & Replace](FIND_REPLACE.md) - Search functionality
- [Keyboard Shortcuts](KEYBOARD_SHORTCUTS.md) - All shortcuts

---

**Master line navigation for efficient script editing!** 🎯✨
