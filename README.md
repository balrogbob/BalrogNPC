# BalrogNPC 🐉 — rAthena Script Editor
<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Version 1.0.0](https://img.shields.io/badge/Version-0.2.1-brightgreen.svg)](#)

</div>



A lightweight rAthena-focused text editor with integrated script generation, dialog builders and validation tools. Designed for fast NPC/script editing with helpful utilities built right in.

<!-- Screenshots should be placed in the project root -->
![App Screenshot 2](./screenshot2.png)
![App Screenshot 1](./screenshot1.png)

## What's new ✨

- Left-side line number gutter for easier navigation 🔢
- Go To Line (Ctrl+G) — jump straight to any line ➤
- Full Find & Replace (Ctrl+F):
  - Find Next / Find Previous
  - Replace Next / Replace All
  - Regex mode (Python `re`) 🧩
  - Case sensitive toggle
  - Whole-word matching
  - Highlight all matches
- Improved Find behavior and selection handling
- All features implemented in `BalrogNPC.py` (no external library edits required)

## Features 🚀

- Simple text editing (New/Open/Save)
- Undo, Cut/Copy/Paste, Select All
- Word Wrap toggle
- Adjustable font size
- rAthena Tools integration (NPC wizard, dialog builder, function creator, validators)
- Quick NPC templates and script insertion

## Keyboard Shortcuts ⌨️

- New: Ctrl+N
- Open: Ctrl+O
- Save: Ctrl+S
- Undo: Ctrl+Z
- Find & Replace: Ctrl+F
- Go To Line: Ctrl+G

## Running the Application

```bash
python BalrogNPC.py
```

## Screenshots 📸

Place `screenshot1.png` and `screenshot2.png` in the project root to have them displayed at the top of this README.

## Notes & Tips

- Regex mode uses Python's `re` — invalid patterns will show an error in the Find dialog.
- Whole-word matching wraps the pattern with `\b` boundaries (when not in raw regex mode the pattern is escaped first).
- Highlight All Matches will visually mark all matches using a highlight tag; closing the dialog clears highlights.

Enjoy editing — happy scripting! 🎉

