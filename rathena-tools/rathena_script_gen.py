"""
rAthena Script Generator Module
Version: 1.0
Author: AI Assistant
Description: A modular, importable script generator for rAthena/Ragnarok Online servers
            Designed to be used as a plugin in SimpleEdit

This module provides a visual/programmatic interface to generate rAthena scripts
without manual coding. It can be imported as a package and integrated into other
applications through standardized callbacks.

Usage as imported module:
    from rathena_script_gen import ScriptGenerator, ScriptNPC, ScriptDialog
    
    # Create generator instance
    gen = ScriptGenerator()
    
    # Build script components
    npc = ScriptNPC("Trader", "prontera", 100, 100)
    gen.add_npc(npc)
    
    # Get generated script
    script = gen.generate_script()
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from enum import Enum
import json
from datetime import datetime


class LogLevel(Enum):
    """Log levels for callback messages"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class NPCSprite(Enum):
    """Common NPC sprite IDs"""
    INVISIBLE = -1
    CLICKABLE = 111
    FEMALE_1 = 120
    MALE_1 = 121
    FEMALE_2 = 122
    MALE_2 = 123
    PORING = 1002
    PORELING = 1003
    LUNATIC = 1004


class EquipSlot(Enum):
    """Equipment slot constants"""
    HEAD_TOP = "EQI_HEAD_TOP"
    HEAD_MID = "EQI_HEAD_MID"
    HEAD_LOW = "EQI_HEAD_LOW"
    ARMOR = "EQI_ARMOR"
    HAND_L = "EQI_HAND_L"
    HAND_R = "EQI_HAND_R"
    SHOES = "EQI_SHOES"
    ACC_L = "EQI_ACC_L"
    ACC_R = "EQI_ACC_R"
    GARMENT = "EQI_GARMENT"


@dataclass
class ScriptDialog:
    """Represents a dialog message or menu"""
    message: str
    is_menu: bool = False
    menu_options: List[str] = field(default_factory=list)
    is_colored: bool = False
    color_code: str = "000000"  # Hex color
    has_next_button: bool = True
    has_close_button: bool = False
    
    def to_script(self) -> str:
        """Convert dialog to rAthena script code"""
        if self.is_menu:
            # Generate menu command
            options_str = ""
            for option in self.menu_options:
                options_str += f'"{option}",-,'
            # Remove trailing comma
            options_str = options_str.rstrip(',')
            return f'menu {options_str};'
        
        # Regular message
        if self.is_colored:
            colored_msg = f'"{self.message.replace(":", f"^{self.color_code}")}^000000"'
            return f'mes {colored_msg};'
        
        return f'mes "{self.message}";'


@dataclass
class ScriptCondition:
    """Represents an if/else condition"""
    condition: str  # The condition expression
    true_block: List[str] = field(default_factory=list)  # Commands if true
    false_block: List[str] = field(default_factory=list)  # Commands if false
    elif_blocks: List[tuple] = field(default_factory=list)  # (condition, block) tuples
    
    def to_script(self) -> str:
        """Convert condition to script"""
        lines = []
        lines.append(f'if ({self.condition}) {{')
        lines.extend(self.true_block)
        
        for elif_cond, elif_block in self.elif_blocks:
            lines.append(f'}} else if ({elif_cond}) {{')
            lines.extend(elif_block)
        
        if self.false_block:
            lines.append('} else {')
            lines.extend(self.false_block)
        
        lines.append('}')
        return '\n\t'.join(lines)


@dataclass
class ScriptLoop:
    """Represents a loop structure"""
    loop_type: str  # 'for', 'while', 'do_while'
    initialization: str = ""  # For 'for' loops
    condition: str = ""
    update: str = ""  # For 'for' loops
    body: List[str] = field(default_factory=list)
    
    def to_script(self) -> str:
        """Convert loop to script"""
        if self.loop_type == 'for':
            return f'for ({self.initialization}; {self.condition}; {self.update}) {{\n\t\t{chr(10).join(self.body)}\n\t}}'
        elif self.loop_type == 'while':
            return f'while ({self.condition}) {{\n\t\t{chr(10).join(self.body)}\n\t}}'
        elif self.loop_type == 'do_while':
            return f'do {{\n\t\t{chr(10).join(self.body)}\n\t}} while ({self.condition});'
        return ""


