# BalrogNPC - rAthena Script Editor

A standalone text editor with integrated rAthena script generation tools.

## Features

- **Simple text editor** - Windows XP Notepad-style interface
- **File operations** - New, Open, Save, Save As
- **Basic editing** - Cut, Copy, Paste, Undo, Select All
- **Word wrap** - Toggle word wrapping on/off
- **Font customization** - Adjustable font size
- **rAthena Tools** - Complete script generation toolkit integrated

## rAthena Tools Menu

When rAthena tools are available, you get access to:

- **New NPC Script** - Create NPCs using the wizard
- **New Function** - Create custom script functions with templates
- **NPC Wizard** - Step-by-step NPC creation
- **Dialog Builder** - Visual dialog sequence builder
- **Validate Script** - Check scripts for errors with auto-fix
- **Validate YAML Database** - Validate rAthena YAML files
- **Insert Quick NPC** - Insert pre-built NPC templates

## Running the Application

```bash
python BalrogNPC.py
```

Or on Windows, double-click `BalrogNPC.py`

## Requirements

- Python 3.8 or higher
- tkinter (usually included with Python)

Optional for YAML validation:
- PyYAML (`pip install pyyaml`)

## File Structure

```
BalrogNPC/
├── BalrogNPC.py              # Main application
├── rathena_tools_menu.py     # rAthena tools menu integration
├── rathena-tools/            # Complete rAthena toolkit
│   ├── rathena_script_gen.py
│   ├── rathena_script_ui.py
│   ├── rathena_yaml_validator.py
│   ├── examples.py
│   └── [documentation files]
└── README.md                 # This file
```

## Keyboard Shortcuts

- **Ctrl+N** - New file
- **Ctrl+O** - Open file
- **Ctrl+S** - Save file
- **Ctrl+Z** - Undo
- **Ctrl+X** - Cut
- **Ctrl+C** - Copy
- **Ctrl+V** - Paste
- **Ctrl+A** - Select All

## Supported File Types

- All files (*.*)
- Text files (*.txt)
- rAthena Scripts (*.npc, *.txt)
- YAML Files (*.yml, *.yaml)

## About rAthena Tools

The integrated rAthena tools provide:

- **Script Generation** - Create NPCs, functions, and variables programmatically
- **Visual Builders** - Dialog builder, NPC wizard, and more
- **Validation** - Check scripts for syntax errors and best practices
- **Templates** - Pre-built NPCs for common use cases
- **Auto-fix** - Automatic fixing of indentation and syntax issues

For complete documentation, see the `rathena-tools/` directory.

## License

This application is provided as-is for rAthena development.

## Version

1.0 - Initial release
