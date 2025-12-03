# rAthena Script Development Tools

**Comprehensive Script Writing Guide + Modular Script Generator**

This package contains a complete reference guide for rAthena scripting and a modular Python-based script generator that can be integrated into SimpleEdit or other IDEs.

---

## Contents

### 1. **RATHENA_SCRIPT_GUIDE.md**
A comprehensive markdown guide covering all aspects of rAthena scripting:

- **Chapter 1**: Fundamentals - Basic concepts and file structure
- **Chapter 2**: Variables and Data - Variable scopes, types, operators
- **Chapter 3**: Basic Commands - Messages, dialogs, input, items
- **Chapter 4**: Control Flow - Conditionals, loops, switches
- **Chapter 5**: Functions and Subroutines - Reusable code blocks
- **Chapter 6**: NPC Creation - Creating interactive NPCs
- **Chapter 7**: Item and Equipment - Working with inventory
- **Chapter 8**: Advanced Features - Quest systems, events, warping
- **Chapter 9**: Debugging and Best Practices - Common mistakes and solutions

**Best for:**
- Learning rAthena scripting from scratch
- Quick reference during development
- Understanding complex concepts
- Code examples and patterns

---

## Modular Script Generator

Three Python modules that work together to generate rAthena scripts programmatically:

### 2. **rathena_script_gen.py**
Core generator module with the engine for creating scripts.

**Key Classes:**

#### `ScriptGenerator`
Main orchestrator class for script creation.

```python
from rathena_script_gen import ScriptGenerator, ScriptNPC

# Create generator with logging
def log_handler(level, msg):
    print(f"[{level.value}] {msg}")

gen = ScriptGenerator(log_callback=log_handler)
gen.set_metadata(
    name="my_script",
    author="Your Name",
    description="My custom script"
)

# Generate script
script = gen.generate_script()

# Export to file
gen.export_script("my_script.txt")
```

#### `ScriptNPC`
Represents a single NPC with all properties and commands.

```python
from rathena_script_gen import ScriptNPC

npc = ScriptNPC(
    name="Merchant",
    map_name="prontera",
    x=150,
    y=150,
    sprite_id=120,
    facing=4
)

npc.add_command('mes "[Merchant]";')
npc.add_command('mes "Welcome!";')
npc.add_command('close;')

gen.add_npc(npc)
```

#### `ScriptFunction`
Reusable function definitions.

```python
from rathena_script_gen import ScriptFunction

func = ScriptFunction("CalculatePrice")
func.add_command('.@base = getarg(0);')
func.add_command('.@result = .@base * 2;')
func.return_value = ".@result"

gen.add_function(func)
```

#### `ScriptVariable`
Global and local variable definitions.

```python
from rathena_script_gen import ScriptVariable

var = ScriptVariable(
    name="quest_level",
    value=1,
    scope=".",  # NPC scope
    is_string=False
)

gen.add_global_variable(var)
```

#### `QuickScriptBuilders`
Pre-built templates for common NPC types.

```python
from rathena_script_gen import QuickScriptBuilders

# Create a healing NPC
npc = QuickScriptBuilders.create_heal_npc(
    "Healer",
    "prontera",
    150, 150
)
gen.add_npc(npc)

# Create a warp NPC
npc = QuickScriptBuilders.create_warp_npc(
    "Porter",
    "prontera",
    150, 150,
    [
        ("geffen", 119, 59, "Geffen"),
        ("payon", 161, 247, "Payon"),
        ("izlude", 128, 114, "Izlude")
    ]
)
gen.add_npc(npc)
```

---

### 3. **rathena_script_ui.py**
UI components and helpers for visual script building (framework-agnostic).

**Key Classes:**

#### `NPCWizard`
Step-by-step guided NPC creation.

```python
from rathena_script_ui import NPCWizard, NPCTypeEnum

def on_complete(npc):
    print(f"Created NPC: {npc.name}")

wizard = NPCWizard(on_complete)

# Step 1: Basic info
wizard.set_npc_basic_info("Trainer", "prontera", 150, 150)

# Step 2: Appearance
wizard.set_npc_appearance(120)

# Step 3: Type
wizard.set_npc_type(NPCTypeEnum.QUEST_GIVER)

# Move through steps
wizard.next_step()
```

