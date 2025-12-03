"""
rAthena Script Generator - UI Helper Module
Version: 1.0

This module provides UI building blocks and wizards for creating rAthena scripts
through a visual interface. It can be integrated into SimpleEdit or other IDEs.

Classes in this module are designed to be used with various UI frameworks
(PyQt, Tkinter, etc.) through abstract methods that need implementation.
"""

from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import json

from rathena_script_gen import (
    ScriptGenerator, ScriptNPC, ScriptFunction, ScriptVariable,
    ScriptDialog, ScriptCondition, QuickScriptBuilders, LogLevel
)


class NPCTypeEnum(Enum):
    """Types of NPCs that can be created"""
    DIALOG = "Dialog NPC"
    SHOP = "Shop Keeper"
    QUEST_GIVER = "Quest Giver"
    HEALER = "Healer"
    TELEPORTER = "Teleporter"
    CUSTOM = "Custom Script"


class DialogActionEnum(Enum):
    """Actions available in dialogs"""
    MESSAGE = "Display Message"
    NEXT_BUTTON = "Show Next Button"
    CLOSE_BUTTON = "Show Close Button"
    MENU = "Show Menu"
    INPUT = "Get Input"
    ITEM_CHECK = "Check Item"
    ITEM_GIVE = "Give Item"
    ITEM_REMOVE = "Remove Item"
    CONDITION = "If Condition"
    WARP = "Warp Player"


@dataclass
class DialogAction:
    """Represents a single dialog action"""
    action_type: DialogActionEnum
    parameters: Dict[str, Any]
    
    def to_script_command(self) -> str:
        """Convert action to script command"""
        if self.action_type == DialogActionEnum.MESSAGE:
            msg = self.parameters.get('message', '')
            # Handle script commands (prefixed with {SCRIPT})
            if msg.startswith('{SCRIPT}'):
                return msg[8:]  # Return raw command without prefix
            return f'mes "{msg}";'
        
        elif self.action_type == DialogActionEnum.NEXT_BUTTON:
            return 'next;'
        
        elif self.action_type == DialogActionEnum.CLOSE_BUTTON:
            return 'close;'
        
        elif self.action_type == DialogActionEnum.MENU:
            options = self.parameters.get('options', [])
            branches = self.parameters.get('branches', {})
            opts_str = '":"'.join(options)
            
            # If no branches, just return the select command
            if not branches:
                return f'select("{opts_str}");'
            
            # Generate switch/case structure for branches
            lines = [f'switch(select("{opts_str}")) {{']
            for idx, opt in enumerate(options, 1):
                lines.append(f'\tcase {idx}:')
                if opt in branches:
                    # Parse branch content (simple line-by-line)
                    branch_content = branches[opt]
                    for line in branch_content.split('\n'):
                        line = line.strip()
                        if not line:
                            continue
                        if line.lower() == 'next':
                            lines.append('\t\tnext;')
                        elif line.lower() == 'close':
                            lines.append('\t\tclose;')
                        elif line.lower() == 'break':
                            lines.append('\t\tbreak;')
                        else:
                            # Assume it's a message or command
                            if line.startswith('"') or line.endswith(';'):
                                lines.append(f'\t\t{line}')
                            else:
                                lines.append(f'\t\tmes "{line}";')
                lines.append('\t\tbreak;')
            lines.append('}')
            return '\n'.join(lines)
        
        elif self.action_type == DialogActionEnum.ITEM_CHECK:
            item_id = self.parameters.get('item_id', 0)
            count = self.parameters.get('count', 1)
            return f'if (countitem({item_id}) < {count})'
        
        elif self.action_type == DialogActionEnum.ITEM_GIVE:
            item_id = self.parameters.get('item_id', 0)
            amount = self.parameters.get('amount', 1)
            return f'getitem {item_id}, {amount};'
        
        elif self.action_type == DialogActionEnum.ITEM_REMOVE:
            item_id = self.parameters.get('item_id', 0)
            amount = self.parameters.get('amount', 1)
            return f'delitem {item_id}, {amount};'
        
        elif self.action_type == DialogActionEnum.WARP:
            map_name = self.parameters.get('map', 'prontera')
            x = self.parameters.get('x', 150)
            y = self.parameters.get('y', 150)
            return f'warp "{map_name}", {x}, {y};'
        
        return "// Unknown action"


class UIComponent(ABC):
    """
    Abstract base class for UI components
    Subclasses should implement these methods for specific UI frameworks
    """
    
    @abstractmethod
    def render(self) -> Any:
        """Render the component for the UI framework"""
        pass
    
    @abstractmethod
    def get_value(self) -> Any:
        """Get current value from component"""
        pass
    
    @abstractmethod
    def set_value(self, value: Any):
        """Set value for component"""
        pass


