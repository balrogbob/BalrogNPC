# Getting Started with BalrogNPC

**Quick start guide to get you up and running in minutes**

---

## Table of Contents
1. [Installation](#installation)
2. [First Launch](#first-launch)
3. [Quick Tour](#quick-tour)
4. [Your First NPC](#your-first-npc)
5. [Next Steps](#next-steps)

---

## Installation

### Requirements

**Minimum Requirements:**
- Windows 7/8/10/11 (or Linux with Python 3.8+)
- Python 3.8 or higher
- ~10 MB disk space

**Recommended:**
- Windows 10/11
- Python 3.10+
- 50 MB disk space (with examples and docs)

### Step 1: Install Python

If you don't have Python installed:

1. Download Python from [python.org](https://python.org)
2. Run the installer
3. ? **Important:** Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Download BalrogNPC

**Option A: Using Git**
```bash
git clone https://github.com/balrogbob/BalrogNPC.git
cd BalrogNPC
```

**Option B: Direct Download**
1. Download ZIP from [GitHub Releases](https://github.com/balrogbob/BalrogNPC/releases)
2. Extract to desired location
3. Open folder in terminal/command prompt

### Step 3: Install Optional Dependencies

For YAML validation (optional):
```bash
pip install pyyaml
```

### Step 4: Launch BalrogNPC

**Windows:**
```bash
# Double-click run.bat
# OR run from command line:
python BalrogNPC.py
```

**Linux/Mac:**
```bash
python3 BalrogNPC.py
```

---

## First Launch

### What You'll See

When BalrogNPC launches, you'll see:

1. **Menu Bar** at the top with:
   - File (New, Open, Save)
   - Edit (Undo, Cut, Copy, Paste, Find & Replace)
   - Format (Word Wrap, Font)
   - Syntax (Script/Database/None highlighting)
   - rAthena Tools (NPC creation tools)
   - Help (About)

2. **Line Numbers** on the left side showing line numbers

3. **Text Area** in the center for editing

4. **Title Bar** showing "BalrogNPC - Untitled"

### Initial Setup (Optional)

**Set Font Size:**
1. Click **Format ? Font...**
2. Adjust slider to comfortable size (default: 10)
3. Click OK

**Enable Word Wrap (if desired):**
1. Click **Format ? Word Wrap**
2. Long lines will now wrap to window width

---

## Quick Tour

### 5-Minute Feature Tour

**1. Create a New File (10 seconds)**
- Click **File ? New** or press `Ctrl+N`
- Title changes to "BalrogNPC - Untitled"

**2. Type Some Text (20 seconds)**
```
// My first script
prontera,150,150,4	script	TestNPC	111,{
	mes "Hello!";
	close;
}
```

**3. Save Your File (20 seconds)**
- Click **File ? Save** or press `Ctrl+S`
- Choose location and filename
- Title updates to show filename

**4. Try Find & Replace (30 seconds)**
- Press `Ctrl+F`
- Type "Hello" in Find box
- Type "Greetings" in Replace box
- Click "Replace Next"

**5. Use Go To Line (10 seconds)**
- Press `Ctrl+G`
- Type line number
- Press OK to jump to that line

**6. Enable Syntax Highlighting (20 seconds)**
- Click **Syntax ? Script**
- Watch your code get colored!

**7. Try an rAthena Tool (2 minutes)**
- Click **rAthena Tools ? Insert Quick NPC**
- Select "Simple Dialog"
- Enter NPC name
- Click "Insert NPC"
- See the generated code!

---

## Your First NPC

### Method 1: Using Quick NPC Template (Easiest)

1. **Open Insert Quick NPC**
   - Click **rAthena Tools ? Insert Quick NPC**

2. **Choose Template**
   - Select "Simple Dialog" from dropdown
   - See description: "Basic NPC with greeting and close"

3. **Customize Details**
   - **Name:** `Greeter`
   - **Map:** `prontera`
   - **Position:** X: `150`, Y: `150`
   - **Sprite:** Select "Novice (Male)" or enter custom ID

4. **Preview**
   - See generated script in preview pane on right
   - Verify it looks correct

5. **Insert**
   - Click "Insert NPC"
   - Script appears in your editor!

6. **Save**
   - Press `Ctrl+S`
   - Save as `greeter.npc`

**Result:**
```
// Simple Dialog NPC
prontera,150,150,4	script	Greeter	1_M_01,{
	mes "[Greeter]";
	mes "Hello there!";
	mes "Welcome to our server!";
	close;
}
```

### Method 2: Using NPC Wizard (Step-by-Step)

1. **Launch Wizard**
   - Click **rAthena Tools ? NPC Wizard...**

2. **Step 1: Name and Location**
   - Enter NPC name: `Helper`
   - Map: `prontera`
   - X: `160`, Y: `160`
   - Direction: `4` (facing south)
   - Click **Next**

3. **Step 2: Appearance**
   - Choose sprite ID: `120` (or browse sprites)
   - See preview (if sprite file available)
   - Click **Next**

4. **Step 3: NPC Type**
   - Select "Dialog NPC"
   - Click **Next**

5. **Step 4: Dialog Actions**
   - Click "Message" ? Enter: `Welcome, adventurer!`
   - Click "Next" to add Next button
   - Click "Message" ? Enter: `How can I help you?`
   - Click "Close" to add Close button
   - Click **Next**

6. **Step 5: Confirmation**
   - Review summary and preview
   - Click **Next** to insert

7. **Done!**
   - NPC inserted into editor
   - Save your file

### Method 3: Manual Typing (Learning)

1. **Create New File**
   - `Ctrl+N`

2. **Type NPC Structure**
   ```
   prontera,150,150,4	script	MyNPC	111,{
   	
   }
   ```

3. **Add Dialog**
   ```
   prontera,150,150,4	script	MyNPC	111,{
   	mes "[MyNPC]";
   	mes "Hello!";
   	close;
   }
   ```

4. **Validate**
   - Click **rAthena Tools ? Validate Script**
   - Fix any errors shown

5. **Save**
   - `Ctrl+S` ? Save as `mynpc.npc`

---

## Next Steps

### Immediate Actions

? **Explore the Tools**
- Try each rAthena Tools menu item
- Experiment with templates
- Build a complex dialog with Dialog Builder

? **Learn Keyboard Shortcuts**
- Read [Keyboard Shortcuts](KEYBOARD_SHORTCUTS.md)
- Practice common ones (Save, Find, Go To Line)

? **Validate Your Scripts**
- Open any script file
- Run **rAthena Tools ? Validate Script**
- See what issues it finds
- Try "Apply All Fixes"

### Learning Resources

**For Text Editing:**
1. [Text Editor Features](TEXT_EDITOR.md) - All editing features
2. [Find & Replace](FIND_REPLACE.md) - Advanced search
3. [Line Numbers & Navigation](LINE_NUMBERS.md) - Navigation tools

**For Script Creation:**
1. [Quick Reference](QUICK_REFERENCE.md) - Command cheat sheet
2. [Quick NPC Templates](QUICK_NPC_TEMPLATES.md) - All 10 templates
3. [Dialog Builder](DIALOG_BUILDER.md) - Build complex dialogs
4. [Function Creator](FUNCTION_CREATOR.md) - Create functions

**For Learning rAthena:**
1. [Quick Reference](QUICK_REFERENCE.md) - Start here (30 min)
2. [Script Examples](SCRIPT_EXAMPLES.md) - See working code (1 hour)
3. [rAthena Script Guide](RATHENA_SCRIPT_GUIDE.md) - Complete guide (6-8 hours)

### Practice Projects

**Project 1: Simple Greeter (10 minutes)**
- Create an NPC that greets players
- Use mes and close commands
- Place in prontera

**Project 2: Menu NPC (20 minutes)**
- Create an NPC with a menu
- Offer 3 choices
- Different response for each choice

**Project 3: Item Checker (30 minutes)**
- Create an NPC that checks for items
- Use countitem command
- Give reward if player has items

**Project 4: Quest NPC (1 hour)**
- Create a complete quest NPC
- Check quest state with variables
- Offer quest, check items, give reward

---

## Troubleshooting First Launch

### BalrogNPC Won't Start

**Error: "Python not found"**
- Install Python from python.org
- Make sure to check "Add to PATH" during install
- Restart terminal/command prompt

**Error: "No module named 'tkinter'"**
- Linux: `sudo apt-get install python3-tk`
- Mac: Should be included with Python
- Windows: Reinstall Python with tcl/tk option checked

**Error: "rAthena Tools not available"**
- Check that `rathena-tools` folder exists
- Check that `rathena_tools_menu.py` exists
- Try reinstalling/redownloading

### Window Size Issues

**Window too small:**
- Resize manually
- Next launch will remember size

**Window off screen:**
- Close BalrogNPC
- Delete any config file (if present)
- Relaunch

### Menu Items Grayed Out

**rAthena Tools menu missing:**
- Check console for error messages
- Ensure all files are present
- See [Troubleshooting](TROUBLESHOOTING.md)

---

## Quick Reference Card

### Essential Keyboard Shortcuts
```
Ctrl+N  - New file
Ctrl+O  - Open file
Ctrl+S  - Save file
Ctrl+F  - Find & Replace
Ctrl+G  - Go to line
Ctrl+Z  - Undo
```

### Essential Menu Items
```
File ? New, Open, Save
Edit ? Find & Replace, Go To Line
rAthena Tools ? Insert Quick NPC
rAthena Tools ? Validate Script
Syntax ? Script (enable highlighting)
```

### First Three NPCs to Create
```
1. Simple Dialog (Greeter)
2. Healer NPC
3. Teleporter (Warper)
```

---

## Getting Help

### Documentation
- **Complete Index:** [docs/INDEX.md](INDEX.md)
- **User Guide:** [USER_GUIDE.md](USER_GUIDE.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **FAQ:** [FAQ.md](FAQ.md)

### Community
- **GitHub Issues:** Report bugs and request features
- **rAthena Forums:** Ask scripting questions
- **Discord:** Join rAthena community

### Examples
- **Script Examples:** [SCRIPT_EXAMPLES.md](SCRIPT_EXAMPLES.md)
- **Template Library:** **rAthena Tools ? Insert Quick NPC**
- **rAthena Examples:** `rathena-tools/examples.py`

---

## Summary

? **You've installed BalrogNPC**  
? **You've launched the application**  
? **You've taken a quick tour**  
? **You've created your first NPC**  
? **You know where to find help**

**Next:** Dive deeper into [User Guide](USER_GUIDE.md) or start learning [rAthena Script Guide](RATHENA_SCRIPT_GUIDE.md)!

---

**Welcome to BalrogNPC! Happy scripting!** ???
