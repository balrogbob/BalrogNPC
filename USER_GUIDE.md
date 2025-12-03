# BalrogNPC - Complete User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [rAthena Tools Features](#rathena-tools-features)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [File Types](#file-types)
7. [Troubleshooting](#troubleshooting)

---

## Introduction

**BalrogNPC** is a standalone text editor specifically designed for rAthena script development. It combines the simplicity of Windows XP Notepad with powerful integrated tools for creating and editing rAthena server scripts.

### Key Features

- ✅ **Simple Interface** - Clean, distraction-free editing
- ✅ **Full rAthena Toolkit** - NPC wizard, dialog builder, validators
- ✅ **Script Validation** - Real-time error checking with auto-fix
- ✅ **YAML Support** - Validate rAthena database files
- ✅ **Template Library** - Pre-built NPCs for common scenarios
- ✅ **No Dependencies** - Works out of the box with Python

---

## Installation

### Requirements

- **Python 3.8 or higher**
- **tkinter** (usually included with Python on Windows)

### Optional Requirements

For YAML validation features:
```bash
pip install pyyaml
```

### Quick Start

1. **Download** the BalrogNPC folder
2. **Navigate** to the folder
3. **Run** one of:
   - Double-click `run.bat` (Windows)
   - Run `python BalrogNPC.py` from terminal

That's it! The application will start immediately.

---

## Basic Usage

### Creating a New File

1. Click **File → New** (or press `Ctrl+N`)
2. Start typing your script
3. Save with **File → Save** (or `Ctrl+S`)

### Opening an Existing File

1. Click **File → Open** (or press `Ctrl+O`)
2. Browse to your file
3. Select and click **Open**

Supported file types:
- Text files (*.txt)
- rAthena scripts (*.npc)
- YAML database files (*.yml, *.yaml)
- All files (*.*)

### Editing Text

Standard editing features are available:

- **Cut** - `Ctrl+X`
- **Copy** - `Ctrl+C`
- **Paste** - `Ctrl+V`
- **Undo** - `Ctrl+Z`
- **Select All** - `Ctrl+A`

### Word Wrap

Toggle word wrapping from **Format → Word Wrap**

### Changing Font Size

1. Click **Format → Font...**
2. Adjust the slider
3. Click **OK**

---

## rAthena Tools Features

The **rAthena Tools** menu provides powerful script creation and validation features.

### 1. New NPC Script

Creates a new NPC using a step-by-step wizard.

**Steps:**
1. Click **rAthena Tools → New NPC Script**
2. Follow the wizard through 5 steps:
   - **Step 1:** Name and location (map, X, Y coordinates)
   - **Step 2:** Appearance (sprite selection)
   - **Step 3:** NPC type (Dialog, Quest, Shop, etc.)
   - **Step 4:** Dialog actions (messages, menus, commands)
   - **Step 5:** Review and confirm
3. Script is inserted into the editor

### 2. New Function

Creates a custom rAthena function with:

- **Parameter definition** - Add typed parameters
- **Return type selection** - void, int, string, array
- **Code templates** - Item checker, Zeny checker, random rewards, etc.
- **Quick snippets** - Common code patterns

**Features:**
- Live preview of generated function
- Template insertion
- Parameter documentation comments
- "Insert & Close" or "Insert Function" to add multiple

### 3. NPC Wizard

Opens the full NPC creation wizard (same as "New NPC Script").

### 4. Dialog Builder

Visual dialog sequence builder for creating complex NPC conversations.

**Actions Available:**
- **Message** - Display text to player
- **Next** - Show "Next" button
- **Close** - Close dialog
- **Menu** - Create selection menu with branches
- **Script** - Insert raw script commands
- **Warp** - Teleport player
- **Check Item** - Verify player has items
- **Give Item** - Reward player with items
- **Remove Item** - Take items from player

**Features:**
- Drag to reorder actions (↑↓ buttons)
- Define dialog branches for menus
- Live preview of generated script
- Insert directly into editor

### 5. Validate Script

Comprehensive script validation with:

**Three Tabs:**
- **Errors** - Syntax errors (must fix)
- **Warnings** - Style issues (should fix)
- **Best Practices** - Suggestions (optional)

**Features:**
- Line-by-line validation
- Indentation checking
- Missing semicolons detection
- Common typo detection
- **Auto-fix** - Fix issues automatically
- **Review & Fix** - Step through each issue

**Example Checks:**
- Bracket balancing
- String closing
- Indentation consistency (tabs vs spaces)
- Command typos (mesage → mes, clos → close)
- Missing semicolons
- Case statement colons

### 6. Validate YAML Database

Validates rAthena YAML database files (items, mobs, skills, etc.)

**Features:**
- YAML syntax validation
- Structure verification
- Field type checking
- Three-tab result display (Errors/Warnings/Suggestions)

### 7. Insert Quick NPC

Insert pre-built NPC templates with customization.

**Templates Available:**
1. **Simple Dialog** - Basic greeting NPC
2. **Healer NPC** - Restores HP/SP
3. **Warper/Teleporter** - Multi-destination warp menu
4. **Item Shop** - Sells items
5. **Buffer NPC** - Provides buffs
6. **Quest Starter** - Item collection quest
7. **Job Changer** - Change player job
8. **Information NPC** - Display server info
9. **Stylist NPC** - Change appearance
10. **Tool Dealer** - Shop with NPC shop system

**Customization:**
- NPC name
- Map location (X, Y coordinates)
- Sprite selection (from dropdown or custom ID)
- Live preview before inserting

---

## Keyboard Shortcuts

### File Operations
- `Ctrl+N` - New file
- `Ctrl+O` - Open file
- `Ctrl+S` - Save file

### Editing
- `Ctrl+Z` - Undo
- `Ctrl+X` - Cut
- `Ctrl+C` - Copy
- `Ctrl+V` - Paste
- `Ctrl+A` - Select All

---

## File Types

### Supported Extensions

| Extension | Description |
|-----------|-------------|
| .txt | Plain text files |
| .npc | rAthena NPC scripts |
| .yml, .yaml | YAML database files |
| *.* | All files |

### File Encoding

- **Reading:** UTF-8 with error replacement
- **Writing:** UTF-8

---

## Troubleshooting

### Application Won't Start

**Problem:** Double-clicking `run.bat` does nothing or shows error

**Solution:**
1. Ensure Python 3.8+ is installed
2. Check Python is in PATH:
   ```bash
   python --version
   ```
3. If not in PATH, run directly:
   ```bash
   C:\Python38\python.exe BalrogNPC.py
   ```

### rAthena Tools Menu Missing

**Problem:** Only File, Edit, Format, Help menus appear

**Solution:**
- Check `rathena_tools_menu.py` exists in same folder as `BalrogNPC.py`
- Check `rathena-tools` folder exists with all files
- Look for error messages in console when starting

### YAML Validation Shows "Not Available"

**Problem:** YAML validator menu item doesn't work

**Solution:**
Install PyYAML:
```bash
pip install pyyaml
```

Restart BalrogNPC.

### Script Validation Errors

**Problem:** Validator shows many indentation warnings

**Solution:**
- Use **Apply All Fixes** to auto-correct
- Or use **Review & Fix** to step through each issue
- rAthena scripts should use **tabs**, not spaces

### Can't Save File

**Problem:** "Could not save file" error appears

**Solution:**
1. Check you have write permission to the folder
2. Try "Save As" to a different location
3. Ensure file is not open in another program
4. Check disk is not full

---

## Advanced Tips

### Using Templates Effectively

1. **Start with template** - Use Insert Quick NPC for foundation
2. **Modify in place** - Edit the inserted code
3. **Use Dialog Builder** - Add complex interactions
4. **Validate often** - Check for errors as you go

### Working with Large Scripts

1. **Use Functions** - Break complex logic into functions
2. **Use Word Wrap** - Enable for long dialog lines
3. **Validate Early** - Find errors before they compound
4. **Save Often** - Use Ctrl+S frequently

### Best Practices

1. **Use Tabs for Indentation** - Not spaces (rAthena standard)
2. **End Commands with Semicolons** - Required for most commands
3. **Close Dialogs Properly** - Use `close;` or `end;`
4. **Comment Your Code** - Use `//` for clarity
5. **Test NPCs** - Load on test server before production

---

## Example Workflow

### Creating a Quest NPC

1. **Start with Template**
   - Click **rAthena Tools → Insert Quick NPC**
   - Select **Quest Starter** template
   - Set name, location, sprite
   - Click **Insert NPC**

2. **Customize Dialog**
   - Select the inserted NPC code
   - Click **rAthena Tools → Dialog Builder**
   - Add messages, item checks, rewards
   - Click **Insert into Script**

3. **Add Function**
   - Click **rAthena Tools → New Function**
   - Name: `CheckQuestComplete`
   - Use **Item Checker** template
   - Customize item IDs
   - Click **Insert Function**

4. **Validate**
   - Click **rAthena Tools → Validate Script**
   - Review any errors or warnings
   - Use **Apply All Fixes** if needed

5. **Save**
   - Press `Ctrl+S`
   - Choose filename (e.g., `my_quest.npc`)
   - Save

6. **Test**
   - Copy to rAthena server's `npc/custom/` folder
   - Add to `scripts_custom.conf`
   - Reload server and test

---

## Getting Help

### Documentation

- **rAthena Script Guide** - See `rathena-tools/RATHENA_SCRIPT_GUIDE.md`
- **Quick Reference** - See `rathena-tools/QUICK_REFERENCE.md`
- **API Docs** - See `rathena-tools/RATHENA_TOOLS_README.md`

### Examples

- Run `python rathena-tools/examples.py` to see 10 working examples

---

## Credits

- **rAthena** - https://rathena.org
- **BalrogNPC** - Standalone editor with integrated toolkit

---

## Version

**Version:** 1.0  
**Release Date:** 2025  
**Python:** 3.8+  
**License:** Open Source  

---

## Changelog

### Version 1.0 (Initial Release)
- Simple text editor interface
- File operations (New, Open, Save, Save As)
- Basic editing (Cut, Copy, Paste, Undo)
- Word wrap toggle
- Font size customization
- Full rAthena Tools integration
  - NPC Wizard (5-step guided creation)
  - Function Creator (with templates)
  - Dialog Builder (visual sequence builder)
  - Script Validator (with auto-fix)
  - YAML Validator
  - Quick NPC Templates (10 pre-built)
- Comprehensive documentation

---

**Happy scripting!** 🎮✨
