"""
Complete Example Scripts for rAthena Script Generator
Demonstrates all major features of the toolkit

Run this file to generate example scripts and see the output
"""

from rathena_script_gen import (
    ScriptGenerator, ScriptNPC, ScriptFunction, ScriptVariable,
    QuickScriptBuilders, LogLevel
)
from rathena_script_ui import (
    DialogBuilder, NPCWizard, ScriptValidator, ScriptTemplates
)


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def example_1_simple_dialog():
    """Example 1: Simple Dialog NPC"""
    print_section("Example 1: Simple Dialog NPC")
    
    def log_handler(level, msg):
        if level in [LogLevel.SUCCESS, LogLevel.ERROR]:
            print(f"[{level.value}] {msg}")
    
    gen = ScriptGenerator(log_callback=log_handler)
    gen.set_metadata(
        name="simple_dialog",
        author="Example Author",
        description="A simple NPC that greets players"
    )
    
    npc = ScriptNPC(
        name="Greeter",
        map_name="prontera",
        x=150,
        y=150,
        sprite_id=120
    )
    
    npc.add_command('mes "[Greeter]";')
    npc.add_command('mes "Welcome to Prontera, adventurer!";')
    npc.add_command('mes "What would you like to do?";')
    npc.add_command('switch(select("Talk:Shop:Leave")) {')
    npc.add_command('\tcase 1:')
    npc.add_command('\t\tmes "Nice to meet you!";')
    npc.add_command('\t\tbreak;')
    npc.add_command('\tcase 2:')
    npc.add_command('\t\tmes "Sorry, I don\'t have a shop yet.";')
    npc.add_command('\t\tbreak;')
    npc.add_command('}')
    npc.add_command('close;')
    
    gen.add_npc(npc)
    print(gen.generate_script())


def example_2_quest_npc():
    """Example 2: Quest-Giving NPC"""
    print_section("Example 2: Quest-Giving NPC")
    
    gen = ScriptGenerator()
    gen.set_metadata(
        name="quest_example",
        author="Example Author",
        description="NPC that gives a quest with item requirements"
    )
    
    npc = ScriptNPC(
        name="QuestMaster",
        map_name="prontera",
        x=160,
        y=160,
        sprite_id=120
    )
    
    # Check if quest already completed
    npc.add_command('if (MISC_QUEST & 2) {')
    npc.add_command('\t\tmes "[QuestMaster]";')
    npc.add_command('\t\tmes "Thank you for your hard work!";')
    npc.add_command('\t\tclose;')
    npc.add_command('}')
    npc.add_command('')
    
    # Offer quest
    npc.add_command('mes "[QuestMaster]";')
    npc.add_command('mes "I need your help gathering materials.";')
    npc.add_command('mes "Can you bring me 5 Phracon?";')
    npc.add_command('')
    
    # Menu choice
    npc.add_command('if (select("Accept Quest:Decline") == 2) {')
    npc.add_command('\t\tmes "I understand. Come back if you change your mind.";')
    npc.add_command('\t\tclose;')
    npc.add_command('}')
    npc.add_command('')
    
    # Check items
    npc.add_command('if (countitem(1010) < 5) {')
    npc.add_command('\t\tmes "You don\'t have enough Phracon!";')
    npc.add_command('\t\tmes "Please come back when you do.";')
    npc.add_command('\t\tclose;')
    npc.add_command('}')
    npc.add_command('')
    
    # Complete quest
    npc.add_command('mes "Excellent! You have the materials!";')
    npc.add_command('delitem 1010, 5;')
    npc.add_command('getitem 1012, 1;')
    npc.add_command('getitem 501, 5;')
    npc.add_command('set MISC_QUEST, MISC_QUEST | 2;')
    npc.add_command('mes "Here\'s your reward. Thank you!";')
    npc.add_command('close;')
    
    gen.add_npc(npc)
    print(gen.generate_script())


def example_3_using_quick_builders():
    """Example 3: Using Quick Script Builders"""
    print_section("Example 3: Quick Script Builders")
    
    gen = ScriptGenerator()
    gen.set_metadata(
        name="quick_builders_example",
        author="Example Author",
        description="NPCs created using quick builders"
    )
    
    # Create a healing NPC
    healer = QuickScriptBuilders.create_heal_npc(
        "Healer",
        "prontera",
        100, 100
    )
    gen.add_npc(healer)
    
    # Create a teleporter NPC
    teleporter = QuickScriptBuilders.create_warp_npc(
        "Teleporter",
        "prontera",
        150, 150,
        [
            ("geffen", 119, 59, "Geffen"),
            ("payon", 161, 247, "Payon"),
            ("izlude", 128, 114, "Izlude"),
            ("aldebaran", 140, 131, "Aldebaran")
        ]
    )
    gen.add_npc(teleporter)
    
    print(gen.generate_script())