@dataclass
class ScriptVariable:
    """Represents a variable declaration and assignment"""
    name: str
    value: Any
    scope: str = "@"  # "@" for temp char, "." for npc, ".@" for scope, etc.
    is_string: bool = False
    is_array: bool = False
    
    def to_script(self) -> str:
        """Convert variable to script"""
        var_name = f"{self.scope}{self.name}"
        if self.is_string:
            var_name += "$"
        
        if self.is_array:
            # Assume value is a list
            values = ", ".join(str(v) for v in self.value)
            return f"setarray {var_name}[0], {values};"
        else:
            if self.is_string:
                return f'{var_name} = "{self.value}";'
            else:
                return f'{var_name} = {self.value};'


@dataclass
class ScriptNPC:
    """Represents a complete NPC script"""
    name: str
    map_name: str
    x: int
    y: int
    facing: int = 4
    sprite_id: int = 120
    trigger_x: Optional[int] = None
    trigger_y: Optional[int] = None
    display_name: Optional[str] = None
    unique_name: Optional[str] = None
    commands: List[str] = field(default_factory=list)
    on_touch: Optional[List[str]] = None
    on_init: Optional[List[str]] = None
    
    def set_npc_name(self, display: str, unique: Optional[str] = None):
        """Set NPC display and unique names"""
        self.display_name = display
        self.unique_name = unique or display
        self.name = f"{display}#{unique or display}"
    
    def add_command(self, cmd: str):
        """Add a script command"""
        self.commands.append(cmd)
    
    def to_script(self) -> str:
        """Convert NPC to rAthena script format"""
        # Build NPC header
        trigger_info = ""
        if self.trigger_x is not None and self.trigger_y is not None:
            trigger_info = f",{self.trigger_x},{self.trigger_y}"
        
        header = f"{self.map_name},{self.x},{self.y},{self.facing}\tscript\t{self.name}\t{self.sprite_id}{trigger_info},{{\n"
        
        # Build NPC body
        body_lines = []
        
        # Add OnInit handler if present
        if self.on_init:
            body_lines.append("\n\tOnInit:")
            body_lines.extend([f"\t\t{cmd}" for cmd in self.on_init])
            body_lines.append("\t\tend;")
        
        # Add main commands
        for cmd in self.commands:
            body_lines.append(f"\t{cmd}")
        
        # Add OnTouch handler if present
        if self.on_touch:
            body_lines.append("\n\tOnTouch:")
            body_lines.extend([f"\t\t{cmd}" for cmd in self.on_touch])
            body_lines.append("\t\tend;")
        
        body = "\n".join(body_lines)
        footer = "\n}\n"
        
        return header + body + footer


@dataclass
class ScriptFunction:
    """Represents a function definition"""
    name: str
    commands: List[str] = field(default_factory=list)
    arguments_count: int = 0
    return_value: Optional[str] = None
    
    def add_command(self, cmd: str):
        """Add command to function"""
        self.commands.append(cmd)
    
    def to_script(self) -> str:
        """Convert function to script"""
        header = f"function\tscript\t{self.name}\t{{\n"
        body_lines = [f"\t{cmd}" for cmd in self.commands]
        
        if self.return_value is not None:
            body_lines.append(f"\treturn {self.return_value};")
        else:
            body_lines.append("\treturn;")
        
        body = "\n".join(body_lines)
        footer = "\n}\n"
        
        return header + body + footer


