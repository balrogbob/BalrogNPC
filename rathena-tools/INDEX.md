# rAthena Script Development Tools - Complete Index

## 📚 START HERE

**New to rAthena scripting?**  
→ Start with **RATHENA_SCRIPT_GUIDE.md** (comprehensive)

**Need quick answers?**  
→ Use **QUICK_REFERENCE.md** (one-page reference)

**Want to use the Python toolkit?**  
→ Read **RATHENA_TOOLS_README.md** (API docs)

**Want to integrate into SimpleEdit?**  
→ Follow **SIMPLEEDIT_INTEGRATION.md** (step-by-step)

**Want to see working examples?**  
→ Run **examples.py** (10 complete examples)

---

## 📄 Documentation Files

| File | Size | Purpose | Chapters/Sections |
|------|------|---------|------------------|
| [RATHENA_SCRIPT_GUIDE.md](RATHENA_SCRIPT_GUIDE.md) | 90 KB | Comprehensive scripting guide | 9 chapters + 2 appendices |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 15 KB | Quick lookup reference | 15 sections |
| [RATHENA_TOOLS_README.md](RATHENA_TOOLS_README.md) | 25 KB | Python toolkit API docs | Complete class documentation |
| [SIMPLEEDIT_INTEGRATION.md](SIMPLEEDIT_INTEGRATION.md) | 20 KB | Integration guide | Step-by-step instructions |
| [README_COMPLETE_PACKAGE.md](README_COMPLETE_PACKAGE.md) | 18 KB | Package overview | Features, statistics, paths |
| [INDEX.md](INDEX.md) | This file | Navigation guide | Quick links |

---

## 💻 Code Files

| File | Size | Type | Purpose |
|------|------|------|---------|
| [rathena_script_gen.py](rathena_script_gen.py) | 35 KB | Python Module | Core script generator engine |
| [rathena_script_ui.py](rathena_script_ui.py) | 28 KB | Python Module | UI helpers and wizards |
| [examples.py](examples.py) | 18 KB | Python Script | 10 working examples |
| [rathena_tools/__init__.py](rathena_tools/__init__.py) | 8 KB | Python Package | Package initialization |

---

## 🎓 Learning Paths

### Path 1: Learn rAthena Scripting (5-8 hours)
1. **QUICK_REFERENCE.md** (20 min) - Get syntax overview
2. **RATHENA_SCRIPT_GUIDE.md** - Read all 9 chapters
   - Chapter 1-2: Fundamentals (1 hour)
   - Chapter 3: Basic Commands (1 hour)
   - Chapter 4: Control Flow (1 hour)
   - Chapter 5-6: Functions and NPCs (1.5 hours)
   - Chapter 7-9: Advanced features (2 hours)

### Path 2: Use Python Toolkit (2-4 hours)
1. **RATHENA_TOOLS_README.md** (30 min) - Understand API
2. **examples.py** (1 hour) - Run and study examples
3. **Quick project** (1-2 hours) - Create your first script
4. **Integration** (1-2 hours) - Add to SimpleEdit

### Path 3: Complete Integration Setup (4-6 hours)
1. **README_COMPLETE_PACKAGE.md** (20 min) - Overview
2. **SIMPLEEDIT_INTEGRATION.md** (30 min) - Read guide
3. **Copy files** (10 min) - Set up directories
4. **Create wrapper** (1 hour) - Write plugin code
5. **Test integration** (1-2 hours) - Create test NPCs
6. **Polish UI** (1-2 hours) - Add dialogs/menus

### Path 4: Quick Start (1 hour)
1. **QUICK_REFERENCE.md** (15 min)
2. Run **examples.py** (20 min)
3. Modify example for your needs (25 min)

---

## 📖 Guide Chapters

### RATHENA_SCRIPT_GUIDE.md

**Chapter 1: Fundamentals**
- What is rAthena Scripting
- Script File Structure
- File Organization
- Comments
- Syntax Conventions

**Chapter 2: Variables and Data**
- Variable Scope and Prefixes
- Variable Declaration
- Arrays
- Special Character Variables
- Operators (all types)
- Ternary Operators

**Chapter 3: Basic Commands**
- Message Display (colors, multiple lines)
- Dialog Buttons (next, close, close2, clear)
- Player Input (numeric, string)
- Menu System
- Item Operations
- Script Termination

**Chapter 4: Control Flow**
- Conditional Statements (if/else)
- Switch Statements
- While Loops
- For Loops
- Do-While Loops
- Jump and Goto

