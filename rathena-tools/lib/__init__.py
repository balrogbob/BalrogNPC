"""
rAthena Script Generation Tools Package
Version: 1.0

This package provides a complete toolkit for generating rAthena scripts
programmatically, suitable for integration into IDEs like SimpleEdit.

Main Modules:
    - rathena_script_gen: Core generator engine
    - rathena_script_ui: UI helpers and wizards

Example usage:
    from rathena_script_gen import ScriptGenerator, ScriptNPC
    from rathena_script_ui import DialogBuilder, NPCWizard
    
    gen = ScriptGenerator()
    npc = ScriptNPC("Merchant", "prontera", 150, 150)
    gen.add_npc(npc)
    
    script = gen.generate_script()
"""

__version__ = "1.0.0"
__author__ = "rAthena Tools Developer"
__all__ = [
    # Core Generator
    "ScriptGenerator",
    "ScriptNPC",
    "ScriptFunction",
    "ScriptVariable",
    "ScriptDialog",
    "ScriptCondition",
    "ScriptLoop",
    
    # UI Components
    "DialogBuilder",
    "NPCWizard",
    "ScriptTemplates",
    "ScriptValidator",
    "SimpleEditIntegration",
    
    # Enums
    "NPCSprite",
    "EquipSlot",
    "NPCTypeEnum",
    "DialogActionEnum",
    "LogLevel",
    
    # Builders
    "QuickScriptBuilders",
]

# Import from submodules
from rathena_script_gen import (
    ScriptGenerator,
    ScriptNPC,
    ScriptFunction,
    ScriptVariable,
    ScriptDialog,
    ScriptCondition,
    ScriptLoop,
    NPCSprite,
    EquipSlot,
    QuickScriptBuilders,
    LogLevel,
)

from rathena_script_ui import (
    DialogBuilder,
    NPCWizard,
    ScriptTemplates,
    ScriptValidator,
    SimpleEditIntegration,
    NPCTypeEnum,
    DialogActionEnum,
)


def create_generator(name: str = "script", author: str = "", 
                    description: str = "", log_callback=None) -> ScriptGenerator:
    """
    Convenience function to create a configured ScriptGenerator
    
    Args:
        name: Script name
        author: Author name
        description: Script description
        log_callback: Optional logging callback
        
    Returns:
        Configured ScriptGenerator instance
    """
    gen = ScriptGenerator(log_callback=log_callback)
    gen.set_metadata(name, author, description)
    return gen


def create_npc_from_template(template_name: str, 
                             name: str, 
                             map_name: str, 
                             x: int, 
                             y: int) -> ScriptNPC:
    """
    Create NPC from template
    
    Args:
        template_name: Name of template to use
        name: NPC name
        map_name: Map location
        x, y: Coordinates
        
    Returns:
        ScriptNPC instance or None if template not found
    """
    template = ScriptTemplates.get_template_by_name(template_name)
    if not template:
        return None
    
    npc = ScriptNPC(name, map_name, x, y)
    return npc


__doc__ += """

Quick Start Examples:

Example 1: Create a simple dialog NPC
    >>> gen = create_generator("my_script", "MyName")
    >>> npc = ScriptNPC("Merchant", "prontera", 150, 150)
    >>> npc.add_command('mes "[Merchant]";')
    >>> npc.add_command('mes "Welcome!";')
    >>> npc.add_command('close;')
    >>> gen.add_npc(npc)
    >>> print(gen.generate_script())

Example 2: Use DialogBuilder for complex dialog
    >>> dialog = DialogBuilder()
    >>> dialog.add_message("Hello!") \\
    ...       .add_next_button() \\
    ...       .add_message("How can I help?") \\
    ...       .add_close_button()
    >>> commands = dialog.to_script_commands()

Example 3: Use NPCWizard for guided creation
    >>> def on_complete(npc):
    ...     print(f"Created {npc.name}")
    >>> wizard = NPCWizard(on_complete)
    >>> wizard.set_npc_basic_info("Trainer", "prontera", 150, 150)
    >>> wizard.next_step()

Example 4: Validate before export
    >>> gen = create_generator("test")
    >>> gen.add_npc(npc)
    >>> valid, errors = ScriptValidator.validate_script(gen)
    >>> if valid:
    ...     gen.export_script("output.txt")
"""
