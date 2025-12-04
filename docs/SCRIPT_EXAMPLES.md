# Script Examples for BalrogNPC

**Working code examples for common NPC types**

---

## Table of Contents

1. [Simple Greeting NPC](#1-simple-greeting-npc)
2. [Shop NPC](#2-shop-npc)
3. [Healer NPC](#3-healer-npc)
4. [Warper NPC](#4-warper-npc)
5. [Quest NPC](#5-quest-npc)
6. [Buffer NPC](#6-buffer-npc)
7. [Job Changer NPC](#7-job-changer-npc)
8. [Information NPC](#8-information-npc)
9. [Stylist NPC](#9-stylist-npc)
10. [Time-Based Event NPC](#10-time-based-event-npc)

---

## 1. Simple Greeting NPC

**Purpose:** Greet players with a simple message

```
prontera,150,150,4	script	Greeter	111,{
	mes "[Greeter]";
	mes "Welcome to our server!";
	mes "Enjoy your stay!";
	close;
}
```

**How to Use:**
- Save as `greeter.npc`
- Place in `npc/custom/` folder
- Add to `scripts_custom.conf`
- Reload server: `@reloadscript`

---

## 2. Shop NPC

**Purpose:** Sell items to players

```
prontera,140,140,4	script	Item Seller	4_M_01,{
	mes "[Item Seller]";
	mes "Check out my items!";
	close;
}

// Shop definition
-	shop	ItemShop	-1,501:50,502:200,503:500,601:1000
```

**Items Sold:**
- 501: Red Potion (50z)
- 502: Orange Potion (200z)
- 503: Yellow Potion (500z)
- 601: Butterfly Wing (1000z)

---

## 3. Healer NPC

**Purpose:** Heal player HP/SP

```
prontera,160,160,4	script	Healer	4_W_SISTER,{
	mes "[Healer]";
	mes "Would you like to be healed?";
	next;
	
	if(select("Yes, please!:No, thanks") == 1) {
		percentheal 100, 100;
		sc_end SC_ALL;
		mes "[Healer]";
		mes "You're fully healed!";
	}
	close;
}
```

---

## 4. Warper NPC

**Purpose:** Teleport to different cities

```
prontera,150,180,4	script	Warper	4_M_SAGE_A,{
	mes "[Warper]";
	mes "Where would you like to go?";
	next;
	
	switch(select("Prontera:Morocc:Geffen:Payon:Alberta:Cancel")) {
		case 1:
			warp "prontera", 156, 191;
			break;
		case 2:
			warp "morocc", 156, 93;
			break;
		case 3:
			warp "geffen", 119, 59;
			break;
		case 4:
			warp "payon", 152, 75;
			break;
		case 5:
			warp "alberta", 28, 234;
			break;
	}
	close;
}
```

---

## 5. Quest NPC

**Purpose:** Simple item collection quest

```
prontera,170,170,4	script	Quest Giver	1_M_MERCHANT,{
	// Check if quest is complete
	if(quest_jellopy == 1) {
		mes "[Quest Giver]";
		mes "Thank you for helping me!";
		close;
	}
	
	mes "[Quest Giver]";
	mes "I need 10 Jellopy.";
	mes "Can you help me?";
	next;
	
	if(select("Accept:Decline") == 2) {
		mes "[Quest Giver]";
		mes "Come back if you change your mind.";
		close;
	}
	
	// Check if player has items
	if(countitem(909) < 10) {
		mes "[Quest Giver]";
		mes "You need 10 Jellopy!";
		close;
	}
	
	// Complete quest
	delitem 909, 10;
	getitem 501, 5;  // 5 Red Potions
	set quest_jellopy, 1;
	
	mes "[Quest Giver]";
	mes "Perfect! Here's your reward!";
	close;
}
```

---

## 6. Buffer NPC

**Purpose:** Provide stat buffs

```
prontera,145,145,4	script	Buffer	4_F_KAFRA1,{
	mes "[Buffer]";
	mes "I can buff you!";
	next;
	
	switch(select("Blessing:Increase AGI:Both:Cancel")) {
		case 1:
			sc_start SC_BLESSING, 240000, 10;
			mes "[Buffer]";
			mes "Blessing granted!";
			break;
		case 2:
			sc_start SC_INCREASEAGI, 240000, 10;
			mes "[Buffer]";
			mes "AGI increased!";
			break;
		case 3:
			sc_start SC_BLESSING, 240000, 10;
			sc_start SC_INCREASEAGI, 240000, 10;
			mes "[Buffer]";
			mes "Double buff applied!";
			break;
	}
	close;
}
```

---

## 7. Job Changer NPC

**Purpose:** Change player's job class

```
prontera,155,155,4	script	Job Changer	1_F_PRIEST,{
	mes "[Job Changer]";
	mes "I can change your job!";
	next;
	
	if(BaseLevel < 10) {
		mes "[Job Changer]";
		mes "You need level 10 first!";
		close;
	}
	
	switch(select("Swordman:Mage:Archer:Acolyte:Merchant:Thief:Cancel")) {
		case 1: jobchange Job_Swordman; break;
		case 2: jobchange Job_Mage; break;
		case 3: jobchange Job_Archer; break;
		case 4: jobchange Job_Acolyte; break;
		case 5: jobchange Job_Merchant; break;
		case 6: jobchange Job_Thief; break;
		case 7: close;
	}
	
	mes "[Job Changer]";
	mes "Job changed successfully!";
	close;
}
```

---

## 8. Information NPC

**Purpose:** Display server information

```
prontera,165,165,4	script	Info NPC	8W_SOLDIER,{
	mes "[Server Info]";
	mes "^0000FFServer Information^000000";
	mes "─────────────────────────";
	mes "^008000Rates:^000000";
	mes "  • Base EXP: 1x";
	mes "  • Job EXP: 1x";
	mes "  • Drop: 1x";
	next;
	
	mes "[Server Info]";
	mes "^008000Max Stats:^000000";
	mes "  • Max Level: 99/70";
	mes "  • Max Stats: 99";
	close;
}
```

---

## 9. Stylist NPC

**Purpose:** Change player appearance

```
prontera,135,135,4	script	Stylist	4_F_ALCHE,{
	mes "[Stylist]";
	mes "What would you like to change?";
	next;
	
	switch(select("Hair Style:Hair Color:Cancel")) {
		case 1:
			mes "[Stylist]";
			mes "Choose style (1-27):";
			input .@style;
			
			if(.@style < 1 || .@style > 27) {
				mes "Invalid style!";
				close;
			}
			setlook LOOK_HAIR, .@style;
			break;
			
		case 2:
			mes "[Stylist]";
			mes "Choose color (0-8):";
			input .@color;
			setlook LOOK_HAIR_COLOR, .@color;
			break;
	}
	close;
}
```

---

## 10. Time-Based Event NPC

**Purpose:** Daily announcements

```
-	script	Daily Events	-1,{
OnClock0600:  // 6:00 AM
	announce "Good morning! Daily reset complete!", bc_all;
	end;

OnClock1200:  // 12:00 PM
	announce "Lunchtime event starting!", bc_all;
	end;

OnClock1800:  // 6:00 PM
	announce "Evening PvP event begins!", bc_all;
	end;
}
```

---

## How to Use These Examples

1. **Copy Code**
   - Copy the script you want
   - Paste into BalrogNPC

2. **Customize**
   - Change NPC name
   - Modify coordinates
   - Adjust sprite ID
   - Edit dialog text

3. **Validate**
   - Use **rAthena Tools → Validate Script**
   - Fix any errors

4. **Save**
   - Save as `.npc` file
   - Place in `npc/custom/` folder

5. **Load**
   - Add to `scripts_custom.conf`:
     ```
     npc: npc/custom/yourfile.npc
     ```
   - Reload: `@reloadscript`

---

## Tips for Modifying Examples

### Change Location
```
// Original
prontera,150,150,4	script	NPC	111,{

// Modified
geffen,119,59,4	script	NPC	111,{
```

### Change Sprite
```
// Original sprite
111

// Custom sprite (Kafra)
4_F_KAFRA1
```

### Add More Menu Options
```
// Add to switch statement
switch(select("Option1:Option2:Option3:NewOption:Cancel")) {
	case 4:
		// New option code
		break;
}
```

### Change Quest Variable
```
// Original
if(quest_jellopy == 1) {

// Custom
if(MyCustomQuest == 1) {

// At completion
set MyCustomQuest, 1;
```

---

**Practice with these examples to master rAthena scripting!** 🎮✨