#### `DialogBuilder`
Fluent API for building dialogs.

```python
from rathena_script_ui import DialogBuilder

dialog = DialogBuilder()
dialog.add_message("Hello, adventurer!") \
       .add_next_button() \
       .add_message("I have a quest for you.") \
       .add_menu(["Accept", "Decline"]) \
       .add_item_check(1010, 5) \
       .add_item_give(1011, 1) \
       .add_warp("geffen", 119, 59) \
       .add_close_button()

commands = dialog.to_script_commands()
for cmd in commands:
    print(cmd)
```

#### `ScriptTemplates`
Pre-defined script templates.

```python
from rathena_script_ui import ScriptTemplates

# Get all templates
templates = ScriptTemplates.get_all_templates()

# Get specific template
shop_template = ScriptTemplates.get_template_by_name("Simple Shop")
print(shop_template['preview'])
```

#### `ScriptValidator`
Validates scripts before generation.

```python
from rathena_script_ui import ScriptValidator

# Validate NPC
valid, errors = ScriptValidator.validate_npc(npc)
if not valid:
    for error in errors:
        print(f"Error: {error}")

# Validate entire script
valid, errors = ScriptValidator.validate_script(generator)
```

#### `SimpleEditIntegration`
Standard callbacks for IDE integration.

```python
from rathena_script_ui import SimpleEditIntegration

integration = SimpleEditIntegration(generator)

# Handle IDE events
integration.on_new_project()
integration.on_export("my_script.txt")
status = integration.get_status_info()
```

---

## Integration with SimpleEdit

### Adding to SimpleEdit as a Module

1. **Copy files** to SimpleEdit plugin directory:
   ```
   SimpleEdit/plugins/
   ├── rathena_script_gen.py
   ├── rathena_script_ui.py
   └── __init__.py (empty file)
   ```

2. **Create plugin wrapper** for SimpleEdit:
   ```python
   # SimpleEdit/plugins/rathena_plugin.py
   from rathena_script_ui import SimpleEditIntegration
   from rathena_script_gen import ScriptGenerator
   
   class RathenaPlugin:
       def __init__(self):
           self.generator = ScriptGenerator()
           self.integration = SimpleEditIntegration(self.generator)
       
       def on_menu_click_new_script(self):
           self.integration.on_new_project()
       
       def on_menu_click_export(self, filepath):
           return self.integration.on_export(filepath)
   ```

3. **Register in SimpleEdit**:
   ```python
   # In SimpleEdit's plugin loader
   from plugins.rathena_plugin import RathenaPlugin
   
   rathena = RathenaPlugin()
   register_plugin("rAthena Script Generator", rathena)
   ```

---

## Usage Examples

### Example 1: Simple Dialog NPC

```python
from rathena_script_gen import ScriptGenerator, ScriptNPC

gen = ScriptGenerator()
gen.set_metadata("dialog_script", "Developer")

npc = ScriptNPC("Greeter", "prontera", 150, 150)
npc.add_command('mes "[Greeter]";')
npc.add_command('mes "Hello, welcome!";')
npc.add_command('mes "What can I help you with?";')
npc.add_command('switch(select("Talk:Leave")) {')
npc.add_command('\tcase 1:')
npc.add_command('\t\tmes "Nice talking with you!";')
npc.add_command('\t\tbreak;')
npc.add_command('}')
npc.add_command('close;')

gen.add_npc(npc)
print(gen.generate_script())
```

### Example 2: Quest-Giving NPC

```python
from rathena_script_gen import ScriptGenerator, ScriptNPC

gen = ScriptGenerator()
gen.set_metadata("quest_script", "Developer")

npc = ScriptNPC("QuestMaster", "prontera", 150, 150)
npc.add_command('mes "[QuestMaster]";')
npc.add_command('if (MISC_QUEST & 1) {')
npc.add_command('\t\tmes "Thanks for completing my task!";')
npc.add_command('\t\tclose;')
npc.add_command('}')
npc.add_command('mes "I need 5 Phracon for a project.";')
npc.add_command('if (select("Accept:Decline") == 1) {')
npc.add_command('\t\tif (countitem(1010) >= 5) {')
npc.add_command('\t\t\tdelitem 1010, 5;')
npc.add_command('\t\t\tgetitem 1012, 1;')
npc.add_command('\t\t\tset MISC_QUEST, MISC_QUEST | 1;')
npc.add_command('\t\t\tmes "Great! Here\'s your reward.";')
npc.add_command('\t\t} else {')
npc.add_command('\t\t\tmes "You don\'t have enough!";')
npc.add_command('\t\t}')
npc.add_command('}')
npc.add_command('close;')

gen.add_npc(npc)
print(gen.generate_script())
```

