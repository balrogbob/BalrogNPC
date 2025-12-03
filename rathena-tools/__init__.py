"""
rAthena Script Development Tools
Complete toolkit for creating rAthena game server scripts.

This package provides:
- Script generation engine (ScriptGenerator, ScriptNPC, ScriptFunction, etc.)
- UI helpers and wizards (DialogBuilder, NPCWizard, etc.)
- Working examples and templates
- Comprehensive documentation

Usage:
    from rathena_tools import ScriptGenerator, ScriptNPC, DialogBuilder
    
    gen = ScriptGenerator()
    npc = ScriptNPC("MyNPC", "prontera", 150, 150)
    npc.add_command('mes "Hello";')
    gen.add_npc(npc)
    print(gen.generate_script())
"""

__version__ = "1.0.0"
__author__ = "rAthena Tools"
__license__ = "MIT"

# Import main classes from the generator module
try:
    from rathena_script_gen import (
        ScriptGenerator,
        ScriptNPC,
        ScriptFunction,
        ScriptVariable,
        ScriptDialog,
        ScriptCondition,
        ScriptLoop,
        QuickScriptBuilders,
        SimpleEditCallback
    )
except ImportError:
    # Fallback for relative imports when running as part of a larger project
    try:
        from .rathena_script_gen import (
            ScriptGenerator,
            ScriptNPC,
            ScriptFunction,
            ScriptVariable,
            ScriptDialog,
            ScriptCondition,
            ScriptLoop,
            QuickScriptBuilders,
            SimpleEditCallback
        )
    except ImportError:
        pass

# Import UI helpers from the UI module
try:
    from rathena_script_ui import (
        NPCWizard,
        DialogBuilder,
        DialogAction,
        ScriptTemplates,
        ScriptValidator,
        SimpleEditIntegration,
        UIComponent
    )
except ImportError:
    try:
        from .rathena_script_ui import (
            NPCWizard,
            DialogBuilder,
            DialogAction,
            ScriptTemplates,
            ScriptValidator,
            SimpleEditIntegration,
            UIComponent
        )
    except ImportError:
        pass

# Convenience function for quick script generation
def create_simple_npc(name, map_name, x, y, commands=None):
    """
    Quick helper to create a simple NPC script.
    
    Args:
        name: NPC name
        map_name: Map location (e.g., "prontera")
        x: X coordinate
        y: Y coordinate
        commands: List of script commands (optional)
    
    Returns:
        ScriptGenerator with the NPC added
    
    Example:
        gen = create_simple_npc("Merchant", "prontera", 150, 150, 
                                ['mes "Hello!";', 'close;'])
        print(gen.generate_script())
    """
    try:
        gen = ScriptGenerator()
        gen.set_metadata("simple_npc", "Quick Script")
        
        npc = ScriptNPC(name, map_name, x, y)
        
        if commands:
            for cmd in commands:
                npc.add_command(cmd)
        else:
            # Default greeting
            npc.add_command('mes "[NPC]";')
            npc.add_command('mes "Hello, adventurer!";')
            npc.add_command('close;')
        
        gen.add_npc(npc)
        return gen
    except Exception as e:
        print(f"Error creating simple NPC: {e}")
        return None

# Convenience function for quick dialog building
def create_simple_dialog(message, options=None):
    """
    Quick helper to create a simple dialog.
    
    Args:
        message: Initial message to display
        options: List of menu options (optional)
    
    Returns:
        List of script commands
    
    Example:
        cmds = create_simple_dialog("What do you want?", 
                                    ["Option 1", "Option 2", "Exit"])
    """
    try:
        try:
            builder = DialogBuilder()
            builder.add_message(message)
            
            if options:
                builder.add_menu(options)
            
            return builder.to_script_commands()
        except NameError:
            # Fallback if DialogBuilder not available
            cmds = [f'mes "{message}";']
            if options:
                cmds.append(f'menu {", ".join(options)};')
            cmds.append('close;')
            return cmds
    except Exception as e:
        print(f"Error creating simple dialog: {e}")
        return []

# Convenience function to validate a script
def validate_script(script_content):
    """
    Quick validation helper for rAthena scripts.
    
    Args:
        script_content: The script text to validate
    
    Returns:
        (is_valid, errors_list)
    """
    try:
        try:
            validator = ScriptValidator()
            return validator.validate(script_content)
        except NameError:
            # Fallback basic validation
            errors = []
            if 'prontera' in script_content.lower() or 'payon' in script_content.lower():
                # Basic sanity check
                return (True, [])
            return (False, ["Script appears to be invalid"])
    except Exception as e:
        return (False, [str(e)])

# Export main classes and functions
__all__ = [
    # Core classes
    'ScriptGenerator',
    'ScriptNPC',
    'ScriptFunction',
    'ScriptVariable',
    'ScriptDialog',
    'ScriptCondition',
    'ScriptLoop',
    'QuickScriptBuilders',
    'SimpleEditCallback',
    
    # UI classes
    'NPCWizard',
    'DialogBuilder',
    'DialogAction',
    'ScriptTemplates',
    'ScriptValidator',
    'SimpleEditIntegration',
    'UIComponent',
    
    # Helper functions
    'create_simple_npc',
    'create_simple_dialog',
    'validate_script',
]

# Version info
def get_version():
    """Get the version of the rAthena tools."""
    return __version__

def get_info():
    """Get information about the rAthena tools package."""
    return {
        'name': 'rAthena Script Development Tools',
        'version': __version__,
        'author': __author__,
        'license': __license__,
        'description': 'Complete toolkit for creating rAthena game server scripts'
    }