**Chapter 5: Functions and Subroutines**
- Calling Functions
- Defining Functions
- Subroutines (callsub)
- Return Values
- Advanced patterns

**Chapter 6: NPC Creation**
- NPC Definition Structure
- NPC Names (display + unique)
- NPC Sprites
- Facing Directions
- Trigger Areas (OnTouch)
- Floating NPCs
- Duplicate NPCs

**Chapter 7: Item and Equipment**
- Getting Items
- Item Properties
- Equipment Operations
- Inventory List Management
- Item Database References

**Chapter 8: Advanced Features**
- Special NPC Labels (OnInit, OnTouch, OnClock)
- Quest Variables (bit-masking)
- Warping Players
- NPC-to-NPC Communication
- Map Events
- Monster Spawning

**Chapter 9: Debugging and Best Practices**
- Common Mistakes
- Debugging Techniques
- Best Practices (10 guidelines)
- Performance Tips
- Complete Quest Example

**Appendices**
- Appendix A: Common Functions (15+ functions)
- Appendix B: Item Database Quick Reference

---

## 🐍 Python API Reference

### ScriptGenerator
```python
from rathena_script_gen import ScriptGenerator

gen = ScriptGenerator(log_callback=handler)
gen.set_metadata(name, author, description)
gen.add_npc(npc)
gen.add_function(func)
gen.add_global_variable(var)
script = gen.generate_script()
gen.export_script(filepath)
gen.clear_all()
```

### ScriptNPC
```python
from rathena_script_gen import ScriptNPC

npc = ScriptNPC(name, map, x, y, facing, sprite_id)
npc.set_npc_name(display, unique)
npc.add_command(cmd)
npc.to_script()
```

### DialogBuilder
```python
from rathena_script_ui import DialogBuilder

dialog = DialogBuilder()
dialog.add_message(text) \
       .add_next_button() \
       .add_menu(options) \
       .add_item_give(id, amount) \
       .to_script_commands()
```

### NPCWizard
```python
from rathena_script_ui import NPCWizard

wizard = NPCWizard(on_complete_callback)
wizard.set_npc_basic_info(name, map, x, y)
wizard.set_npc_appearance(sprite_id)
wizard.set_npc_type(NPCTypeEnum.QUEST_GIVER)
wizard.next_step()
```

### ScriptValidator
```python
from rathena_script_ui import ScriptValidator

valid, errors = ScriptValidator.validate_npc(npc)
valid, errors = ScriptValidator.validate_function(func)
valid, errors = ScriptValidator.validate_script(gen)
```

---

## 🎯 Common Tasks

### Create Simple NPC
**File:** RATHENA_SCRIPT_GUIDE.md - Chapter 6.1  
**Code:** examples.py - example_1_simple_dialog()

### Create Quest NPC
**File:** RATHENA_SCRIPT_GUIDE.md - Chapter 8.2  
**Code:** examples.py - example_2_quest_npc()

### Create Custom Function
**File:** RATHENA_SCRIPT_GUIDE.md - Chapter 5.2  
**Code:** examples.py - example_5_npc_with_function()

### Use Dialog Builder
**File:** RATHENA_TOOLS_README.md - DialogBuilder section  
**Code:** examples.py - example_4_using_dialog_builder()

### Validate Scripts
**File:** RATHENA_TOOLS_README.md - ScriptValidator section  
**Code:** examples.py - example_6_validation()

### Integrate into SimpleEdit
**File:** SIMPLEEDIT_INTEGRATION.md  
**Code:** Plugin wrapper example (provided)

---

## 🔍 Quick Lookup

### Find Information About...

| Topic | Location |
|-------|----------|
| Variable scopes | QUICK_REFERENCE.md + Chapter 2 |
| Basic commands | QUICK_REFERENCE.md + Chapter 3 |
| Item functions | Chapter 7 + Appendix A |
| Equipment slots | QUICK_REFERENCE.md + Chapter 7 |
| NPC creation | Chapter 6 + examples |
| Quests | Chapter 8 + example_2 |
| Python API | RATHENA_TOOLS_README.md |
| Integration | SIMPLEEDIT_INTEGRATION.md |
| Common mistakes | Chapter 9 |
| Best practices | Chapter 9 |

---

## 📊 Package Statistics