### Example 3: Using DialogBuilder with UI

```python
from rathena_script_ui import DialogBuilder, ScriptValidator
from rathena_script_gen import ScriptGenerator, ScriptNPC

# Build dialog
dialog = DialogBuilder()
dialog.add_message("Welcome to the tutorial!") \
       .add_next_button() \
       .add_message("First, let me check if you have supplies.") \
       .add_item_check(1010, 5) \
       .add_message("Good! You have the items I need.") \
       .add_item_remove(1010, 5) \
       .add_item_give(1012, 1) \
       .add_message("Here's your reward!") \
       .add_close_button()

# Create NPC with dialog
npc = ScriptNPC("Trainer", "prontera", 150, 150)
for cmd in dialog.to_script_commands():
    npc.add_command(cmd)

# Validate
gen = ScriptGenerator()
gen.add_npc(npc)
valid, errors = ScriptValidator.validate_script(gen)

if valid:
    print(gen.generate_script())
else:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
```

### Example 4: Using Templates

```python
from rathena_script_ui import ScriptTemplates

# List all templates
templates = ScriptTemplates.get_all_templates()
for template in templates:
    print(f"- {template['name']}: {template['description']}")

# Get and display template
template = ScriptTemplates.get_template_by_name("Teleporter")
print(template['preview'])
```

---

## Class Diagram

```
ScriptGenerator (Main orchestrator)
├── List[ScriptNPC]
├── List[ScriptFunction]
├── List[ScriptVariable]
└── Callbacks: on_log()

ScriptNPC (Single NPC)
├── properties: name, map, x, y, sprite_id
├── List[commands]
├── on_touch: Optional[List[commands]]
└── on_init: Optional[List[commands]]

ScriptFunction
├── name: str
├── List[commands]
└── return_value: Optional[str]

ScriptVariable
├── name, value, scope, type

DialogBuilder (Fluent API)
├── List[DialogAction]
└── Methods: add_message(), add_menu(), etc.

NPCWizard (Step-by-step guide)
├── Steps: 0-5
└── Callbacks: on_complete(npc)

SimpleEditIntegration (IDE Bridge)
├── Callbacks: on_new_project(), on_export(), etc.
└── Methods: get_status_info()
```

---

## Tips for Best Results

1. **Use QuickScriptBuilders** for common NPC types to save time
2. **Use DialogBuilder** for complex dialogs with proper formatting
3. **Always validate** scripts with ScriptValidator before exporting
4. **Check the guide** for proper syntax and best practices
5. **Use logging callbacks** to debug script generation
6. **Start simple** and gradually add complexity

---

## Troubleshooting

### Script won't generate
- Check that NPC has a valid name and location
- Ensure at least one command is added
- Run validation to see specific errors

### Export fails
- Check file path is writable
- Ensure file path is valid for your OS
- Try using absolute path instead of relative

### Commands not appearing
- Make sure to call `add_command()` method
- Check command syntax matches rAthena format
- Verify commands end with semicolon (;)

---

## Architecture Notes

This package uses a **modular, pluggable architecture** designed for integration:

- **rathena_script_gen.py**: Core logic, framework-agnostic
- **rathena_script_ui.py**: UI helpers, can work with any UI framework
- **Callbacks**: All user interactions use callbacks for flexibility
- **Enums**: Standard enums for constants (NPCType, DialogAction, etc.)
- **Validation**: Separate validator class for error checking

This design allows easy integration with SimpleEdit or any other Python IDE/editor.

---

## License and Attribution

These tools are provided as-is for use with rAthena projects.
Original rAthena documentation adapted for this guide.

---

## Version History

- **1.0** - Initial release with core generator, UI helpers, and comprehensive guide
  - ScriptGenerator and supporting classes
  - DialogBuilder and NPCWizard
  - ScriptValidator
  - SimpleEditIntegration
  - Complete rAthena Script Guide (9 chapters)