def example_4_using_dialog_builder():
    """Example 4: Using DialogBuilder"""
    print_section("Example 4: DialogBuilder with Fluent API")
    
    # Create dialog with fluent API
    dialog = DialogBuilder()
    dialog.add_message("Greetings, adventurer!") \
           .add_next_button() \
           .add_message("I see you have come to seek fortune and glory.") \
           .add_next_button() \
           .add_message("I have a task that might interest you.") \
           .add_menu(["Accept", "Decline", "Ask for details"]) \
           .add_close_button()
    
    # Create NPC with dialog
    gen = ScriptGenerator()
    gen.set_metadata(
        name="dialog_builder_example",
        author="Example Author",
        description="NPC created with DialogBuilder"
    )
    
    npc = ScriptNPC("TaskGiver", "prontera", 170, 170)
    for cmd in dialog.to_script_commands():
        npc.add_command(cmd)
    
    gen.add_npc(npc)
    print(gen.generate_script())


def example_5_npc_with_function():
    """Example 5: NPC using a Custom Function"""
    print_section("Example 5: NPC with Custom Function")
    
    gen = ScriptGenerator()
    gen.set_metadata(
        name="function_example",
        author="Example Author",
        description="NPC that uses custom functions"
    )
    
    # Create function
    price_func = ScriptFunction("CalculatePrice")
    price_func.add_command('.@base_price = getarg(0);')
    price_func.add_command('.@quantity = getarg(1);')
    price_func.add_command('.@discount = getarg(2, 1);')
    price_func.add_command('.@final_price = (.@base_price * .@quantity) / .@discount;')
    price_func.return_value = ".@final_price"
    
    gen.add_function(price_func)
    
    # Create NPC that uses function
    npc = ScriptNPC("Merchant", "prontera", 180, 180)
    npc.add_command('mes "[Merchant]";')
    npc.add_command('mes "Welcome to my shop!";')
    npc.add_command('.@item_price = callfunc("CalculatePrice", 100, 5, 2);')
    npc.add_command('mes "Total cost: " + .@item_price + " Zeny";')
    npc.add_command('close;')
    
    gen.add_npc(npc)
    print(gen.generate_script())


def example_6_validation():
    """Example 6: Script Validation"""
    print_section("Example 6: Script Validation")
    
    gen = ScriptGenerator()
    gen.set_metadata(
        name="validation_example",
        author="Example Author",
        description="Demonstrating script validation"
    )
    
    # Create a valid NPC
    valid_npc = ScriptNPC("ValidNPC", "prontera", 100, 100)
    valid_npc.add_command('mes "Hello";')
    valid_npc.add_command('close;')
    gen.add_npc(valid_npc)
    
    # Validate
    is_valid, errors = ScriptValidator.validate_script(gen)
    
    print(f"Script Validation Result: {'PASS ✓' if is_valid else 'FAIL ✗'}")
    if errors:
        print("Errors found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No errors found! Script is ready.")
    
    print("\nGenerated Script:")
    print("-" * 70)
    print(gen.generate_script())


def example_7_npc_templates():
    """Example 7: Using NPC Templates"""
    print_section("Example 7: Available NPC Templates")
    
    templates = ScriptTemplates.get_all_templates()
    
    print("Available templates:\n")
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template['name']}")
        print(f"   Type: {template['type'].value}")
        print(f"   Description: {template['description']}")
        print()