class NPCWizard:
    """
    Interactive wizard for creating NPCs
    Guides users through NPC creation step-by-step
    """
    
    def __init__(self, on_complete: Callable[[ScriptNPC], None]):
        """
        Initialize wizard
        
        Args:
            on_complete: Callback when NPC is created
        """
        self.on_complete = on_complete
        self.current_step = 0
        self.npc_data = {
            'name': '',
            'map': 'prontera',
            'x': 150,
            'y': 150,
            'sprite': 120,
            'type': NPCTypeEnum.DIALOG,
            'dialog_actions': []
        }
    
    def get_current_step(self) -> int:
        """Get current step number"""
        return self.current_step
    
    def get_step_count(self) -> int:
        """Get total steps required"""
        return 5
    
    def get_step_title(self) -> str:
        """Get title for current step"""
        steps = [
            "NPC Name and Location",
            "Appearance",
            "NPC Type",
            "Dialog/Interactions",
            "Confirmation"
        ]
        return steps[self.current_step] if self.current_step < len(steps) else "Complete"
    
    def get_step_description(self) -> str:
        """Get description for current step"""
        descriptions = {
            0: "Choose a name for your NPC and where to place them",
            1: "Select the NPC's appearance (sprite)",
            2: "Choose what type of NPC this will be",
            3: "Define the NPC's dialog and interactions",
            4: "Review and confirm the NPC configuration"
        }
        return descriptions.get(self.current_step, "")
    
    def next_step(self) -> bool:
        """Move to next step. Returns False if at end"""
        if self.current_step < self.get_step_count() - 1:
            self.current_step += 1
            return True
        else:
            self._finish()
            return False
    
    def previous_step(self) -> bool:
        """Move to previous step. Returns False if at start"""
        if self.current_step > 0:
            self.current_step -= 1
            return True
        return False
    
    def set_npc_basic_info(self, name: str, map_name: str, x: int, y: int):
        """Set basic NPC information"""
        self.npc_data['name'] = name
        self.npc_data['map'] = map_name
        self.npc_data['x'] = x
        self.npc_data['y'] = y
    
    def set_npc_appearance(self, sprite_id: int):
        """Set NPC sprite"""
        self.npc_data['sprite'] = sprite_id
    
    def set_npc_type(self, npc_type: NPCTypeEnum):
        """Set NPC type"""
        self.npc_data['type'] = npc_type
    
    def add_dialog_action(self, action: DialogAction):
        """Add dialog action"""
        self.npc_data['dialog_actions'].append(action)
    
    def _finish(self):
        """Build and return final NPC"""
        npc = ScriptNPC(
            self.npc_data['name'],
            self.npc_data['map'],
            self.npc_data['x'],
            self.npc_data['y'],
            sprite_id=self.npc_data['sprite']
        )
        
        # Add commands from dialog actions
        for action in self.npc_data['dialog_actions']:
            npc.add_command(action.to_script_command())
        
        self.on_complete(npc)
    
    def get_summary(self) -> str:
        """Get text summary of NPC"""
        return f"""
NPC Name: {self.npc_data['name']}
Location: {self.npc_data['map']} ({self.npc_data['x']}, {self.npc_data['y']})
Type: {self.npc_data['type'].value}
Sprite ID: {self.npc_data['sprite']}
Dialog Actions: {len(self.npc_data['dialog_actions'])}
        """


