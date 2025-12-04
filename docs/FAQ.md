# Frequently Asked Questions (FAQ)

**Quick answers to common questions about BalrogNPC**

---

## General Questions

### What is BalrogNPC?

BalrogNPC is a lightweight text editor specifically designed for creating rAthena server scripts. It combines simple text editing with integrated tools for NPC creation, validation, and testing.

### Is BalrogNPC free?

Yes! BalrogNPC is completely free and open source (MIT License).

### What operating systems are supported?

- ✅ Windows 7/8/10/11
- ✅ Linux (most distributions)
- ✅ macOS

### Do I need to know Python to use BalrogNPC?

No! BalrogNPC is a ready-to-use application. Python is only needed to run it.

---

## Installation & Setup

### How do I install BalrogNPC?

1. Install Python 3.8+ from [python.org](https://python.org)
2. Download BalrogNPC from GitHub
3. Run `python BalrogNPC.py`

See [Getting Started](GETTING_STARTED.md) for detailed steps.

### Why isn't there an .exe file?

BalrogNPC is a Python application. You can create your own .exe using PyInstaller if desired.

### Can I use BalrogNPC without internet?

Yes! Once downloaded, BalrogNPC works completely offline.

---

## Features & Functionality

### Can BalrogNPC run my scripts?

No. BalrogNPC is an **editor**, not a server. You need an rAthena server to run scripts.

### Does BalrogNPC support syntax highlighting?

Yes! Enable it via **Syntax → Script** or **Syntax → Database**.

### Can I customize the syntax colors?

Yes! Click **Syntax → Edit Colors...** to customize foreground and background colors for each syntax element.

### Does BalrogNPC have auto-complete?

Not currently. This is a potential future feature.

### Can I open multiple files at once?

Not currently. BalrogNPC focuses on single-file editing. Use multiple instances if needed.

---

## rAthena Tools

### What can the NPC Wizard do?

The NPC Wizard guides you through creating NPCs step-by-step:
1. Set name and location
2. Choose appearance (sprite)
3. Select NPC type
4. Build dialog sequence
5. Generate complete script

### What templates are available?

10 pre-built templates:
1. Simple Dialog
2. Healer NPC
3. Warper/Teleporter
4. Item Shop
5. Buffer NPC
6. Quest Starter
7. Job Changer
8. Information NPC
9. Stylist NPC
10. Tool Dealer

See [Quick NPC Templates](QUICK_NPC_TEMPLATES.md).

### How does the Script Validator work?

The validator checks for:
- Syntax errors (missing semicolons, unbalanced brackets)
- Indentation issues (tabs vs spaces)
- Common typos (clos → close)
- Best practices

It can auto-fix many issues automatically.

### Can I validate YAML files?

Yes! Use **rAthena Tools → Validate YAML Database**. Requires PyYAML:
```bash
pip install pyyaml
```

---

## Editing & Navigation

### How do I search for text?

Press `Ctrl+F` to open Find & Replace dialog. Features:
- Find Next / Find Previous
- Replace Next / Replace All
- Regex support
- Case sensitive option
- Whole word matching

### How do I go to a specific line?

Press `Ctrl+G` and enter the line number.

### Can I use regex in Find & Replace?

Yes! Check the "Use Regex" option in the Find & Replace dialog.

### How do I select all text?

Press `Ctrl+A` or use **Edit → Select All**.

---

## File Management

### What file formats does BalrogNPC support?

- `.txt` - Plain text
- `.npc` - rAthena script files
- `.yml`, `.yaml` - YAML database files
- All files (`*.*`)

### What encoding does BalrogNPC use?

UTF-8 for both reading and writing files.

### Can I open binary files?

Not recommended. BalrogNPC is designed for text files only.

---

## Scripting Questions

### Where can I learn rAthena scripting?

1. [Quick Reference](QUICK_REFERENCE.md) - One-page command list
2. [rAthena Script Guide](RATHENA_SCRIPT_GUIDE.md) - Complete 9-chapter guide
3. [Script Examples](SCRIPT_EXAMPLES.md) - Working code examples
4. rAthena wiki and forums

### What's the difference between Script and Database syntax?

- **Script** - For `.npc` files (NPC scripts, functions)
- **Database** - For `.yml` files (item_db, mob_db, etc.)

### How do I test my scripts?

1. Save your script
2. Copy to rAthena server's `npc/custom/` folder
3. Add to `scripts_custom.conf`:
   ```
   npc: npc/custom/yourfile.npc
   ```
4. Reload server: `@reloadscript`

---

## Troubleshooting

### BalrogNPC won't start

**Check:**
1. Python 3.8+ installed?
2. Python in PATH?
3. All files present?

See [Troubleshooting](TROUBLESHOOTING.md) for solutions.

### rAthena Tools menu is missing

**Cause:** Missing or corrupted files

**Fix:**
1. Verify `rathena-tools/` folder exists
2. Check for import errors in console
3. Redownload if needed

### Validation shows too many errors

**This is normal!** Scripts often have issues. Use:
- **Review & Fix** - Step through each issue
- **Apply All Fixes** - Auto-fix simple issues
- **Skip false positives** - Some warnings are optional

### Find & Replace is slow

**Cause:** Regex on large files

**Fix:**
- Disable regex mode
- Use simple text search
- Disable "Highlight All Matches"

---

## Comparison Questions

### BalrogNPC vs Notepad++

| Feature | BalrogNPC | Notepad++ |
|---------|-----------|-----------|
| **rAthena Tools** | ✅ Built-in | ❌ None |
| **Script Validation** | ✅ Yes | ❌ No |
| **NPC Templates** | ✅ 10 templates | ❌ No |
| **Syntax Highlighting** | ✅ rAthena-specific | ⚠️ Generic |
| **Multi-file** | ❌ No | ✅ Yes |
| **Plugins** | ❌ No | ✅ Yes |
| **Size** | ⚠️ Requires Python | ✅ Standalone |
| **Learning Curve** | ✅ Simple | ⚠️ Moderate |

**Use BalrogNPC if:** You primarily write rAthena scripts  
**Use Notepad++ if:** You need multi-file editing

### BalrogNPC vs VS Code

| Feature | BalrogNPC | VS Code |
|---------|-----------|---------|
| **rAthena Tools** | ✅ Built-in | ⚠️ Via extensions |
| **Size** | ✅ Lightweight | ⚠️ Heavy (~200MB) |
| **Simplicity** | ✅ Very simple | ⚠️ Complex |
| **Features** | ⚠️ Basic | ✅ Advanced |
| **Extensions** | ❌ No | ✅ Thousands |

**Use BalrogNPC if:** You want simplicity and rAthena focus  
**Use VS Code if:** You need advanced IDE features

---

## Advanced Questions

### Can I extend BalrogNPC with plugins?

Not currently. BalrogNPC doesn't have a plugin system.

### Can I modify BalrogNPC?

Yes! It's open source (MIT License). Fork and modify as needed.

### How do I report bugs?

Create an issue on GitHub Issues (see repository) with:
- OS and Python version
- Steps to reproduce
- Error messages

### Can I contribute to BalrogNPC?

Yes! Contributions welcome:
1. Fork repository
2. Make changes
3. Submit pull request

### Will there be more features?

Potentially! Feature requests welcome on GitHub Issues.

---

## Tips & Best Practices

### Workflow Tips

**Quick NPC Creation:**
1. `Ctrl+N` - New file
2. **rAthena Tools → Insert Quick NPC**
3. Customize and insert
4. `Ctrl+S` - Save

**Validate Before Use:**
1. Write script
2. **rAthena Tools → Validate Script**
3. Fix issues
4. Save and deploy

**Learn by Example:**
1. Open [Script Examples](SCRIPT_EXAMPLES.md)
2. Copy template
3. Modify for your needs
4. Test and iterate

### Keyboard Efficiency

**Essential Shortcuts:**
```
Ctrl+S  Save (use frequently!)
Ctrl+F  Find & Replace
Ctrl+G  Go To Line
Ctrl+Z  Undo (saves you!)
```

**[Full Shortcuts List →](KEYBOARD_SHORTCUTS.md)**

---

## Getting More Help

### Documentation
- [Getting Started](GETTING_STARTED.md) - Installation
- [User Guide](USER_GUIDE.md) - All features
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- [Complete Index](INDEX.md) - All docs

### Community
- rAthena Forums: [rathena.org](https://rathena.org)
- GitHub Issues: Bug reports and features
- Discord: rAthena community channels

### Learning Resources
- [rAthena Script Guide](RATHENA_SCRIPT_GUIDE.md) - Complete guide
- [Quick Reference](QUICK_REFERENCE.md) - Command list
- [Script Examples](SCRIPT_EXAMPLES.md) - Working code

---

**Question not answered?** Ask on GitHub Issues (see repository) or check [Troubleshooting](TROUBLESHOOTING.md)!