def example_8_complex_npc():
    """Example 8: Complex NPC with Multiple Handlers"""
    print_section("Example 8: Complex NPC with OnInit and OnTouch")
    
    gen = ScriptGenerator()
    gen.set_metadata(
        name="complex_npc_example",
        author="Example Author",
        description="NPC with initialization and touch handlers"
    )
    
    npc = ScriptNPC(
        name="Manager#manager1",
        map_name="prontera",
        x=190,
        y=190,
        sprite_id=121,
        trigger_x=2,
        trigger_y=2
    )
    
    # Main dialog
    npc.add_command('mes "[Manager]";')
    npc.add_command('mes "What do you need?";')
    npc.add_command('switch(select("Status:Settings:Leave")) {')
    npc.add_command('\tcase 1:')
    npc.add_command('\t\tmes "NPC active since: " + .npc_uptime;')
    npc.add_command('\t\tbreak;')
    npc.add_command('\tcase 2:')
    npc.add_command('\t\tmes "Settings menu not yet implemented.";')
    npc.add_command('\t\tbreak;')
    npc.add_command('}')
    npc.add_command('close;')
    
    # OnInit handler
    npc.on_init = [
        '.npc_uptime = "startup";',
        '.npc_version = "1.0";',
        'end;'
    ]
    
    # OnTouch handler
    npc.on_touch = [
        'mes "You touched the manager!";',
        'end;'
    ]
    
    gen.add_npc(npc)
    print(gen.generate_script())


def example_9_batch_generation():
    """Example 9: Generate Multiple NPCs at Once"""
    print_section("Example 9: Batch NPC Generation")
    
    gen = ScriptGenerator()
    gen.set_metadata(
        name="town_npcs",
        author="Example Author",
        description="A collection of NPCs for a town"
    )
    
    npc_configs = [
        ("Guard", "prontera", 100, 100, 120, "I guard this town."),
        ("Baker", "prontera", 120, 120, 122, "I bake fresh bread daily."),
        ("Armorer", "prontera", 140, 140, 121, "I craft and repair armor."),
        ("Mage", "prontera", 160, 160, 120, "I teach spells and magic."),
    ]
    
    for name, map_name, x, y, sprite, dialogue in npc_configs:
        npc = ScriptNPC(name, map_name, x, y, sprite_id=sprite)
        npc.add_command(f'mes "[{name}]";')
        npc.add_command(f'mes "{dialogue}";')
        npc.add_command('close;')
        gen.add_npc(npc)
    
    print(gen.generate_script())


def example_10_dynamic_dialog():
    """Example 10: Dynamic Dialog Based on Player Status"""
    print_section("Example 10: Dynamic Dialog Based on Player Status")
    
    gen = ScriptGenerator()
    gen.set_metadata(
        name="level_based_npc",
        author="Example Author",
        description="NPC that responds differently based on player level"
    )
    
    npc = ScriptNPC("Trainer", "prontera", 200, 200)
    
    # Dynamic dialog based on level
    npc.add_command('mes "[Trainer]";')
    npc.add_command('')
    
    npc.add_command('if (BaseLevel < 10) {')
    npc.add_command('\t\tmes "You are very new! Let me help you.";')
    npc.add_command('\t\tmes "First, gather some basic items.";')
    npc.add_command('} else if (BaseLevel < 30) {')
    npc.add_command('\t\tmes "You\'re getting stronger!";')
    npc.add_command('\t\tmes "Try hunting in the dungeons.";')
    npc.add_command('} else if (BaseLevel < 60) {')
    npc.add_command('\t\tmes "You\'re becoming experienced!";')
    npc.add_command('\t\tmes "Have you tried the harder dungeons?";')
    npc.add_command('} else {')
    npc.add_command('\t\tmes "You are a skilled adventurer!";')
    npc.add_command('\t\tmes "Take on the greatest challenges.";')
    npc.add_command('}')
    npc.add_command('')
    npc.add_command('close;')
    
    gen.add_npc(npc)
    print(gen.generate_script())


def main():
    """Run all examples"""
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "rAthena Script Generator - Complete Examples" + " " * 15 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Run all examples
    example_1_simple_dialog()
    example_2_quest_npc()
    example_3_using_quick_builders()
    example_4_using_dialog_builder()
    example_5_npc_with_function()
    example_6_validation()
    example_7_npc_templates()
    example_8_complex_npc()
    example_9_batch_generation()
    example_10_dynamic_dialog()
    
    print_section("All Examples Complete")
    print("""
The examples above demonstrate:
  1. Simple dialog NPC creation
  2. Quest-giving NPC with item requirements
  3. Quick builder templates
  4. DialogBuilder fluent API
  5. NPCs with custom functions
  6. Script validation
  7. Available templates
  8. Complex NPC with multiple handlers
  9. Batch NPC generation
  10. Dynamic dialog based on conditions

For more information, see:
  - RATHENA_SCRIPT_GUIDE.md (comprehensive guide)
  - RATHENA_TOOLS_README.md (toolkit documentation)
  - QUICK_REFERENCE.md (quick reference card)
    """)


if __name__ == "__main__":
    main()