- **Total Documentation**: ~140 KB
- **Total Code**: ~90 KB
- **Documentation Pages**: 50+
- **Code Examples**: 1000+
- **Python Lines**: 2000+
- **Classes**: 20+
- **Functions**: 50+
- **Chapters**: 9
- **Working Examples**: 10

---

## ✅ Quality Checklist

- ✅ Comprehensive 9-chapter guide
- ✅ Quick reference card
- ✅ Complete Python API
- ✅ 10 working examples
- ✅ UI helper classes
- ✅ Script validation
- ✅ SimpleEdit integration
- ✅ Best practices guide
- ✅ Troubleshooting section
- ✅ 1000+ code examples

---

## 🚀 Getting Started Right Now

### Option 1: Read Only (30 minutes)
```
1. Open QUICK_REFERENCE.md
2. Skim RATHENA_SCRIPT_GUIDE.md - Chapter 1-3
3. You now understand rAthena scripting basics
```

### Option 2: Use Python (1 hour)
```
1. Read RATHENA_TOOLS_README.md
2. Run: python examples.py
3. Study example_1 code
4. Modify example_1 for your needs
```

### Option 3: Create with SimpleEdit (2 hours)
```
1. Copy files to SimpleEdit/plugins/
2. Create wrapper (code provided)
3. Test with NPCWizard
4. Create your first NPC using visual builder
```

---

## 📞 Help Resources

### For rAthena Syntax
→ **RATHENA_SCRIPT_GUIDE.md** (comprehensive)  
→ **QUICK_REFERENCE.md** (quick lookup)

### For Python Code
→ **RATHENA_TOOLS_README.md** (API docs)  
→ **examples.py** (working code)

### For Integration
→ **SIMPLEEDIT_INTEGRATION.md** (step-by-step)  
→ Plugin wrapper code (in integration guide)

### For Examples
→ **examples.py** (10 working scripts)  
→ Chapter 9 of guide (complete example)

---

## 🎓 Recommended Reading Order

1. **Start:** README_COMPLETE_PACKAGE.md (5 min)
2. **Learn Syntax:** QUICK_REFERENCE.md (15 min)
3. **Deep Dive:** RATHENA_SCRIPT_GUIDE.md - Chapters 1-3 (2 hours)
4. **Try Code:** examples.py examples (1 hour)
5. **Learn API:** RATHENA_TOOLS_README.md (1 hour)
6. **Integrate:** SIMPLEEDIT_INTEGRATION.md (if needed)
7. **Reference:** Chapters 4-9 of guide (as needed)

---

## 💡 Tips

- Use QUICK_REFERENCE.md while coding
- Run examples.py to learn patterns
- Keep RATHENA_SCRIPT_GUIDE.md open during coding
- Use ScriptValidator before exporting
- Start with simple NPCs, build complexity gradually
- Comment your code liberally
- Test all dialog branches

---

## 🎉 You Now Have

✅ Complete rAthena scripting guide  
✅ Python-based script generator  
✅ UI helpers and wizards  
✅ 10 working examples  
✅ SimpleEdit integration code  
✅ Validation and testing tools  
✅ Quick reference materials  
✅ Best practices documentation  

---

## 🔗 File Navigation

```
🏠 You are here: INDEX.md

📚 Documentation:
  ├─ RATHENA_SCRIPT_GUIDE.md ─────→ Main guide (9 chapters)
  ├─ QUICK_REFERENCE.md ─────────→ One-page reference
  ├─ RATHENA_TOOLS_README.md ────→ Python API docs
  ├─ SIMPLEEDIT_INTEGRATION.md ──→ Integration guide
  └─ README_COMPLETE_PACKAGE.md ─→ Package overview

🐍 Code:
  ├─ rathena_script_gen.py ──────→ Core engine
  ├─ rathena_script_ui.py ───────→ UI helpers
  ├─ examples.py ────────────────→ 10 examples
  └─ rathena_tools/__init__.py ──→ Package init
```

---

**Version:** 1.0  
**Status:** Complete ✅  
**Last Updated:** 2025-05-17  

**Ready to start? Pick your path above and dive in!** 🚀

---

## Quick Command Reference

```bash
# View comprehensive guide
less RATHENA_SCRIPT_GUIDE.md

# Quick lookup
cat QUICK_REFERENCE.md

# Run examples
python examples.py

# View API docs
less RATHENA_TOOLS_README.md

# Integration instructions
less SIMPLEEDIT_INTEGRATION.md
```

---

**Happy scripting! 🎮✨**
