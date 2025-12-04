# Find & Replace Guide

**Advanced search and replace functionality**

---

## Overview

BalrogNPC includes a powerful Find & Replace dialog for searching text and making batch replacements. Access it instantly with `Ctrl+F`.

---

## Opening Find & Replace

**Three ways to open:**
1. Press `Ctrl+F` (fastest)
2. Menu: Edit → Find & Replace
3. Menu: Edit → Go To Line (for line-based navigation)

---

## Find Tab

### Basic Find

**Search for text in current document**

1. Press `Ctrl+F`
2. Type search term in "Find:" field
3. Click "Find Next" (or press Enter)
4. Text is highlighted if found
5. Status shows: "Found at position X"

**Navigate results:**
- **Find Next** - Jump to next occurrence
- **Find Previous** - Jump to previous occurrence

---

### Find Options

**Case Sensitive**
- ☐ Unchecked: Finds "npc", "NPC", "Npc"
- ☑ Checked: Finds only exact case match

**Whole Word**
- ☐ Unchecked: Finds "mes" in "message"
- ☑ Checked: Finds only standalone "mes"

**Use Regex**
- ☐ Unchecked: Literal text search
- ☑ Checked: Regular expression pattern

**Highlight All**
- ☐ Unchecked: Highlights current match only
- ☑ Checked: Highlights all matches in yellow

---

## Replace Tab

### Basic Replace

**Replace text occurrences**

1. Enter search term in "Find:" field
2. Enter replacement in "Replace:" field
3. Choose action:
   - **Replace Next** - Replace current match, find next
   - **Replace All** - Replace all occurrences at once

**Example:**
```
Find: "prontera"
Replace: "geffen"
Result: All map references updated
```

---

### Replace Workflow

**Single replacement:**
1. Find first occurrence
2. Review context
3. Click "Replace Next"
4. Repeat or skip as needed

**Batch replacement:**
1. Verify find/replace terms
2. Click "Replace All"
3. Check result count
4. Undo (`Ctrl+Z`) if needed

---

## Regular Expressions

### Enable Regex Mode

Check **"Use Regex"** option to use regex patterns.

### Common Patterns

**Find any number:**
```
Pattern: \d+
Matches: 100, 150, 999
```

**Find variable names:**
```
Pattern: @\w+
Matches: @temp, @value, @count
```

**Find function calls:**
```
Pattern: \w+\(
Matches: mes(, getitem(, callfunc(
```

**Find comments:**
```
Pattern: //.*
Matches: // This is a comment
```

**Find map coordinates:**
```
Pattern: \d+,\d+
Matches: 100,150 or 160,170
```

---

### Regex Replace

**Example 1: Update all Zeny amounts**
```
Find: Zeny\s*[<>=]+\s*(\d+)
Replace: Zeny >= 1000
```

**Example 2: Change all sprite IDs**
```
Find: sprite\s+(\d+)
Replace: sprite 120
```

**Example 3: Update map names**
```
Find: prontera,(\d+),(\d+)
Replace: geffen,\1,\2
Keeps coordinates, changes map
```

---

## Highlight All Matches

**Visual overview of all occurrences**

1. Enable "Highlight All" option
2. Enter search term
3. Click "Find Next"
4. All matches highlighted in yellow

**Benefits:**
- See how many times term appears
- Visual scan of locations
- Identify patterns

**Clear highlights:**
- Close Find dialog
- Or start new search

---

## Advanced Techniques

### Find & Count

**How many times does "mes" appear?**

1. Search for "mes"
2. Enable "Highlight All"
3. Status shows: "Highlighted X occurrence(s)"

---

### Replace with Undo Safety

**Safe mass replacement:**

1. Note current line number
2. Click "Replace All"
3. Review changes
4. If wrong, press `Ctrl+Z` immediately
5. All changes undo at once

---

### Case-Preserving Replace

**Regex example:**
```
Find: (M|m)es
Replace: \1essage
Result: Mes → Message, mes → message
```

---

### Multi-line Search

**Regex across lines:**
```
Pattern: script.*\n.*\{
Finds: script headers with opening brace
```

---

## Common Use Cases

### Use Case 1: Change NPC Location

**Move all NPCs from prontera to geffen:**

```
Find: prontera,150,150
Replace: geffen,119,59
Action: Replace All
```

---

### Use Case 2: Update Item IDs

**Change all Red Potion (501) to Orange Potion (502):**

```
Find: getitem 501,
Replace: getitem 502,
Action: Replace All
```

---

### Use Case 3: Rename Variable

**Rename @temp to @value:**

```
Find: @temp
Replace: @value
Options: ☑ Whole Word
Action: Replace All
```

---

### Use Case 4: Find All Functions

**Locate all function definitions:**

```
Pattern: function\s+script\s+\w+
Options: ☑ Use Regex
Action: Find Next (repeatedly)
```

---

### Use Case 5: Clean Up Spacing

**Remove double spaces:**

```
Find: \s\s+
Replace: (single space)
Options: ☑ Use Regex
Action: Replace All
```

---

## Tips & Tricks

### Tip 1: Test Before Replace All
Use "Find Next" first to verify pattern before "Replace All".

### Tip 2: Use Whole Word
Prevent partial matches (e.g., "mes" in "message").

### Tip 3: Regex is Powerful
Learn basic regex for complex searches.

### Tip 4: Highlight for Overview
Enable "Highlight All" to see all matches at once.

### Tip 5: Undo is Your Friend
Made a mistake? `Ctrl+Z` reverses "Replace All".

---

## Regular Expression Quick Reference

### Character Classes
- `.` - Any character
- `\d` - Digit (0-9)
- `\w` - Word character (a-z, A-Z, 0-9, _)
- `\s` - Whitespace

### Quantifiers
- `*` - Zero or more
- `+` - One or more
- `?` - Zero or one
- `{n}` - Exactly n times
- `{n,}` - n or more times
- `{n,m}` - Between n and m times

### Anchors
- `^` - Start of line
- `$` - End of line

### Groups
- `(...)` - Capture group
- `\1, \2` - Back-reference to group

### Escapes
- `\.` - Literal dot
- `\(` - Literal parenthesis
- `\\` - Literal backslash

---

## Keyboard Shortcuts in Dialog

| Action | Shortcut |
|--------|----------|
| Open dialog | `Ctrl+F` |
| Find Next | `Enter` (in Find field) |
| Find Previous | `Shift+Enter` |
| Close dialog | `Escape` |

---

## Troubleshooting

### Find doesn't work

**Check:**
- Spelling of search term
- Case sensitivity option
- Text actually exists in file

---

### Replace All replaced too much

**Solution:**
1. Press `Ctrl+Z` immediately
2. Use "Whole Word" option
3. Or use "Replace Next" to review each

---

### Regex pattern not working

**Common mistakes:**
- Forgot to check "Use Regex"
- Need to escape special characters: `\. \( \)`
- Test pattern incrementally

---

### Highlights won't clear

**Solution:**
1. Close Find dialog
2. Reopen (`Ctrl+F`)
3. Close again
4. Or restart BalrogNPC

---

## Related Features

- [Text Editor Features](TEXT_EDITOR.md) - Basic editing
- [Line Numbers & Navigation](LINE_NUMBERS.md) - Navigation
- [Keyboard Shortcuts](KEYBOARD_SHORTCUTS.md) - All shortcuts

---

**Master Find & Replace for efficient script editing!** 🔍✨
