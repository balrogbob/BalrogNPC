#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BalrogNPC - rAthena Script Editor
A simple text editor with integrated rAthena script generation tools

Based on Windows XP Notepad with rAthena Tools integration
"""

from tkinter import *
from tkinter import messagebox, filedialog, simpledialog
from tkinter import ttk
from tkinter import font as tkfont
import os
import sys

# Ensure rathena-tools package is in path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_rathena_path = os.path.join(_current_dir, 'rathena-tools')
if _rathena_path not in sys.path:
    sys.path.insert(0, _rathena_path)

# Import rAthena tools menu
try:
    from rathena_tools_menu import create_rathena_menu
    _RATHENA_TOOLS_AVAILABLE = True
except ImportError as e:
    _RATHENA_TOOLS_AVAILABLE = False
    print(f"[WARNING] rAthena Tools not available: {e}")


class BalrogNPC:
    """Simple text editor with rAthena Tools integration"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("BalrogNPC - Untitled")
        self.root.geometry("800x600")
        
        # Current file path
        self.current_file = None
        self.modified = False
        
        # Create menu bar
        self.menuBar = Menu(self.root)
        self.root.config(menu=self.menuBar)
        
        # File menu
        fileMenu = Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        fileMenu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        fileMenu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As...", command=self.save_as_file)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.exit_app)
        
        # Edit menu
        editMenu = Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        editMenu.add_separator()
        editMenu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        editMenu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        editMenu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        editMenu.add_command(label="Delete", command=self.delete)
        editMenu.add_separator()
        editMenu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        editMenu.add_command(label="Find & Replace...", command=self.find_replace_dialog, accelerator="Ctrl+F")
        editMenu.add_command(label="Go To Line...", command=self.goto_line_dialog, accelerator="Ctrl+G")
        
        # Format menu
        formatMenu = Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="Format", menu=formatMenu)
        formatMenu.add_checkbutton(label="Word Wrap", command=self.toggle_word_wrap)
        formatMenu.add_command(label="Font...", command=self.change_font)
        
        # Add rAthena Tools menu if available
        if _RATHENA_TOOLS_AVAILABLE:
            create_rathena_menu(self.root, self.menuBar, self)
        
        # Help menu
        helpMenu = Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="About BalrogNPC", command=self.show_about)
        
        # Create text widget with scrollbar
        self.textFrame = Frame(self.root)
        self.textFrame.pack(fill=BOTH, expand=True)
        # Line numbers gutter
        self.line_numbers = Text(self.textFrame, width=6, padx=4, takefocus=0, bd=0,
                                 bg='#f0f0f0', fg='#666666', state=DISABLED)
        self.line_numbers.pack(side=LEFT, fill=Y)

        self.scrollbar = Scrollbar(self.textFrame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Text area
        self.textArea = Text(
            self.textFrame,
            undo=True,
            wrap=NONE,
            yscrollcommand=self._on_textscroll,
            font=("Courier New", 10)
        )
        self.textArea.pack(side=RIGHT, fill=BOTH, expand=True)

        # Scrollbar command should scroll both text and line numbers
        def _on_scrollbar(*args):
            try:
                self.textArea.yview(*args)
                self.line_numbers.yview(*args)
            except Exception:
                pass

        self.scrollbar.config(command=_on_scrollbar)
        
        # Track modifications
        self.textArea.bind('<<Modified>>', self.on_text_modified)
        # Update line numbers on edits and keys
        self.textArea.bind('<KeyRelease>', lambda e: self._update_line_numbers())
        self.textArea.bind('<MouseWheel>', lambda e: self._update_line_numbers())
        self.line_numbers.bind('<Button-1>', lambda e: self._on_ln_click(e))
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-x>', lambda e: self.cut())
        self.root.bind('<Control-c>', lambda e: self.copy())
        self.root.bind('<Control-v>', lambda e: self.paste())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Control-g>', lambda e: self.goto_line_dialog())
        self.root.bind('<Control-f>', lambda e: self.find_replace_dialog())
        
        # Bind window close
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        
        # Word wrap state
        self.word_wrap_enabled = False
        
    def on_text_modified(self, event=None):
        """Track when text is modified"""
        if self.textArea.edit_modified():
            self.modified = True
            self.update_title()
            self.textArea.edit_modified(False)
            # Update line numbers when content changes
            try:
                self._update_line_numbers()
            except Exception:
                pass
    
    def update_title(self):
        """Update window title"""
        title = "BalrogNPC - "
        if self.current_file:
            title += os.path.basename(self.current_file)
        else:
            title += "Untitled"
        
        if self.modified:
            title += " *"
        
        self.root.title(title)
    
    def check_save(self):
        """Check if user wants to save before proceeding"""
        if self.modified:
            response = messagebox.askyesnocancel(
                "BalrogNPC",
                "Do you want to save changes?"
            )
            if response is True:  # Yes
                return self.save_file()
            elif response is False:  # No
                return True
        return True

    def find_replace_dialog(self):
        dlg = Toplevel(self.root)
        dlg.title("Find & Replace")
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.geometry("460x186")

        frame = ttk.Frame(dlg, padding=12)
        frame.pack(fill=BOTH, expand=True)

        ttk.Label(frame, text="Find:").grid(row=0, column=0, sticky='w')
        find_var = StringVar()
        find_entry = ttk.Entry(frame, textvariable=find_var, width=60)
        find_entry.grid(row=0, column=1, columnspan=3, sticky='ew', pady=4)

        ttk.Label(frame, text="Replace:").grid(row=1, column=0, sticky='w')
        replace_var = StringVar()
        replace_entry = ttk.Entry(frame, textvariable=replace_var, width=60)
        replace_entry.grid(row=1, column=1, columnspan=3, sticky='ew', pady=4)

        regex_var = BooleanVar(value=False)
        case_var = BooleanVar(value=False)  # Strict case when True
        wholeword_var = BooleanVar(value=False)
        highlight_var = BooleanVar(value=False)

        ttk.Checkbutton(frame, text="Use Regex", variable=regex_var).grid(row=2, column=1, sticky='w')
        ttk.Checkbutton(frame, text="Case Sensitive", variable=case_var).grid(row=2, column=2, sticky='w')
        ttk.Checkbutton(frame, text="Whole Word", variable=wholeword_var).grid(row=2, column=3, sticky='w')
        ttk.Checkbutton(frame, text="Highlight All Matches", variable=highlight_var, command=lambda: highlight_all()).grid(row=3, column=1, sticky='w')

        status_var = StringVar(value="")
        status_label = ttk.Label(frame, textvariable=status_var, foreground='#333333')
        status_label.grid(row=4, column=0, columnspan=4, sticky='w', pady=(6,0))

        # Configure highlight tag
        try:
            self.textArea.tag_config('find_highlight', background='#fffb7d')
        except Exception:
            pass

        def clear_highlights():
            try:
                self.textArea.tag_remove('find_highlight', '1.0', 'end')
            except Exception:
                pass

        def highlight_all():
            clear_highlights()
            if not highlight_var.get():
                return
            pattern = find_var.get()
            if not pattern:
                status_var.set('No search pattern')
                return
            content = self.textArea.get('1.0', 'end-1c')
            try:
                import re
                flags = 0
                if not case_var.get():
                    flags |= re.IGNORECASE

                if not regex_var.get():
                    pat = re.escape(pattern)
                    if wholeword_var.get():
                        pat = r'\b' + pat + r'\b'
                else:
                    pat = pattern
                    if wholeword_var.get():
                        # wrap with word boundaries if not already
                        if not pat.startswith('\\b') and not pat.endswith('\\b'):
                            pat = r'\\b' + pat + r'\\b'

                regex = re.compile(pat, flags)
                for m in regex.finditer(content):
                    # convert offsets to indices
                    start_off, end_off = m.start(), m.end()
                    sidx = self.textArea.index(f'1.0 + {start_off}c')
                    eidx = self.textArea.index(f'1.0 + {end_off}c')
                    self.textArea.tag_add('find_highlight', sidx, eidx)

                status_var.set('Highlights updated')
            except Exception as e:
                status_var.set(f'Error: {e}')

        # Helper functions
        def get_search_start_index():
            try:
                if self.textArea.tag_ranges('sel'):
                    # start after current selection
                    idx = self.textArea.index('sel.last')
                    # advance by one char to avoid re-finding same selection
                    return self.textArea.index(f"{idx} + 1c")
                else:
                    return self.textArea.index('insert')
            except Exception:
                return '1.0'

        def find_next(event=None):
            pattern = find_var.get()
            if not pattern:
                status_var.set('No search pattern')
                return False

            start_index = get_search_start_index()
            try:
                if regex_var.get() or wholeword_var.get():
                    import re
                    flags = 0
                    if not case_var.get():
                        flags |= re.IGNORECASE

                    pat = pattern if regex_var.get() else re.escape(pattern)
                    if wholeword_var.get() and regex_var.get():
                        # ensure boundaries
                        if not pat.startswith('\\b'):
                            pat = r'\\b' + pat
                        if not pat.endswith('\\b'):
                            pat = pat + r'\\b'
                    elif wholeword_var.get() and not regex_var.get():
                        pat = r'\\b' + pat + r'\\b'

                    content = self.textArea.get('1.0', 'end-1c')
                    line, col = map(int, start_index.split('.'))
                    lines = content.splitlines(True)
                    offset = sum(len(lines[i]) for i in range(max(0, line-1))) + col
                    regex = re.compile(pat, flags)
                    m = regex.search(content, pos=offset)
                    if not m:
                        status_var.set('No more matches')
                        return False
                    start_off, end_off = m.start(), m.end()
                    sidx = self.textArea.index(f'1.0 + {start_off}c')
                    eidx = self.textArea.index(f'1.0 + {end_off}c')
                else:
                    nocase = not case_var.get()
                    sidx = self.textArea.search(pattern, start_index, nocase=nocase, stopindex='end')
                    if not sidx:
                        status_var.set('No more matches')
                        return False
                    eidx = f"{sidx} + {len(pattern)}c"

                # Select match
                self.textArea.tag_remove('sel', '1.0', 'end')
                self.textArea.tag_add('sel', sidx, eidx)
                self.textArea.mark_set('insert', eidx)
                self.textArea.see(sidx)
                status_var.set(f'Match at {sidx}')
                if highlight_var.get():
                    highlight_all()
                return True
            except Exception as e:
                status_var.set(f'Error: {e}')
                return False

        def find_prev(event=None):
            pattern = find_var.get()
            if not pattern:
                status_var.set('No search pattern')
                return False

            # Determine search offset (position before current selection/start)
            try:
                if self.textArea.tag_ranges('sel'):
                    idx = self.textArea.index('sel.first')
                    start_index = self.textArea.index(f"{idx} - 1c")
                else:
                    start_index = self.textArea.index('insert')

                if regex_var.get() or wholeword_var.get():
                    import re
                    flags = 0
                    if not case_var.get():
                        flags |= re.IGNORECASE

                    pat = pattern if regex_var.get() else re.escape(pattern)
                    if wholeword_var.get() and not regex_var.get():
                        pat = r'\\b' + pat + r'\\b'
                    elif wholeword_var.get() and regex_var.get():
                        if not pat.startswith('\\b'):
                            pat = r'\\b' + pat
                        if not pat.endswith('\\b'):
                            pat = pat + r'\\b'

                    content = self.textArea.get('1.0', 'end-1c')
                    line, col = map(int, start_index.split('.'))
                    lines = content.splitlines(True)
                    offset = sum(len(lines[i]) for i in range(max(0, line-1))) + col
                    regex = re.compile(pat, flags)
                    last_match = None
                    for m in regex.finditer(content):
                        if m.start() < offset:
                            last_match = m
                        else:
                            break
                    if not last_match:
                        status_var.set('No previous match')
                        return False
                    sidx = self.textArea.index(f'1.0 + {last_match.start()}c')
                    eidx = self.textArea.index(f'1.0 + {last_match.end()}c')
                else:
                    # use Text.search backwards
                    sidx = self.textArea.search(pattern, start_index, backwards=True, nocase=not case_var.get(), stopindex='1.0')
                    if not sidx:
                        status_var.set('No previous match')
                        return False
                    eidx = f"{sidx} + {len(pattern)}c"

                self.textArea.tag_remove('sel', '1.0', 'end')
                self.textArea.tag_add('sel', sidx, eidx)
                self.textArea.mark_set('insert', eidx)
                self.textArea.see(sidx)
                status_var.set(f'Match at {sidx}')
                if highlight_var.get():
                    highlight_all()
                return True
            except Exception as e:
                status_var.set(f'Error: {e}')
                return False

        def replace_next():
            # If selection present and matches pattern, replace it; else find next then replace
            repl = replace_var.get()
            if self.textArea.tag_ranges('sel'):
                try:
                    sel_start = self.textArea.index('sel.first')
                    sel_end = self.textArea.index('sel.last')
                    self.textArea.delete(sel_start, sel_end)
                    self.textArea.insert(sel_start, repl)
                    end_idx = self.textArea.index(f"{sel_start} + {len(repl)}c")
                    self.textArea.mark_set('insert', end_idx)
                    self.textArea.see(end_idx)
                    self.modified = True
                    self.update_title()
                    self._update_line_numbers()
                    status_var.set(f'Replaced at {sel_start}')
                    if highlight_var.get():
                        highlight_all()
                    return True
                except Exception as e:
                    status_var.set(f'Error replacing: {e}')
                    return False
            else:
                found = find_next()
                if found:
                    return replace_next()
                return False

        def replace_all():
            pattern = find_var.get()
            if not pattern:
                status_var.set('No search pattern')
                return
            repl = replace_var.get()
            try:
                content = self.textArea.get('1.0', 'end-1c')
                count = 0
                import re
                flags = 0
                if not case_var.get():
                    flags |= re.IGNORECASE

                if regex_var.get():
                    pat = pattern
                else:
                    pat = re.escape(pattern)
                if wholeword_var.get():
                    pat = r'\\b' + pat + r'\\b'

                new, count = re.subn(pat, repl, content, flags=flags)

                # Replace entire content
                self.textArea.delete('1.0', 'end')
                self.textArea.insert('1.0', new)
                self.modified = True
                self.update_title()
                self._update_line_numbers()
                status_var.set(f'Replaced {count} occurrence(s)')
                if highlight_var.get():
                    highlight_all()
            except Exception as e:
                status_var.set(f'Error: {e}')

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=4, sticky='e', pady=(12,0))

        ttk.Button(btn_frame, text="Find Prev", command=find_prev).pack(side=LEFT, padx=4)
        ttk.Button(btn_frame, text="Find Next", command=find_next).pack(side=LEFT, padx=4)
        ttk.Button(btn_frame, text="Replace Next", command=replace_next).pack(side=LEFT, padx=4)
        ttk.Button(btn_frame, text="Replace All", command=replace_all).pack(side=LEFT, padx=4)
        ttk.Button(btn_frame, text="Close", command=lambda: (clear_highlights(), dlg.destroy())).pack(side=LEFT, padx=4)

        # Bind Enter and Shift+Enter
        find_entry.bind('<Return>', lambda e: find_next())
        find_entry.bind('<Shift-Return>', lambda e: find_prev())
        replace_entry.bind('<Return>', lambda e: replace_next())

        find_entry.focus()
        dlg.wait_window()

    def _update_line_numbers(self):
        try:
            last_index = self.textArea.index('end-1c')
            last_line = int(last_index.split('.')[0])
            nums = '\n'.join(str(i) for i in range(1, last_line + 1))
            self.line_numbers.config(state=NORMAL)
            self.line_numbers.delete('1.0', 'end')
            self.line_numbers.insert('1.0', nums)
            self.line_numbers.config(state=DISABLED)
        except Exception:
            pass

    def _on_textscroll(self, first, last):
        # Called by text widget via its yscrollcommand; sync line numbers and scrollbar
        try:
            # first/last are strings like '0.0'.. we move line numbers accordingly
            self.line_numbers.yview_moveto(first)
            # update scrollbar
            try:
                self.scrollbar.set(first, last)
            except Exception:
                pass
        except Exception:
            pass

    def _on_ln_click(self, event):
        try:
            # find line clicked and move cursor there
            index = self.line_numbers.index(f"@0,{event.y}")
            line = int(index.split('.')[0])
            self.textArea.mark_set('insert', f"{line}.0")
            self.textArea.see(f"{line}.0")
            self.textArea.focus()
        except Exception:
            pass

    def goto_line_dialog(self):
        try:
            line = simpledialog.askinteger("Go To Line", "Line number:", parent=self.root, minvalue=1)
            if line is None:
                return
            self.textArea.mark_set('insert', f"{line}.0")
            self.textArea.see(f"{line}.0")
            self.textArea.focus()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to go to line: {e}")
            return False
        return True
    
    def new_file(self):
        """Create a new file"""
        if not self.check_save():
            return
        
        self.textArea.delete(1.0, END)
        self.current_file = None
        self.modified = False
        self.update_title()
        try:
            self._update_line_numbers()
        except Exception:
            pass
    
    def open_file(self):
        """Open an existing file"""
        if not self.check_save():
            return
        
        filepath = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("rAthena Scripts", "*.npc;*.txt"),
                ("YAML Files", "*.yml;*.yaml")
            ]
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.textArea.delete(1.0, END)
                self.textArea.insert(1.0, content)
                self.current_file = filepath
                self.modified = False
                self.update_title()
                try:
                    self._update_line_numbers()
                except Exception:
                    pass
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Could not open file:\n{str(e)}"
                )
    
    def save_file(self):
        """Save current file"""
        if self.current_file:
            return self._save_to_file(self.current_file)
        else:
            return self.save_as_file()
    
    def save_as_file(self):
        """Save file with new name"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("rAthena Scripts", "*.npc"),
                ("YAML Files", "*.yml")
            ]
        )
        
        if filepath:
            return self._save_to_file(filepath)
        return False
    
    def _save_to_file(self, filepath):
        """Internal method to save to file"""
        try:
            content = self.textArea.get(1.0, END)
            # Remove trailing newline that Text widget adds
            if content.endswith('\n'):
                content = content[:-1]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.current_file = filepath
            self.modified = False
            self.update_title()
            return True
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not save file:\n{str(e)}"
            )
            return False
    
    def undo(self):
        """Undo last action"""
        try:
            self.textArea.edit_undo()
        except:
            pass
    
    def cut(self):
        """Cut selected text"""
        try:
            self.textArea.event_generate("<<Cut>>")
        except:
            pass
    
    def copy(self):
        """Copy selected text"""
        try:
            self.textArea.event_generate("<<Copy>>")
        except:
            pass
    
    def paste(self):
        """Paste from clipboard"""
        try:
            self.textArea.event_generate("<<Paste>>")
        except:
            pass
    
    def delete(self):
        """Delete selected text"""
        try:
            self.textArea.delete(SEL_FIRST, SEL_LAST)
        except:
            pass
    
    def select_all(self):
        """Select all text"""
        self.textArea.tag_add(SEL, "1.0", END)
        self.textArea.mark_set(INSERT, "1.0")
        self.textArea.see(INSERT)
        return 'break'
    
    def toggle_word_wrap(self):
        """Toggle word wrap on/off"""
        if self.word_wrap_enabled:
            self.textArea.config(wrap=NONE)
            self.word_wrap_enabled = False
        else:
            self.textArea.config(wrap=WORD)
            self.word_wrap_enabled = True
    
    def change_font(self):
        """Open font dialog"""
        # Simple font size changer
        current_font = tkfont.Font(font=self.textArea['font'])
        
        dialog = Toplevel(self.root)
        dialog.title("Font")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("300x150")
        
        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill=BOTH, expand=True)
        
        Label(frame, text="Font Size:").pack(anchor=W)
        
        size_var = IntVar(value=current_font.actual()['size'])
        
        size_scale = Scale(
            frame,
            from_=8,
            to=24,
            orient=HORIZONTAL,
            variable=size_var
        )
        size_scale.pack(fill=X, pady=10)
        
        def apply_font():
            new_size = size_var.get()
            self.textArea.config(font=("Courier New", new_size))
            dialog.destroy()
        
        Button(frame, text="OK", command=apply_font, width=10).pack(side=RIGHT, padx=5)
        Button(frame, text="Cancel", command=dialog.destroy, width=10).pack(side=RIGHT)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """BalrogNPC - rAthena Script Editor
Version 1.0

A simple text editor with integrated rAthena script generation tools.

Based on Windows XP Notepad with rAthena Tools menu.

© 2025"""
        
        messagebox.showinfo("About BalrogNPC", about_text)
    
    def exit_app(self):
        """Exit application"""
        if not self.check_save():
            return
        
        self.root.destroy()


def main():
    """Main entry point"""
    root = Tk()
    app = BalrogNPC(root)
    
    # Set icon if available
    try:
        icon_path = os.path.join(_current_dir, 'icon.ico')
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass
    
    root.mainloop()


if __name__ == "__main__":
    main()
