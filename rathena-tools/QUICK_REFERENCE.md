# rAthena Script Quick Reference Card

## Variable Prefixes & Types

| Prefix | Scope | Lifetime | Example |
|--------|-------|----------|---------|
| (none) | Character | Permanent | `variable` |
| `@` | Character | Temporary | `@temp` |
| `$` | Global | Permanent | `$global` |
| `$@` | Global | Temporary | `$@temp` |
| `.` | NPC | Permanent | `.npc_var` |
| `.@` | Scope | Temporary | `.@local` |
| `#` | Account | Permanent | `#account` |
| `##` | Global Account | Permanent | `##global_acc` |

**Postfix:** `$` for string, nothing for integer

---

## Common Script Commands

### Messages & Dialogs
```
mes "Your message here";
next;
close;
close2;
clear;
```

### Input & Menu
```
input .@var;
.@choice = select("Option 1:Option 2:Cancel");
menu "A",L_A, "B",L_B;
```

### Items
```
getitem <id>, <amount>;
delitem <id>, <amount>;
.@count = countitem(<id>);
.@name$ = getitemname(<id>);
```

### Warping
```
warp "map_name", x, y;
warpparty "map_name", x, y;
```

### Control Flow
```
if (condition) {
    // code
} else if (other) {
    // code
} else {
    // code
}

switch(expression) {
    case 1:
        // code
        break;
    default:
        // code
}

for (.@i = 0; .@i < 5; .@i++) {
    // code
}

while (condition) {
    // code
}
```

### Functions & Subroutines
```
callfunc "FunctionName", arg1, arg2;
callsub L_SubroutineName, arg1;
return value;
```

---

## NPC Definition Template

```
map,x,y,facing	script	NPC Name	sprite_id,{
	// Main script
	mes "Hello";
	close;

OnInit:
	.var = 1;
	end;

OnTouch:
	mes "You touched me!";
	end;
}
```

---

## Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `+` `-` `*` `/` `%` | Math | `5 + 3` |
| `==` `!=` `>` `<` `>=` `<=` | Comparison | `x == 5` |
| `&&` `\|\|` `!` | Logical | `a && b` |
| `&` `\|` `^` | Bitwise | `.@flags & 1` |
| `+=` `-=` `*=` `/=` | Compound assign | `.@x += 5;` |
| `? :` | Ternary | `(x > 5) ? "yes" : "no"` |

---

## Equipment Slots

```
EQI_HEAD_TOP      - Top Headgear
EQI_HEAD_MID      - Mid Headgear
EQI_HEAD_LOW      - Low Headgear
EQI_ARMOR         - Body Armor
EQI_HAND_L        - Left Hand
EQI_HAND_R        - Right Hand
EQI_SHOES         - Footgear
EQI_ACC_L         - Left Accessory
EQI_ACC_R         - Right Accessory
EQI_GARMENT       - Garment
```

---

## Sprite IDs

| ID | Type |
|----|------|
| -1 | Invisible |
| 111 | Clickable object |
| 120-200 | Standard NPCs |
| 1002+ | Monsters |

---

## Special Character Variables

```
Zeny                Money
Hp, MaxHp           Hit Points
Sp, MaxSp           Spell Points
BaseLevel           Character level
JobLevel            Job level
StatusPoint         Stat points
SkillPoint          Skill points
Weight, MaxWeight   Inventory weight
Sex                 0=Female, 1=Male
Class               Job ID
Upper               0=Normal, 1=Advanced, 2=Baby
```

---

## Useful Functions

### Character Info
```
strcharinfo(0)          Player name
strcharinfo(1)          Player account name
strcharinfo(2)          Player map name
```

### Item Functions
```
getitem(id, count)      Give item
delitem(id, count)      Remove item
countitem(id)           Count items
getitemname(id)         Get item name
```

### Equipment Functions
```
getequipid(slot)        Get equipped item ID
getequipname(slot)      Get equipped item name
getequiprefinerycnt(slot)  Get refine level
```

### Utility Functions
```
rand(min, max)          Random number
int(value)              Convert to integer
str(value)              Convert to string
```

---

## Common Quest Pattern

```
prontera,100,100,4	script	Questor	120,{
	mes "[Questor]";
	
	// Check if quest done
	if (MISC_QUEST & 1) {
		mes "Thanks for helping!";
		close;
	}
	
	// Quest not started
	mes "I need 5 Phracon.";
	
	if (select("Accept:Decline") == 2) {
		mes "Suit yourself.";
		close;
	}
	
	// Check items
	if (countitem(1010) < 5) {
		mes "You don't have enough!";
		close;
	}
	
	// Complete quest
	delitem 1010, 5;
	getitem 1012, 1;
	set MISC_QUEST, MISC_QUEST | 1;
	mes "Thank you! Here's your reward.";
	close;
}
```

---

## Common Shop Pattern

```
prontera,100,100,4	script	Merchant	120,{
	mes "[Merchant]";
	mes "Welcome to my shop!";
	close;
}

// For a true shop with items, use map editor or:
// -	shop	Merchant	120,1010:100,1011:200,1012:300
```

---

## Debugging Tips

```
// Print variable values
mes "DEBUG: value = " + .@value;

// Check conditions
if (BaseLevel >= 50)
    mes "DEBUG: Level ok";
else
    mes "DEBUG: Level too low";

// Use announce for visible output
announce "Debug message",bc_all;

// Use console logging (admin only)
broadcast "Important: " + .@message;
```

---

## Common Mistakes

❌ **Wrong:**
```
if (x == 5)
    statement1;
    statement2;  // This ALWAYS runs!
```

✅ **Correct:**
```
if (x == 5) {
    statement1;
    statement2;
}
```

---

## Best Practices Checklist

- [ ] Use meaningful variable names
- [ ] Always validate user input
- [ ] Check item/resource availability before use
- [ ] Use appropriate variable scope
- [ ] Comment complex logic
- [ ] Test all dialog branches
- [ ] Handle edge cases (full inventory, etc.)
- [ ] Use proper indentation
- [ ] End all commands with `;`
- [ ] Use `end;` not `close;` if script continues after

---

## Python Generator Quick Start

```python
from rathena_script_gen import ScriptGenerator, ScriptNPC

# Create generator
gen = ScriptGenerator()
gen.set_metadata("my_script", "Author Name")

# Create NPC
npc = ScriptNPC("NPC Name", "prontera", 100, 100)
npc.add_command('mes "Hello";')
npc.add_command('close;')

# Add and generate
gen.add_npc(npc)
script = gen.generate_script()

# Export
gen.export_script("output.txt")
```

---

## Map Names (Common)

```
prontera         Prontera
geffen           Geffen
payon            Payon
izlude           Izlude
aldebaran        Aldebaran
amatsu           Amatsu
kunlun           Kunlun
rachel           Rachel
lighthalzen      Lighthalzen
einbech          Einbech
einbroch         Einbroch
hugel            Hugel
gonryun          Gonryun
```

---

**Last Updated:** 2025-05-17  
**For:** rAthena Game Server