class DialogBuilder:
    """
    Visual dialog builder
    Creates dialog sequences for NPCs
    """
    
    def __init__(self):
        self.actions: List[DialogAction] = []
    
    def add_message(self, message: str) -> 'DialogBuilder':
        """Add a message display action"""
        action = DialogAction(
            DialogActionEnum.MESSAGE,
            {'message': message}
        )
        self.actions.append(action)
        return self
    
    def add_next_button(self) -> 'DialogBuilder':
        """Add next button"""
        action = DialogAction(DialogActionEnum.NEXT_BUTTON, {})
        self.actions.append(action)
        return self
    
    def add_close_button(self) -> 'DialogBuilder':
        """Add close button"""
        action = DialogAction(DialogActionEnum.CLOSE_BUTTON, {})
        self.actions.append(action)
        return self
    
    def add_menu(self, options: List[str]) -> 'DialogBuilder':
        """Add menu with options"""
        action = DialogAction(
            DialogActionEnum.MENU,
            {'options': options}
        )
        self.actions.append(action)
        return self
    
    def add_item_check(self, item_id: int, required_count: int = 1) -> 'DialogBuilder':
        """Add item count check"""
        action = DialogAction(
            DialogActionEnum.ITEM_CHECK,
            {'item_id': item_id, 'count': required_count}
        )
        self.actions.append(action)
        return self
    
    def add_item_give(self, item_id: int, amount: int = 1) -> 'DialogBuilder':
        """Add give item action"""
        action = DialogAction(
            DialogActionEnum.ITEM_GIVE,
            {'item_id': item_id, 'amount': amount}
        )
        self.actions.append(action)
        return self
    
    def add_item_remove(self, item_id: int, amount: int = 1) -> 'DialogBuilder':
        """Add remove item action"""
        action = DialogAction(
            DialogActionEnum.ITEM_REMOVE,
            {'item_id': item_id, 'amount': amount}
        )
        self.actions.append(action)
        return self
    
    def add_warp(self, map_name: str, x: int, y: int) -> 'DialogBuilder':
        """Add warp action"""
        action = DialogAction(
            DialogActionEnum.WARP,
            {'map': map_name, 'x': x, 'y': y}
        )
        self.actions.append(action)
        return self
    
    def get_actions(self) -> List[DialogAction]:
        """Get all actions"""
        return self.actions
    
    def to_script_commands(self) -> List[str]:
        """Convert all actions to script commands"""
        return [action.to_script_command() for action in self.actions]
    
    def clear(self):
        """Clear all actions"""
        self.actions = []


class ScriptTemplates:
    """
    Collection of pre-defined script templates
    Users can choose templates as starting points
    """
    
    TEMPLATE_SHOP = {
        'name': 'Simple Shop',
        'description': 'A basic shop NPC that sells items',
        'type': NPCTypeEnum.SHOP,
        'preview': '''
prontera,100,100,4	script	Shopkeeper	120,{
    mes "[Shopkeeper]";
    mes "Welcome! Check out my wares!";
    close;
}
        '''
    }
    
    TEMPLATE_QUEST = {
        'name': 'Quest Giver',
        'description': 'An NPC that gives quests with rewards',
        'type': NPCTypeEnum.QUEST_GIVER,
        'preview': '''
prontera,100,100,4	script	Master	120,{
    if (QUEST_VAR & 1) {
        mes "[Master]";
        mes "Good job completing my task!";
        close;
    }
    
    mes "[Master]";
    mes "I have an important task for you!";
    
    if (select("Accept:Decline") == 1) {
        mes "Great! Go forth!";
        set QUEST_VAR, QUEST_VAR | 1;
    }
    close;
}
        '''
    }
    
    TEMPLATE_HEALER = {
        'name': 'Healer NPC',
        'description': 'Heals nearby players automatically',
        'type': NPCTypeEnum.HEALER,
        'preview': '''
prontera,100,100,4	script	Healer	120,3,3,{
    OnTouch:
        heal 100, 100;
        mes "[Healer]";
        mes "You've been restored!";
        end;
}
        '''
    }
    
    TEMPLATE_TELEPORTER = {
        'name': 'Teleporter',
        'description': 'Warps players to different locations',
        'type': NPCTypeEnum.TELEPORTER,
        'preview': '''
prontera,100,100,4	script	Porter	120,{
    mes "[Porter]";
    mes "Where would you like to go?";
    
    switch(select("Geffen:Payon:Izlude:Cancel")) {
        case 1:
            warp "geffen", 119, 59;
            break;
        case 2:
            warp "payon", 161, 247;
            break;
        case 3:
            warp "izlude", 128, 114;
            break;
    }
    close;
}
        '''
    }
    
    @classmethod
    def get_all_templates(cls) -> List[Dict[str, Any]]:
        """Get all available templates"""
        return [
            cls.TEMPLATE_SHOP,
            cls.TEMPLATE_QUEST,
            cls.TEMPLATE_HEALER,
            cls.TEMPLATE_TELEPORTER
        ]
    
    @classmethod
    def get_template_by_name(cls, name: str) -> Optional[Dict[str, Any]]:
        """Get template by name"""
        for template in cls.get_all_templates():
            if template['name'] == name:
                return template
        return None


