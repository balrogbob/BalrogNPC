# rAthena Script Writing Guide

**Version:** 1.0  
**Last Updated:** 2025-05-17  
**For:** rAthena Game Server

---

## Table of Contents

1. [Chapter 1: Fundamentals](#chapter-1-fundamentals)
2. [Chapter 2: Variables and Data](#chapter-2-variables-and-data)
3. [Chapter 3: Basic Commands](#chapter-3-basic-commands)
4. [Chapter 4: Control Flow](#chapter-4-control-flow)
5. [Chapter 5: Functions and Subroutines](#chapter-5-functions-and-subroutines)
6. [Chapter 6: NPC Creation](#chapter-6-npc-creation)
7. [Chapter 7: Item and Equipment](#chapter-7-item-and-equipment)
8. [Chapter 8: Advanced Features](#chapter-8-advanced-features)
9. [Chapter 9: Debugging and Best Practices](#chapter-9-debugging-and-best-practices)

---

## Chapter 1: Fundamentals

### 1.1 What is rAthena Scripting?

rAthena scripting is a custom scripting language used to create interactive content in Ragnarok Online private servers. Scripts control:

- **NPC Dialogs** - Interactive conversations with NPCs
- **Quest Systems** - Quest progression and rewards
- **Item Functions** - Custom item behaviors
- **Game Events** - Server-wide events and announcements
- **Player Interactions** - Warps, shops, and services

### 1.2 Script File Structure

Scripts are organized in text files with the following structure:

```
// Comment: File header
// Description of what this script does

npc: path/to/script/file.txt

// Top-level commands (map setup, monster spawning)
prontera,100,100,4	script	NPC Name	120,{
	// Script code here
	mes "Hello";
	close;
}
```

### 1.3 File Organization

- Scripts are loaded via `npc/(pre-)re/scripts_main.conf`
- Each line in `scripts_main.conf` references a script file with: `npc: path/to/file.txt`
- Files can be loaded once to prevent conflicts
- Use `delnpc:` to unload a script file

### 1.4 Comments

**Single-line comments:**
```
// This entire line is ignored by the parser
```

**Block comments:**
```
/* This text
   no matter the line breaks
   is all ignored
   until the closing symbol: */
```

### 1.5 Syntax Conventions

| Symbol | Meaning |
|--------|---------|
| `<angle brackets>` | Required argument |
| `{curly brackets}` | Optional argument |
| `"quotes"` | String literal |
| Numbers | Integer values (no decimals) |
| `;` | Statement terminator |
| `%TAB%` | Tab separator in documentation |

---

## Chapter 2: Variables and Data

### 2.1 Variable Scope and Prefixes

Variables are identified by three components: **prefix**, **name**, and **postfix**.

#### Scope Levels

| Prefix | Scope | Lifetime | Storage |
|--------|-------|----------|---------|
| (none) | Character | Permanent | `char_reg_num/str` |
| `@` | Character | Temporary | RAM |
| `$` | Global Server | Permanent | `mapreg` table |
| `$@` | Global Server | Temporary | RAM |
| `.` | NPC | Permanent* | NPC data |
| `.@` | Scope/Instance | Temporary | Function scope |
| `'` | Instance | Permanent | Instance-specific |
| `#` | Account (Local) | Permanent | `acc_reg_num/str` |
| `##` | Account (Global) | Permanent | `global_acc_reg_num/str` |

*NPC variables exist until server restart or NPC reload

#### Type Postfixes

| Postfix | Type | Example |
|---------|------|---------|
| (none) | Integer | `variable` |
| `$` | String | `variable$` |

### 2.2 Variable Declaration and Assignment

**Integer variable:**
```
.@level = 50;
```

**String variable:**
```
.@name$ = "Poring";
```

**Assignment with expression:**
```
.@total = 100 + 50 - 25;  // Result: 125
```

**Multiple assignment:**
```
.@x = .@y = 100;  // Both equal 100
```

### 2.3 Arrays

Arrays store multiple values under one variable name using indices (starting at 0):

```
// Declaration with setarray
setarray .@items[0], 1010, 1011, 1012, 1013;

// Access individual elements
.@first = .@items[0];  // Result: 1010
.@third = .@items[2];  // Result: 1012

// Use variable as index
.@idx = 2;
.@value = .@items[.@idx];  // Result: 1012
```

**Get array size:**
```
.@size = getarraysize(.@items);  // Returns 4
```

**Clear array elements:**
```
cleararray .@items[0], 0, getarraysize(.@items);
```

### 2.4 Special Character Variables

These built-in variables can be read or modified:

| Variable | Type | Description |
|----------|------|-------------|
| `Zeny` | int | Player's money |
| `Hp` | int | Current HP |
| `MaxHp` | int | Maximum HP |
| `Sp` | int | Current SP |
| `MaxSp` | int | Maximum SP |
| `BaseLevel` | int | Base level (1-99+) |
| `JobLevel` | int | Job level (1-50+) |
| `StatusPoint` | int | Unspent stat points |
| `SkillPoint` | int | Unspent skill points |
| `BaseExp` | int | Base experience points |
| `JobExp` | int | Job experience points |
| `Weight` | int | Current weight carried |
| `MaxWeight` | int | Maximum weight capacity |
| `Sex` | int | 0=Female, 1=Male |
| `Class` | int | Character job class ID |
| `Upper` | int | 0=Normal, 1=Advanced, 2=Baby |

**Example - Full healing:**
```
Hp = MaxHp;
Sp = MaxSp;
```

### 2.5 Operators

#### Arithmetic Operators

| Operator | Operation | Example |
|----------|-----------|---------|
| `+` | Addition | `5 + 3` → `8` |
| `-` | Subtraction | `5 - 3` → `2` |
| `*` | Multiplication | `5 * 3` → `15` |
| `/` | Division (integer) | `7 / 2` → `3` |
| `%` | Modulo (remainder) | `7 % 2` → `1` |

#### Compound Assignment

All operators below support compound assignment with `=`:

```
.@x += 10;  // .@x = .@x + 10
.@x -= 5;   // .@x = .@x - 5
.@x *= 2;   // .@x = .@x * 2
.@x /= 2;   // .@x = .@x / 2
.@x %= 3;   // .@x = .@x % 3
```

#### Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `5 == 5` → `true` |
| `!=` | Not equal to | `5 != 3` → `true` |
| `>` | Greater than | `5 > 3` → `true` |
| `<` | Less than | `5 < 3` → `false` |
| `>=` | Greater or equal | `5 >= 5` → `true` |
| `<=` | Less or equal | `5 <= 3` → `false` |

#### Logical Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `&&` | AND (both true) | `(1==1) && (2==2)` → `true` |
| `\|\|` | OR (either true) | `(1==1) \|\| (2==3)` → `true` |
| `!` | NOT (reverse) | `!(1==2)` → `true` |

#### Bitwise Operators

Used for storing multiple boolean values in one integer (bit-masking):

```
// Set bit 0 (value 1)
.@flags = .@flags \| 1;

// Check if bit 1 (value 2) is set
if (.@flags & 2)
    mes "Bit 1 is set";

// Remove bit 2 (value 4) using XOR
.@flags = .@flags ^ 4;
```

### 2.6 Ternary Operator

Conditional expression returning one of two values:

```
mes "Welcome, " + (Sex ? "Mr." : "Mrs.") + " " + strcharinfo(0);
```

**Syntax:** `(condition) ? value_if_true : value_if_false`

---

## Chapter 3: Basic Commands

### 3.1 Message Display

**Display message:**
```
mes "This text appears in a dialog box";
```

**Multiple lines in one command:**
```
mes "Line 1", "Line 2", "Line 3";
```

**With color codes (HTML-like):**
```
mes "This is ^FF0000 red ^000000 and this is ^00FF00 green ^000000.";
```

Color format: `^RRGGBB` where RR=Red, GG=Green, BB=Blue (hexadecimal)

**Common colors:**
- `^FF0000` - Red
- `^00FF00` - Green
- `^0000FF` - Blue
- `^FFFF00` - Yellow
- `^FF00FF` - Magenta
- `^000000` - Black
- `^FFFFFF` - White

### 3.2 Dialog Buttons

**Next button (shows message, waits for click):**
```
mes "Line 1";
next;
mes "Line 2";
```

**Close button (ends the script):**
```
mes "Goodbye!";
close;
```

**Close2 button (continues script execution after closing):**
```
mes "Warping you...";
close2;
warp "prontera", 150, 150;
end;
```

**Clear dialog (continue without button):**
```
mes "Starting a quest...";
sleep2 2000;  // Wait 2 seconds
clear;
mes "Quest started!";
close;
```

### 3.3 Player Input

**Numeric input:**
```
input .@amount;
mes "You entered: " + .@amount;
```

**String input:**
```
input .@name$;
mes "Your name is: " + .@name$;
```

**Input with validation:**
```
input .@level, 1, 99;  // Min 1, Max 99
if (input .@level, 1, 99 == 1)
    mes "Level must be between 1-99";
```

### 3.4 Menu System

**Simple menu:**
```
menu "Option 1",L_Opt1, "Option 2",L_Opt2, "Cancel",-;

L_Opt1:
    mes "You selected Option 1";
    close;

L_Opt2:
    mes "You selected Option 2";
    close;
```

**Menu with @menu variable:**
```
.@choice = select("Yes:No:Cancel");
// @choice == 1 for "Yes"
// @choice == 2 for "No"
// @choice == 3 for "Cancel"
```

**Dynamic menu (skip empty options):**
```
setarray .@opts$[0], "Accept", "Decline", "Ask Later";
.@selected = select(.@opts$[0], .@opts$[1], .@opts$[2]);
```

### 3.5 Item Operations

**Give item to player:**
```
getitem 1010, 5;  // Give 5x Phracon (ID 1010)
```

**Check item count:**
```
if (countitem(1010) >= 5)
    mes "You have 5 Phracon";
else
    mes "You don't have enough";
```

**Remove item:**
```
delitem 1010, 5;  // Remove 5x Phracon
```

**Get item name:**
```
.@name$ = getitemname(1010);  // Returns "Phracon"
```

### 3.6 Script Termination

**End script immediately:**
```
end;
```

**End and close dialog:**
```
close;
```

---

## Chapter 4: Control Flow

### 4.1 Conditional Statements

**Simple if:**
```
if (BaseLevel > 50)
    mes "You are level 50 or higher";
```

**If with block:**
```
if (countitem(1010) >= 5) {
    mes "You have enough Phracon";
    delitem 1010, 5;
    getitem 1011, 1;
} else {
    mes "You don't have enough";
}
```

**If-else chain:**
```
if (BaseLevel < 10) {
    mes "Novice";
} else if (BaseLevel < 30) {
    mes "Apprentice";
} else if (BaseLevel < 60) {
    mes "Journeyman";
} else {
    mes "Master";
}
```

### 4.2 Switch Statements

**Switch with cases:**
```
switch(Class) {
    case 0:
        mes "You are a Novice";
        break;
    case 1:
    case 2:
        mes "You are a Swordsman";
        break;
    default:
        mes "Unknown class";
        break;
}
```

**Switch with menu:**
```
switch(select("Buy:Sell:Leave")) {
    case 1:
        callsub S_BuyItems;
        break;
    case 2:
        callsub S_SellItems;
        break;
}
```

### 4.3 While Loops

**Counter loop:**
```
.@i = 1;
while (.@i <= 5) {
    mes .@i;
    .@i++;
}
```

**Condition loop:**
```
.@health = 100;
while (.@health > 0) {
    .@health -= 10;
    mes "Health: " + .@health;
}
```

### 4.4 For Loops

**Basic for loop:**
```
for (.@i = 0; .@i < 5; .@i++)
    mes "Iteration: " + .@i;
```

**Iterating through array:**
```
setarray .@items[0], 1010, 1011, 1012;
for (.@i = 0; .@i < getarraysize(.@items); .@i++)
    mes getitemname(.@items[.@i]);
```

**Nested loops:**
```
for (.@x = 0; .@x < 3; .@x++) {
    for (.@y = 0; .@y < 3; .@y++) {
        mes "X:" + .@x + " Y:" + .@y;
    }
}
```

### 4.5 Do-While Loops

**Post-test loop (executes at least once):**
```
do {
    .@menu = select("Continue:Exit");
} while (.@menu == 1);
```

### 4.6 Jump and Goto

**Jump to label:**
```
if (BaseLevel < 10) {
    mes "Too low level";
    goto L_End;
}

mes "Welcome!";

L_End:
    close;
```

**Note:** Avoid excessive `goto` usage. Prefer `if/else` or `switch` statements.

---

## Chapter 5: Functions and Subroutines

### 5.1 Calling Functions

**Call user-defined function:**
```
.@result = callfunc("MyFunction", 10, 20);
mes "Result: " + .@result;
```

**Call function without arguments:**
```
callfunc("DisplayWelcome");
```

### 5.2 Defining Functions

**Function definition (separate file):**
```
function	script	MyFunction	{
    .@arg1 = getarg(0);      // First argument
    .@arg2 = getarg(1);      // Second argument
    .@sum = .@arg1 + .@arg2;
    return .@sum;
}
```

**Function with default values:**
```
function	script	SafeGet	{
    .@value = getarg(0, 0);  // Default 0 if not provided
    return .@value;
}
```

### 5.3 Subroutines (callsub)

**Define and call subroutine:**
```
prontera,100,100,4	script	Trainer	120,{
    callsub S_Training, 10;  // Pass 10 as argument
    close;

S_Training:
    .@points = getarg(0);
    StatusPoint += .@points;
    mes "Gained " + .@points + " status points!";
    return;
}
```

**Get argument count:**
```
function	script	FlexFunc	{
    .@count = getargcount();
    for (.@i = 0; .@i < .@count; .@i++)
        mes getarg(.@i);
    return;
}
```

### 5.4 Return Values

**Return from function:**
```
function	script	Calculate	{
    if (getarg(0) < 0)
        return 0;
    return getarg(0) * 2;
}
```

**Return without value:**
```
function	script	PrintInfo	{
    mes getarg(0);
    mes getarg(1);
    return;  // No return value
}
```

---

## Chapter 6: NPC Creation

### 6.1 NPC Definition Structure

**Basic NPC:**
```
<map>,<x>,<y>,<facing>%TAB%script%TAB%<NPC Name>%TAB%<sprite id>,{
    // Script code
    mes "Hello!";
    close;
}
```

**Real example:**
```
prontera,150,150,4	script	Weapons Dealer	120,{
    mes "[Weapons Dealer]";
    mes "Welcome to my shop!";
    close;
}
```

### 6.2 NPC Names

NPC names can have display and unique components:

```
prontera,150,150,4	script	Merchant#shop1	120,{
    // Display name: "Merchant"
    // Unique name: "Merchant#shop1"
    mes "Hello";
    close;
}
```

**Using with getvariableofnpc:**
```
set getvariableofnpc(.shop_level, "Merchant#shop1"), 5;
```

### 6.3 NPC Sprites

| Sprite ID | Type |
|-----------|------|
| `-1` | Invisible NPC |
| `111` | Clickable object (no sprite) |
| `120-200` | Standard NPC sprites |
| `Mob ID` | Monster sprite |

**Monster sprite example:**
```
prontera,150,150,4	script	Poring Guard	1002,{
    mes "A Poring stands guard";
    close;
}
```

### 6.4 NPC Facing Direction

Direction is counterclockwise in 45° increments:

```
0 = North (top)
1 = North-West
2 = West (left)
3 = South-West
4 = South (bottom)
5 = South-East
6 = East (right)
7 = North-East
```

### 6.5 Trigger Areas (OnTouch)

NPC triggered by walking into area:

```
prontera,150,150,4	script	Heal Point	120,5,5,{
    OnTouch:
        heal 100, 100;
        mes "You've been healed!";
        end;
}
```

**Without trigger area (click only):**
```
prontera,150,150,4	script	Info NPC	120,{
    mes "Information board";
    close;
}
```

### 6.6 Floating NPCs

NPCs not on a map (used for timers/events):

```
-	script	Announcer	-1,{
    OnInit:
        announce "Server started!",bc_all;
        end;
}
```

### 6.7 Duplicate NPCs

Create copy of existing NPC with different settings:

```
prontera,150,150,4	script	Weapons Dealer	120,{
    mes "Welcome!";
    close;
}

geffen,200,200,4	duplicate(Weapons Dealer)	Dealer Copy	120
```

---

## Chapter 7: Item and Equipment

### 7.1 Getting Items

**Give item:**
```
getitem 1010, 1;  // 1x Phracon
```

**Give named item:**
```
getitem "Phracon", 5;
```

**Check if item given successfully:**
```
if (getitem(1010, 1) == 0) {
    mes "Inventory full!";
}
```

### 7.2 Item Properties

**Get item name:**
```
.@name$ = getitemname(1010);  // "Phracon"
```

**Get item info:**
```
.@buy_price = getiteminfo(1010, ITEMINFO_BUY);
.@sell_price = getiteminfo(1010, ITEMINFO_SELL);
.@weight = getiteminfo(1010, ITEMINFO_WEIGHT);
.@type = getiteminfo(1010, ITEMINFO_TYPE);
```

**Check item slots:**
```
.@slots = getitemslots(1010);  // Number of slots
if (.@slots > 0)
    mes "Item is slotted";
```

### 7.3 Equipment Operations

**Check equipped item:**
```
if (getequipid(EQI_HEAD_TOP) == 2234)
    mes "You're wearing a Tiara!";
```

**Equipment slots:**

| Slot Constant | Description |
|---|---|
| `EQI_HEAD_TOP` | Top Headgear |
| `EQI_HEAD_MID` | Mid Headgear |
| `EQI_HEAD_LOW` | Low Headgear |
| `EQI_ARMOR` | Body Armor |
| `EQI_HAND_L` | Left Hand |
| `EQI_HAND_R` | Right Hand |
| `EQI_SHOES` | Footgear |
| `EQI_ACC_L` | Left Accessory |
| `EQI_ACC_R` | Right Accessory |
| `EQI_GARMENT` | Garment |

**Get equipment name:**
```
.@equip_name$ = getequipname(EQI_HEAD_TOP);
mes "You wear: " + .@equip_name$;
```

**Get equipment refine level:**
```
.@refine = getequiprefinerycnt(EQI_ARMOR);
mes "Armor refine: +" + .@refine;
```

### 7.4 Inventory List

**Get all inventory items:**
```
getinventorylist;

for (.@i = 0; .@i < @inventorylist_count; .@i++) {
    .@id = @inventorylist_id[.@i];
    .@amount = @inventorylist_amount[.@i];
    mes getitemname(.@id) + " x" + .@amount;
}
```

**Available arrays:**
- `@inventorylist_id[]` - Item IDs
- `@inventorylist_amount[]` - Quantities
- `@inventorylist_refine[]` - Refine levels
- `@inventorylist_identify[]` - Identified flag
- `@inventorylist_card1-4[]` - Card data
- `@inventorylist_count` - Total items

---

## Chapter 8: Advanced Features

### 8.1 Special NPC Labels

**Initialization (runs on script load/reload):**
```
prontera,100,100,4	script	MyNPC	120,{
    OnInit:
        .shop_level = 1;
        .shop_open = true;
        end;
}
```

**Time-based triggers:**
```
-	script	DailyAnnounce	-1,{
    OnClock0600:  // 6:00 AM
        announce "Good morning!",bc_all;
        end;
    
    OnClock1800:  // 6:00 PM
        announce "Good evening!",bc_all;
        end;
}
```

### 8.2 Quest Variables

**Using quest variables (bit-wise):**
```
// Check if quest bit is set
if (MISC_QUEST & 1) {
    mes "You've completed Juice Maker Quest";
}

// Set quest bit
set MISC_QUEST, MISC_QUEST | 1;

// Clear quest bit
set MISC_QUEST, MISC_QUEST ^ 1;
```

### 8.3 Warping Players

**Warp to location:**
```
warp "prontera", 150, 150;
```

**Warp multiple players:**
```
warpparty "prontera", 150, 150;
```

**Save/load warp point:**
```
@memo;  // Save current location
@load;  // Warp to saved location
```

### 8.4 NPC-to-NPC Communication

**Get NPC variable:**
```
.@level = getvariableofnpc(.shop_level, "Merchant#shop1");
```

**Set NPC variable:**
```
set getvariableofnpc(.shop_level, "Merchant#shop1"), 5;
```

### 8.5 Map Events

**OnPCLoginEvent - Player logs in:**
```
-	script	LoginNotif	-1,{
    OnPCLoginEvent:
        announce "Player " + strcharinfo(0) + " logged in!",bc_all;
        end;
}
```

**OnPCLogoutEvent - Player logs out:**
```
-	script	LogoutNotif	-1,{
    OnPCLogoutEvent:
        announce "Player " + strcharinfo(0) + " logged out!",bc_all;
        end;
}
```

**OnPCDieEvent - Player dies:**
```
-	script	DeathNotif	-1,{
    OnPCDieEvent:
        mes "You died!";
        end;
}
```

### 8.6 Monster Spawning

**Permanent monster spawn (top-level command):**
```
prontera,100,100,5,5	monster	Poring	1002,10,10000,20000
```

**Parameters:**
- Map: `prontera`
- Coordinates: `100,100`
- Spawn range: `5,5` (±5 cells)
- Monster name: `Poring` (or `--en--` or `--ja--`)
- Monster ID: `1002`
- Count: `10` monsters
- Respawn delay: `10000` ms base, `20000` ms random variance

---

## Chapter 9: Debugging and Best Practices

### 9.1 Common Mistakes

**Missing semicolons:**
```
// Wrong
mes "Hello"
close;

// Correct
mes "Hello";
close;
```

**String concatenation errors:**
```
// Wrong
mes "Level: " + BaseLevel;  // May cause issues with type mismatch

// Correct
mes "Level: " + BaseLevel;  // Explicit conversion happens automatically
```

**Variable scope confusion:**
```
// Wrong - .@var only exists in current scope
function	script	Test	{
    .@var = 10;
    return;
}

// If calling from NPC, .@var won't exist there

// Correct - use return value
function	script	Test	{
    return 10;
}
```

**Infinite loops:**
```
// Wrong
while (1) {
    mes "This loops forever!";
}

// Correct
.@count = 0;
while (.@count < 5) {
    mes "Iteration: " + .@count;
    .@count++;
}
```

### 9.2 Debugging Techniques

**Print variable values:**
```
mes "DEBUG: .@x = " + .@x;
mes "DEBUG: BaseLevel = " + BaseLevel;
```

**Check conditions:**
```
if (BaseLevel >= 50)
    mes "DEBUG: Level check passed";
else
    mes "DEBUG: Level too low";
```

**Announce to console (GMs only):**
```
// Using built-in debug (if enabled)
broadcast "Variable: " + .@value;
```

### 9.3 Best Practices

**1. Always use proper variable scope:**
```
prontera,100,100,4	script	Trainer	120,{
    .npc_id = 1;           // NPC variable - shared
    .@player_data = 10;    // Scope variable - local
    @player_temp = 100;    // Character temporary - player-specific
}
```

**2. Validate user input:**
```
input .@amount, 1, 999;
if (.@amount < 1 || .@amount > 999) {
    mes "Invalid amount!";
    close;
}
```

**3. Check item availability before removing:**
```
if (countitem(1010) < 5) {
    mes "You don't have enough Phracon";
    close;
}
delitem 1010, 5;
```

**4. Use meaningful variable names:**
```
// Bad
.@a = 100;
.@b = .@a * 2;

// Good
.@base_price = 100;
.@final_price = .@base_price * 2;
```

**5. Comment complex logic:**
```
// Check if player is experienced enough and has required items
if (BaseLevel >= 50 && countitem(1010) >= 5) {
    // Give advancement quest item
    getitem 1011, 1;
}
```

**6. Keep functions focused:**
```
// Bad - does multiple things
function	script	DoEverything	{
    // Trading logic
    // Questing logic
    // Combat logic
}

// Good - single responsibility
function	script	ProcessTrade	{
    // Only trading logic
}
```

**7. Handle edge cases:**
```
// Inventory might be full
if (getitem(1010, 1) == 0) {
    mes "Your inventory is full!";
    close;
}
```

### 9.4 Performance Tips

**1. Avoid nested loops when possible:**
```
// Slower - O(n²)
for (.@i = 0; .@i < 100; .@i++)
    for (.@j = 0; .@j < 100; .@j++)
        // Do something

// Faster - O(n)
for (.@i = 0; .@i < 10000; .@i++)
    // Do something
```

**2. Cache array sizes:**
```
// Slower - recalculates size each iteration
for (.@i = 0; .@i < getarraysize(.@items); .@i++)

// Faster - cache the size
.@size = getarraysize(.@items);
for (.@i = 0; .@i < .@size; .@i++)
```

**3. Use appropriate variable scope:**
```
// Avoid using permanent variables (.var) for temporary data
// Use .@ scope variables instead
.@temp = 100;  // Better than @temp for local NPC use
```

### 9.5 Example: Complete Quest Script

```
prontera,100,100,4	script	Blacksmith	120,{
    mes "[Blacksmith]";
    mes "Welcome to my forge!";
    
    // Check if quest completed
    if (MISC_QUEST & 4) {
        mes "Thank you for helping me before!";
        close;
    }
    
    .@choice = select("Accept Quest:Decline");
    
    if (.@choice == 2) {
        mes "Suit yourself.";
        close;
    }
    
    // Quest dialog
    mes "I need 5 Phracon to complete a weapon.";
    mes "Can you bring them to me?";
    next;
    
    // Check if player has items
    if (countitem(1010) < 5) {
        mes "You don't have enough Phracon!";
        close;
    }
    
    // Process quest completion
    delitem 1010, 5;
    set MISC_QUEST, MISC_QUEST | 4;
    getitem 1012, 1;  // Give reward
    
    mes "Excellent! Here's your reward.";
    close;
}
```

---

## Appendix A: Common Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `getarg(index)` | value | Get function argument |
| `getarraysize(array)` | int | Get array size |
| `getitemname(id)` | string | Get item name |
| `getiteminfo(id, type)` | value | Get item data |
| `countitem(id)` | int | Count items in inventory |
| `getitem(id, amount)` | int | Give item to player |
| `delitem(id, amount)` | int | Remove item from inventory |
| `getequipid(slot)` | int | Get equipped item ID |
| `getequipname(slot)` | string | Get equipped item name |
| `strcharinfo(type)` | string | Get character info |
| `rand(min, max)` | int | Random number |
| `warp(map, x, y)` | - | Warp player |
| `getinventorylist()` | - | Populate inventory arrays |

---

## Appendix B: Item Database Quick Reference

Common item IDs:

| ID | Name | Type |
|----|------|------|
| 501 | Red Potion | Consumable |
| 502 | Orange Potion | Consumable |
| 1010 | Phracon | Material |
| 1011 | Emveretarcon | Material |
| 1012 | Elunium | Material |
| 12024 | Red Pouch | Summon |
| 14581 | Dungeon Teleport Scroll | Consumable |
| 602 | Butterfly Wing | Consumable |
| 601 | Fly Wing | Consumable |

---

**End of Guide**

For full command documentation, refer to `/doc/script_commands.txt` in the rAthena repository.
