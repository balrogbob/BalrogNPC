# Troubleshooting Guide

**Solutions to common issues with BalrogNPC**

---

## Application Won't Start

### Error: "Python not found" or "command not found"

**Problem:** Python not installed or not in PATH

**Solution:**
1. Download Python from [python.org](https://python.org)
2. During installation, check **"Add Python to PATH"**
3. Restart terminal/command prompt
4. Verify: `python --version`

**Alternative:**
```bash
# Use full path to Python
C:\Python310\python.exe BalrogNPC.py
```

### Error: "No module named 'tkinter'"

**Problem:** Tkinter not installed

**Solution:**

**Linux:**
```bash
sudo apt-get install python3-tk
```

**Mac:**
- Should be included with Python
- If missing, reinstall Python from python.org

**Windows:**
- Reinstall Python
- Check "tcl/tk and IDLE" option

### Application Crashes on Startup

**Problem:** Missing files or corrupted installation

**Solution:**
1. Verify all files are present:
   - `BalrogNPC.py`
   - `rathena_tools_menu.py`
   - `syntax_highlighter.py`
   - `rathena-tools/` folder
   - `syntax/` folder

2. Redownload if files are missing

3. Check console for error messages

---

## rAthena Tools Menu Missing

### Tools menu doesn't appear

**Problem:** Import error in rAthena tools

**Solution:**
1. Check that `rathena-tools` folder exists
2. Verify files:
   - `rathena-tools/rathena_script_gen.py`
   - `rathena-tools/rathena_script_ui.py`
   - `rathena-tools/__init__.py`

3. Check console output for error messages

4. Try reinstalling/redownloading

### Tools menu items grayed out

**Problem:** Dependencies missing

**Solution:**
- Ensure Python 3.8+ is installed
- Check that all rathena-tools files are present
- Look for import errors in console

---

## Find & Replace Issues

### Find doesn't work or crashes

**Problem:** Regex pattern error

**Solution:**
1. Disable regex mode
2. Use simple text search
3. If using regex, verify pattern syntax

### Highlights remain after closing Find dialog

**Problem:** Highlights not cleared

**Solution:**
- Reopen Find dialog
- Close it again
- Or restart BalrogNPC

---

## Syntax Highlighting Issues

### Syntax highlighting not working

**Problem:** Syntax not enabled or files missing

**Solution:**
1. Check **Syntax** menu
2. Select **Script** or **Database**
3. Verify `syntax/` folder exists with `.ini` files

### Colors are wrong or unreadable

**Problem:** Color configuration issue

**Solution:**
1. Click **Syntax → Edit Colors...**
2. Adjust foreground/background colors
3. Click **Save Color**
4. Restart BalrogNPC

### Syntax very slow on large files

**Problem:** Performance issue

**Solution:**
1. Disable syntax highlighting: **Syntax → None**
2. Or split large file into smaller files

---

## Validation Issues

### Script Validator shows false errors

**Problem:** Validator misinterpreting code

**Solution:**
1. Check if error is actually valid
2. Review [rAthena Script Guide](RATHENA_SCRIPT_GUIDE.md)
3. Use **Review & Fix** to skip false positives

### YAML Validator not available

**Problem:** PyYAML not installed

**Solution:**
```bash
pip install pyyaml
```

### Auto-fix breaks script

**Problem:** Auto-fix applied incorrectly

**Solution:**
1. Press `Ctrl+Z` to undo changes
2. Use **Review & Fix** instead
3. Manually apply fixes selectively

---

## File Operations Issues

### Can't save file

**Problem:** Permission error or disk full

**Solution:**
1. Check file permissions
2. Try saving to different location
3. Ensure disk has space
4. Close any program accessing the file

### File encoding issues

**Problem:** Special characters display incorrectly

**Solution:**
- BalrogNPC uses UTF-8
- Check source file encoding
- Resave file as UTF-8 in another editor

### Lost work (file not saved)

**Problem:** Didn't save before closing

**Solution:**
- No auto-save feature currently
- Save frequently (`Ctrl+S`)
- Consider enabling auto-save in future

---

## Performance Issues

### Editor slow with large files

**Problem:** Large file performance

**Solution:**
1. Disable syntax highlighting
2. Disable word wrap
3. Split large file into smaller files
4. Use different editor for very large files

### Lag when typing

**Problem:** Syntax highlighting overhead

**Solution:**
1. Disable syntax: **Syntax → None**
2. Reduce file size
3. Close other applications

---

## Display Issues

### Window size problems

**Problem:** Window too small or off-screen

**Solution:**
1. Resize manually
2. Restart BalrogNPC
3. Window position/size should persist

### Text too small/large

**Problem:** Font size issue

**Solution:**
1. Click **Format → Font...**
2. Adjust slider
3. Click OK

### Line numbers misaligned

**Problem:** Display glitch

**Solution:**
1. Resize window
2. Scroll up/down
3. Restart BalrogNPC if persistent

---

## Platform-Specific Issues

### Windows

**UAC Blocks Execution:**
- Run as administrator if needed
- Or move to non-protected location

**Path Issues:**
- Use forward slashes in code: `C:/folder/file.txt`
- Or escape backslashes: `C:\\folder\\file.txt`

### Linux

**Missing Tkinter:**
```bash
sudo apt-get install python3-tk
```

**Permission Denied:**
```bash
chmod +x BalrogNPC.py
python3 BalrogNPC.py
```

### macOS

**Gatekeeper Blocks:**
- Right-click → Open
- Or: System Preferences → Security → Allow

**Python Version:**
- Use `python3` instead of `python`
- Install from python.org if missing

---

## Getting Help

### Check Documentation
1. [Getting Started](GETTING_STARTED.md)
2. [User Guide](USER_GUIDE.md)
3. [FAQ](FAQ.md)

### Report Issues
1. Check existing GitHub Issues (see repository)
2. Create new issue with:
   - Operating system
   - Python version
   - Steps to reproduce
   - Error messages

### Community Support
- rAthena Forums: [rathena.org](https://rathena.org)
- Discord communities
- GitHub Discussions

---

## Common Error Messages

### "AttributeError: 'NoneType' object has no attribute..."

**Cause:** Internal error, likely bug

**Solution:**
- Note the full error message
- Report as GitHub issue
- Try restarting BalrogNPC

### "NameError: name '...' is not defined"

**Cause:** Missing import or variable

**Solution:**
- This shouldn't happen in normal use
- Report as bug if it occurs

### "FileNotFoundError: [Errno 2] No such file..."

**Cause:** Missing file

**Solution:**
1. Check file path is correct
2. Verify file exists
3. Use absolute path if needed

---

## Best Practices to Avoid Issues

✅ **Save frequently** - `Ctrl+S` after changes  
✅ **Validate before use** - Run validator on scripts  
✅ **Keep backups** - Copy important files  
✅ **Update regularly** - Check for new versions  
✅ **Report bugs** - Help improve BalrogNPC  

---

**Still having issues?** Create a GitHub Issue (see repository) with details!