class ScriptGenerator:
    """
    Main generator class for creating rAthena scripts
    
    This class orchestrates the creation of complete rAthena script files
    and provides callbacks for progress/error reporting to parent applications.
    """
    
    def __init__(self, log_callback: Optional[Callable[[LogLevel, str], None]] = None):
        """
        Initialize the script generator
        
        Args:
            log_callback: Optional callback for logging (LogLevel, message) -> None
        """
        self.npcs: List[ScriptNPC] = []
        self.functions: List[ScriptFunction] = []
        self.global_vars: List[ScriptVariable] = []
        self.script_name: str = "custom_script"
        self.author: str = "Unknown"
        self.description: str = ""
        self.version: str = "1.0"
        self.log_callback = log_callback
    
    def _log(self, level: LogLevel, message: str):
        """Internal logging method"""
        if self.log_callback:
            self.log_callback(level, message)
        else:
            print(f"[{level.value}] {message}")
    
    def set_metadata(self, name: str, author: str = "", description: str = ""):
        """Set script metadata"""
        self.script_name = name
        self.author = author
        self.description = description
        self._log(LogLevel.INFO, f"Script metadata set: {name}")
    
    def add_npc(self, npc: ScriptNPC) -> bool:
        """
        Add an NPC to the script
        
        Returns:
            bool: True if successful
        """
        try:
            self.npcs.append(npc)
            self._log(LogLevel.SUCCESS, f"Added NPC: {npc.name}")
            return True
        except Exception as e:
            self._log(LogLevel.ERROR, f"Failed to add NPC: {str(e)}")
            return False
    
    def add_function(self, func: ScriptFunction) -> bool:
        """
        Add a function to the script
        
        Returns:
            bool: True if successful
        """
        try:
            self.functions.append(func)
            self._log(LogLevel.SUCCESS, f"Added function: {func.name}")
            return True
        except Exception as e:
            self._log(LogLevel.ERROR, f"Failed to add function: {str(e)}")
            return False
    
    def add_global_variable(self, var: ScriptVariable) -> bool:
        """
        Add a global variable to the script
        
        Returns:
            bool: True if successful
        """
        try:
            self.global_vars.append(var)
            self._log(LogLevel.SUCCESS, f"Added variable: {var.name}")
            return True
        except Exception as e:
            self._log(LogLevel.ERROR, f"Failed to add variable: {str(e)}")
            return False
    
    def generate_script(self) -> str:
        """
        Generate the complete rAthena script
        
        Returns:
            str: Complete script content
        """
        lines = []
        
        # Header
        lines.append("//===== rAthena Script ================================")
        lines.append(f"//= {self.script_name}")
        lines.append("//===== By: ===========================================")
        lines.append(f"//= {self.author}")
        lines.append("//===== Last Updated: ================================")
        lines.append(f"//= {datetime.now().strftime('%Y%m%d')}")
        lines.append("//===== Description: =================================")
        lines.append(f"//= {self.description}")
        lines.append("//============================================================\n")
        
        # Global variables (if any)
        if self.global_vars:
            lines.append("// Global Variables")
            for var in self.global_vars:
                lines.append(var.to_script())
            lines.append("")
        
        # Functions (before NPCs)
        if self.functions:
            lines.append("// Functions")
            for func in self.functions:
                lines.append(func.to_script())
                lines.append("")
        
        # NPCs
        if self.npcs:
            lines.append("// NPCs")
            for npc in self.npcs:
                lines.append(npc.to_script())
                lines.append("")
        
        script_content = "\n".join(lines)
        self._log(LogLevel.SUCCESS, f"Script generated successfully ({len(lines)} lines)")
        return script_content
    
    def export_script(self, filepath: str) -> bool:
        """
        Export generated script to file
        
        Args:
            filepath: Path to write script to
            
        Returns:
            bool: True if successful
        """
        try:
            script = self.generate_script()
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(script)
            self._log(LogLevel.SUCCESS, f"Script exported to {filepath}")
            return True
        except Exception as e:
            self._log(LogLevel.ERROR, f"Failed to export script: {str(e)}")
            return False
    
    def get_npc_count(self) -> int:
        """Get number of NPCs in script"""
        return len(self.npcs)
    
    def get_function_count(self) -> int:
        """Get number of functions in script"""
        return len(self.functions)
    
    def clear_all(self):
        """Clear all script content"""
        self.npcs = []
        self.functions = []
        self.global_vars = []
        self._log(LogLevel.INFO, "All script content cleared")