class ScriptValidator:
    """
    Validates script components before generation
    Catches common errors early
    """
    
    @staticmethod
    def validate_npc(npc: ScriptNPC) -> tuple[bool, List[str]]:
        """
        Validate NPC configuration
        
        Returns:
            (is_valid, error_list)
        """
        errors = []
        
        if not npc.name or len(npc.name) == 0:
            errors.append("NPC must have a name")
        
        if len(npc.name) > 24:
            errors.append("NPC name cannot exceed 24 characters")
        
        if not npc.map_name or len(npc.map_name) == 0:
            errors.append("NPC must have a map location")
        
        if npc.x < 0 or npc.y < 0:
            errors.append("NPC coordinates cannot be negative")
        
        if npc.sprite_id < -1:
            errors.append("Invalid sprite ID")
        
        if not npc.commands and not npc.on_touch:
            errors.append("NPC must have at least one command or OnTouch handler")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_function(func: ScriptFunction) -> tuple[bool, List[str]]:
        """
        Validate function configuration
        
        Returns:
            (is_valid, error_list)
        """
        errors = []
        
        if not func.name or len(func.name) == 0:
            errors.append("Function must have a name")
        
        if not func.name.isidentifier():
            errors.append("Function name must be a valid identifier")
        
        if not func.commands and func.return_value is None:
            errors.append("Function must have at least one command or return value")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_script(generator: ScriptGenerator) -> tuple[bool, List[str]]:
        """
        Validate complete script
        
        Returns:
            (is_valid, error_list)
        """
        errors = []
        
        if generator.get_npc_count() == 0 and generator.get_function_count() == 0:
            errors.append("Script must contain at least one NPC or function")
        
        # Validate all NPCs
        for npc in generator.npcs:
            valid, npc_errors = ScriptValidator.validate_npc(npc)
            if not valid:
                errors.extend([f"{npc.name}: {err}" for err in npc_errors])
        
        # Validate all functions
        for func in generator.functions:
            valid, func_errors = ScriptValidator.validate_function(func)
            if not valid:
                errors.extend([f"{func.name}: {err}" for err in func_errors])
        
        return len(errors) == 0, errors


class SimpleEditIntegration:
    """
    Integration helper for SimpleEdit
    Provides standard callbacks and data exchange methods
    """
    
    def __init__(self, generator: ScriptGenerator):
        self.generator = generator
        self.last_exported_path: Optional[str] = None
    
    def on_new_project(self) -> bool:
        """Called when user creates new script project"""
        self.generator.clear_all()
        return True
    
    def on_open_project(self, data: Dict[str, Any]) -> bool:
        """
        Called when user opens script project
        
        Args:
            data: Serialized project data
            
        Returns:
            bool: Success
        """
        try:
            # This would deserialize the project from JSON
            # Implementation depends on data format
            return True
        except Exception as e:
            print(f"Error opening project: {e}")
            return False
    
    def on_save_project(self) -> Dict[str, Any]:
        """
        Called when user saves script project
        
        Returns:
            Serialized project data
        """
        return {
            'npcs': len(self.generator.npcs),
            'functions': len(self.generator.functions),
            'metadata': {
                'name': self.generator.script_name,
                'author': self.generator.author,
                'description': self.generator.description
            }
        }
    
    def on_export(self, filepath: str) -> bool:
        """
        Called when user exports script
        
        Args:
            filepath: Destination file path
            
        Returns:
            bool: Success
        """
        success = self.generator.export_script(filepath)
        if success:
            self.last_exported_path = filepath
        return success
    
    def on_preview(self) -> str:
        """
        Called when user previews script
        
        Returns:
            Generated script content
        """
        return self.generator.generate_script()
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get current status information"""
        return {
            'npcs': self.generator.get_npc_count(),
            'functions': self.generator.get_function_count(),
            'script_name': self.generator.script_name,
            'author': self.generator.author,
            'last_exported': self.last_exported_path
        }


if __name__ == "__main__":
    # Example: Using the dialog builder
    builder = DialogBuilder()
    builder.add_message("Hello, adventurer!") \
            .add_next_button() \
            .add_message("I have a task for you.") \
            .add_menu(["Accept", "Decline"]) \
            .add_close_button()
    
    print("Dialog Commands:")
    for cmd in builder.to_script_commands():
        print(f"  {cmd}")
    
    # Example: Using the NPC wizard
    def on_wizard_complete(npc: ScriptNPC):
        print(f"\nNPC Created: {npc.name}")
        print(f"Location: {npc.map_name} ({npc.x}, {npc.y})")
        print(f"Commands: {len(npc.commands)}")
    
    wizard = NPCWizard(on_wizard_complete)
    print(f"\nWizard: {wizard.get_step_title()}")
    print(wizard.get_step_description())
    
    # Example: Script validation
    gen = ScriptGenerator()
    gen.set_metadata("test_script", "Test Author")
    
    test_npc = ScriptNPC("TestNPC", "prontera", 100, 100)
    test_npc.add_command('mes "Hello";')
    test_npc.add_command('close;')
    
    gen.add_npc(test_npc)
    
    valid, errors = ScriptValidator.validate_script(gen)
    print(f"\nScript Validation: {'PASS' if valid else 'FAIL'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
