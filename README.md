# BalrogNPC 🐉 — rAthena Script Editor

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-0.2.1-brightgreen.svg)](#)

**A lightweight rAthena-focused text editor with integrated script generation, dialog builders and validation tools.**

[Features](#features-) • [Quick Start](#quick-start-) • [Documentation](#documentation-) • [Screenshots](#screenshots-)

</div>

---

## What's New ✨

- **Line Numbers** - Left-side gutter for easy navigation 🔢
- **Go To Line** - Jump directly to any line (`Ctrl+G`) ➤
- **Full Find & Replace** (`Ctrl+F`):
  - Find Next / Find Previous
  - Replace Next / Replace All
  - Regex mode with Python `re` 🧩
  - Case sensitive toggle
  - Whole-word matching
  - Highlight all matches
- **Syntax Highlighting** - Customizable colors for rAthena scripts and YAML databases
- **Enhanced rAthena Tools** - NPC wizard, dialog builder, function creator, validators

---

## Features 🚀

### Text Editor
✅ **Simple, clean interface** - Windows XP Notepad style  
✅ **File operations** - New, Open, Save, Save As  
✅ **Editing** - Cut, Copy, Paste, Undo, Select All  
✅ **Search** - Find & Replace with regex support  
✅ **Navigation** - Line numbers, Go To Line  
✅ **Customization** - Word wrap, font size, syntax colors  

### rAthena Tools
✅ **NPC Wizard** - Step-by-step guided NPC creation  
✅ **Function Creator** - Build functions with templates  
✅ **Dialog Builder** - Visual dialog sequence builder  
✅ **Script Validator** - Real-time error checking with auto-fix  
✅ **YAML Validator** - Database file validation  
✅ **Quick NPC Templates** - 10 pre-built NPC types  

### Syntax Highlighting
✅ **Script highlighting** - rAthena script syntax  
✅ **Database highlighting** - YAML database files  
✅ **Color customization** - Edit colors via GUI  
✅ **Multiple syntax files** - Extensible syntax system  

---

## Quick Start 🚀

### Installation

**Requirements:**
- Python 3.8 or higher
- tkinter (usually included)
- PyYAML (optional, for YAML validation)

**Install:**
```bash
# Clone repository
git clone https://github.com/balrogbob/BalrogNPC.git
cd BalrogNPC

# Optional: Install YAML support
pip install pyyaml

# Run
python BalrogNPC.py
```

**Windows Quick Start:**
```bash
# Double-click run.bat
# OR
python BalrogNPC.py
```

### Create Your First NPC

1. Launch BalrogNPC
2. Click **rAthena Tools → Insert Quick NPC**
3. Select **"Simple Dialog"**
4. Enter NPC name and customize
5. Click **Insert NPC**
6. Save (`Ctrl+S`)

Done! You've created your first NPC.

---

## Documentation 📚

### 📖 Complete Documentation Index

**All documentation is in the [docs](docs/) folder.**

#### Getting Started
- **[Getting Started Guide](docs/GETTING_STARTED.md)** - Installation and first steps (30 min)
- **[User Guide](docs/USER_GUIDE.md)** - Complete feature walkthrough (2 hours)
- **[Keyboard Shortcuts](docs/KEYBOARD_SHORTCUTS.md)** - All shortcuts reference

#### rAthena Scripting
- **[rAthena Script Guide](docs/RATHENA_SCRIPT_GUIDE.md)** - Comprehensive 9-chapter guide (6-8 hours)
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - One-page command reference
- **[Script Examples](docs/SCRIPT_EXAMPLES.md)** - 10 working code examples

#### Tools & Features
- **[NPC Wizard Guide](docs/NPC_WIZARD.md)** - Step-by-step NPC creation
- **[Dialog Builder Guide](docs/DIALOG_BUILDER.md)** - Visual dialog sequences
- **[Function Creator Guide](docs/FUNCTION_CREATOR.md)** - Function templates
- **[Script Validator Guide](docs/SCRIPT_VALIDATOR.md)** - Validation and auto-fix
- **[YAML Validator Guide](docs/YAML_VALIDATOR.md)** - Database validation
- **[Quick NPC Templates](docs/QUICK_NPC_TEMPLATES.md)** - All 10 templates

#### Advanced
- **[Syntax Highlighting](docs/SYNTAX_HIGHLIGHTING.md)** - Customize colors
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues
- **[FAQ](docs/FAQ.md)** - Frequently asked questions

**➤ [Complete Documentation Index](docs/INDEX.md)** - Full navigation and learning paths

---

## Keyboard Shortcuts ⌨️

### Essential Shortcuts
```
Ctrl+N  New file
Ctrl+O  Open file
Ctrl+S  Save file
Ctrl+F  Find & Replace
Ctrl+G  Go To Line
Ctrl+Z  Undo
Ctrl+A  Select All
```

**[Complete Shortcuts Reference →](docs/KEYBOARD_SHORTCUTS.md)**

---

## Screenshots 📸

### Main Editor
![Main Editor](screenshot2.png)

### rAthena Tools
![rAthena Tools](screenshot1.png)

---

## Quick Examples 💡

### Example 1: Simple Greeting NPC
```
prontera,150,150,4	script	Greeter	111,{
	mes "[Greeter]";
	mes "Welcome to our server!";
	close;
}
```

### Example 2: Healer NPC
```
prontera,160,160,4	script	Healer	4_W_SISTER,{
	percentheal 100, 100;
	mes "[Healer]";
	mes "You're fully healed!";
	close;
}
```

**[More Examples →](docs/SCRIPT_EXAMPLES.md)**

---

## Features Overview 🎯

| Feature | Description | Access |
|---------|-------------|--------|
| **NPC Wizard** | 5-step guided creation | rAthena Tools menu |
| **Dialog Builder** | Visual dialog sequences | rAthena Tools menu |
| **Function Creator** | Templates & parameters | rAthena Tools menu |
| **Script Validator** | Auto-fix errors | rAthena Tools menu |
| **YAML Validator** | Database validation | rAthena Tools menu |
| **Quick Templates** | 10 pre-built NPCs | rAthena Tools menu |
| **Find & Replace** | Regex support | `Ctrl+F` |
| **Go To Line** | Quick navigation | `Ctrl+G` |
| **Syntax Highlighting** | Customizable colors | Syntax menu |

---

## Project Structure 📁

```
BalrogNPC/
├── BalrogNPC.py              # Main application
├── rathena_tools_menu.py     # rAthena tools integration
├── syntax_highlighter.py     # Syntax highlighting engine
├── run.bat                   # Windows launcher
├── requirements.txt          # Python dependencies
│
├── docs/                     # Complete documentation
│   ├── INDEX.md             # Documentation index
│   ├── GETTING_STARTED.md   # Quick start guide
│   ├── USER_GUIDE.md        # Complete user manual
│   ├── RATHENA_SCRIPT_GUIDE.md  # 9-chapter scripting guide
│   ├── QUICK_REFERENCE.md   # Command reference
│   ├── SCRIPT_EXAMPLES.md   # Working examples
│   └── [More guides...]
│
├── rathena-tools/           # Script generation toolkit
│   ├── rathena_script_gen.py
│   ├── rathena_script_ui.py
│   ├── rathena_yaml_validator.py
│   └── examples.py
│
└── syntax/                  # Syntax highlighting files
    ├── rathena.ini
    ├── yaml.ini
    └── yaml_header.ini
```

---

## Learning Paths 🎓

### Path 1: Quick Start (30 minutes)
1. Read [Getting Started](docs/GETTING_STARTED.md)
2. Try [Quick NPC Templates](docs/QUICK_NPC_TEMPLATES.md)
3. Review [Quick Reference](docs/QUICK_REFERENCE.md)

### Path 2: Script Creation (3-4 hours)
1. [Quick Reference](docs/QUICK_REFERENCE.md)
2. [NPC Wizard](docs/NPC_WIZARD.md)
3. [Dialog Builder](docs/DIALOG_BUILDER.md)
4. [Script Examples](docs/SCRIPT_EXAMPLES.md)

### Path 3: rAthena Mastery (8-10 hours)
1. [Quick Reference](docs/QUICK_REFERENCE.md)
2. [rAthena Script Guide](docs/RATHENA_SCRIPT_GUIDE.md) (all 9 chapters)
3. [Script Examples](docs/SCRIPT_EXAMPLES.md)
4. Practice with tools

---

## Contributing 🤝

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License 📄

MIT License - see [LICENSE.txt](LICENSE.txt)

---

## Support & Resources 💬

- **Documentation:** [docs/INDEX.md](docs/INDEX.md)
- **Issues:** [GitHub Issues](https://github.com/balrogbob/BalrogNPC/issues)
- **rAthena:** [https://rathena.org](https://rathena.org)

---

## Version Information ℹ️

**Current Version:** 0.2.1  
**Python Required:** 3.8+  
**Status:** Active Development  
**Last Updated:** December 2025  

---

<div align="center">

**Built for the rAthena community** ❤️

[Get Started](docs/GETTING_STARTED.md) • [Documentation](docs/INDEX.md) • [Examples](docs/SCRIPT_EXAMPLES.md)

**Happy scripting!** 🎮✨

</div>