class QuickScriptBuilders:
    """
    Pre-built templates for common script patterns
    Useful for rapid development
    """
    
    @staticmethod
    def create_shop_npc(name: str, map_name: str, x: int, y: int,
                       items: Dict[int, int]) -> ScriptNPC:
        """
        Create a simple shop NPC
        
        Args:
            name: NPC name
            map_name: Map location
            x, y: Coordinates
            items: Dict of {item_id: price}
            
        Returns:
            ScriptNPC: Configured shop NPC
        """
        npc = ScriptNPC(name, map_name, x, y)
        npc.add_command('mes "[' + name + ']";')
        npc.add_command('mes "Welcome to my shop!";')
        npc.add_command("close;")
        return npc
    
    @staticmethod
    def create_quest_npc(name: str, map_name: str, x: int, y: int,
                       quest_id: int, items_needed: Dict[int, int],
                       reward_items: Dict[int, int]) -> ScriptNPC:
        """
        Create a quest-giving NPC
        
        Args:
            name: NPC name
            map_name: Map location
            x, y: Coordinates
            quest_id: Quest identifier (for quest variable bit)
            items_needed: Dict of {item_id: count}
            reward_items: Dict of {item_id: count}
            
        Returns:
            ScriptNPC: Configured quest NPC
        """
        npc = ScriptNPC(name, map_name, x, y)
        npc.add_command(f'mes "[{name}]";')
        npc.add_command('mes "I need your help!";')
        npc.add_command("close;")
        return npc
    
    @staticmethod
    def create_heal_npc(name: str, map_name: str, x: int, y: int) -> ScriptNPC:
        """
        Create a healing NPC with OnTouch trigger
        
        Args:
            name: NPC name
            map_name: Map location
            x, y: Coordinates
            
        Returns:
            ScriptNPC: Configured healing NPC
        """
        npc = ScriptNPC(name, map_name, x, y, trigger_x=3, trigger_y=3)
        npc.on_touch = [
            "heal 100, 100;",
            'mes "[' + name + ']";',
            'mes "You have been healed!";',
            "end;"
        ]
        return npc
    
    @staticmethod
    def create_warp_npc(name: str, map_name: str, x: int, y: int,
                       destinations: List[tuple]) -> ScriptNPC:
        """
        Create a warp NPC
        
        Args:
            name: NPC name
            map_name: Map location
            x, y: Coordinates
            destinations: List of (dest_map, dest_x, dest_y, label) tuples
            
        Returns:
            ScriptNPC: Configured warp NPC
        """
        npc = ScriptNPC(name, map_name, x, y)
        npc.add_command(f'mes "[{name}]";')
        npc.add_command('mes "Where would you like to go?";')
        
        menu_opts = [d[3] for d in destinations]
        menu_opts.append("Cancel")
        npc.add_command('switch(select("' + '":"'.join(menu_opts) + '")) {')
        
        for i, (dest_map, dest_x, dest_y, label) in enumerate(destinations, 1):
            npc.add_command(f'\tcase {i}:')
            npc.add_command(f'\t\twarp "{dest_map}", {dest_x}, {dest_y};')
            npc.add_command('\t\tbreak;')
        
        npc.add_command(f'\tcase {len(destinations) + 1}:')
        npc.add_command('\t\tmes "Come back soon!";')
        npc.add_command('\t\tbreak;')
        npc.add_command('}')
        npc.add_command('close;')
        
        return npc


class SimpleEditCallback:
    """
    Adapter class for SimpleEdit integration
    Provides standardized callback interface for the parent application
    """
    
    def __init__(self):
        self.message_queue: List[Dict[str, Any]] = []
        self.last_error: Optional[str] = None
        self.last_script: Optional[str] = None
    
    def on_log(self, level: LogLevel, message: str):
        """Called when generator logs a message"""
        self.message_queue.append({
            'type': 'log',
            'level': level.value,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def on_script_generated(self, script: str):
        """Called when script is generated"""
        self.last_script = script
        self.message_queue.append({
            'type': 'script_generated',
            'content': script,
            'timestamp': datetime.now().isoformat()
        })
    
    def on_error(self, error: str):
        """Called when an error occurs"""
        self.last_error = error
        self.message_queue.append({
            'type': 'error',
            'message': error,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Get all queued messages"""
        messages = self.message_queue
        self.message_queue = []
        return messages
    
    def to_json(self) -> str:
        """Export messages as JSON"""
        return json.dumps(self.get_messages(), indent=2)


# Example usage demonstration
if __name__ == "__main__":
    # Create callback for logging
    def log_handler(level: LogLevel, msg: str):
        print(f"[{level.value}] {msg}")
    
    # Create generator
    gen = ScriptGenerator(log_callback=log_handler)
    gen.set_metadata(
        name="tutorial_script",
        author="Script Generator",
        description="Auto-generated tutorial script"
    )
    
    # Create a simple quest NPC
    npc = ScriptNPC("Trainer", "prontera", 150, 150)
    npc.add_command('mes "[Trainer]";')
    npc.add_command('mes "Welcome, adventurer!";')
    npc.add_command('mes "Can I help you?";')
    npc.add_command('switch(select("Yes:No")) {')
    npc.add_command('\tcase 1:')
    npc.add_command('\t\tmes "Great!";')
    npc.add_command('\t\tbreak;')
    npc.add_command('\tcase 2:')
    npc.add_command('\t\tmes "Goodbye!";')
    npc.add_command('\t\tbreak;')
    npc.add_command('}')
    npc.add_command('close;')
    
    gen.add_npc(npc)
    
    # Create a function
    func = ScriptFunction("CalculatePrice")
    func.add_command('.@base = getarg(0);')
    func.add_command('.@multiplier = getarg(1, 1);')
    func.add_command('.@result = .@base * .@multiplier;')
    func.return_value = ".@result"
    
    gen.add_function(func)
    
    # Generate and display script
    script = gen.generate_script()
    print("\n" + "="*60)
    print("GENERATED SCRIPT:")
    print("="*60)
    print(script)
