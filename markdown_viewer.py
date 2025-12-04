#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown Documentation Viewer for BalrogNPC

Provides a built-in documentation viewer with:
- Markdown rendering
- Document navigation
- Clickable links between documents
- Search functionality
- Table of contents
"""

from tkinter import *
from tkinter import ttk, messagebox, font as tkfont
import os
import re
from pathlib import Path


class MarkdownViewer:
    """
    Markdown viewer window with navigation and search.
    Converts markdown to formatted text with clickable links.
    """
    
    def __init__(self, parent, docs_dir=None):
        """
        Initialize the markdown viewer.
        
        Args:
            parent: Parent Tkinter window
            docs_dir: Path to docs directory (defaults to ./docs)
        """
        self.parent = parent
        self.docs_dir = docs_dir or os.path.join(os.path.dirname(__file__), 'docs')
        
        # Create window
        self.window = Toplevel(parent)
        self.window.title("BalrogNPC Documentation")
        self.window.geometry("900x700")
        self.window.transient(parent)
        
        # Document history for back/forward navigation
        self.history = []
        self.history_index = -1
        
        # Current document
        self.current_doc = None
        
        # Available documents (scan docs directory)
        self.available_docs = self._scan_docs()
        
        # Build UI
        self._build_ui()
        
        # Load default document (INDEX.md or README.md)
        self._load_default_document()
        
        # Center window
        self._center_window()
    
    def _scan_docs(self):
        """Scan docs directory for markdown files."""
        docs = {}
        try:
            if os.path.isdir(self.docs_dir):
                for file in os.listdir(self.docs_dir):
                    if file.endswith('.md'):
                        name = file[:-3]  # Remove .md extension
                        path = os.path.join(self.docs_dir, file)
                        # Get first line as title
                        try:
                            with open(path, 'r', encoding='utf-8') as f:
                                first_line = f.readline().strip()
                                title = first_line.lstrip('#').strip() if first_line.startswith('#') else name
                        except:
                            title = name
                        docs[name] = {
                            'path': path,
                            'title': title,
                            'filename': file
                        }
        except Exception as e:
            print(f"Error scanning docs: {e}")
        
        return docs
    
    def _build_ui(self):
        """Build the user interface."""
        # Toolbar
        toolbar = ttk.Frame(self.window)
        toolbar.pack(side=TOP, fill=X, padx=5, pady=5)
        
        # Navigation buttons
        self.back_btn = ttk.Button(toolbar, text="◀ Back", command=self._go_back, width=8)
        self.back_btn.pack(side=LEFT, padx=2)
        self.back_btn.state(['disabled'])
        
        self.forward_btn = ttk.Button(toolbar, text="Forward ▶", command=self._go_forward, width=10)
        self.forward_btn.pack(side=LEFT, padx=2)
        self.forward_btn.state(['disabled'])
        
        ttk.Separator(toolbar, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=8)
        
        # Document selector
        ttk.Label(toolbar, text="Document:").pack(side=LEFT, padx=(0, 5))
        
        doc_names = sorted(self.available_docs.keys())
        self.doc_var = StringVar()
        self.doc_combo = ttk.Combobox(
            toolbar, 
            textvariable=self.doc_var, 
            values=doc_names,
            state='readonly',
            width=30
        )
        self.doc_combo.pack(side=LEFT, padx=2)
        self.doc_combo.bind('<<ComboboxSelected>>', self._on_doc_selected)
        
        ttk.Separator(toolbar, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=8)
        
        # Search
        ttk.Label(toolbar, text="Search:").pack(side=LEFT, padx=(0, 5))
        self.search_var = StringVar()
        self.search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=LEFT, padx=2)
        self.search_entry.bind('<Return>', lambda e: self._search_in_doc())
        
        ttk.Button(toolbar, text="Find", command=self._search_in_doc, width=6).pack(side=LEFT, padx=2)
        
        # Main content area with sidebar
        content_frame = ttk.Frame(self.window)
        content_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # Sidebar for table of contents
        sidebar = ttk.Frame(content_frame, width=200)
        sidebar.pack(side=LEFT, fill=Y, padx=(0, 5))
        
        ttk.Label(sidebar, text="Contents", font=('Arial', 10, 'bold')).pack(anchor=W, pady=(0, 5))
        
        # TOC listbox
        toc_frame = ttk.Frame(sidebar)
        toc_frame.pack(fill=BOTH, expand=True)
        
        self.toc_listbox = Listbox(toc_frame, width=25, height=20)
        self.toc_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        
        toc_scroll = ttk.Scrollbar(toc_frame, orient=VERTICAL, command=self.toc_listbox.yview)
        toc_scroll.pack(side=RIGHT, fill=Y)
        self.toc_listbox.config(yscrollcommand=toc_scroll.set)
        
        self.toc_listbox.bind('<<ListboxSelect>>', self._on_toc_select)
        
        # Document display area
        doc_frame = ttk.Frame(content_frame)
        doc_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Text widget for rendered markdown
        self.text_widget = Text(
            doc_frame,
            wrap=WORD,
            font=('Arial', 10),
            padx=10,
            pady=10,
            bg='white',
            state=DISABLED
        )
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(doc_frame, orient=VERTICAL, command=self.text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        
        # Configure text tags for formatting
        self._configure_tags()
        
        # Make links clickable
        self.text_widget.tag_bind('link', '<Button-1>', self._on_link_click)
        self.text_widget.tag_bind('link', '<Enter>', lambda e: self.text_widget.config(cursor='hand2'))
        self.text_widget.tag_bind('link', '<Leave>', lambda e: self.text_widget.config(cursor=''))
        
        # Status bar
        status_frame = ttk.Frame(self.window)
        status_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
        
        self.status_var = StringVar(value="Ready")
        ttk.Label(status_frame, textvariable=self.status_var, relief=SUNKEN).pack(fill=X)
    
    def _configure_tags(self):
        """Configure text tags for markdown formatting."""
        # Headers
        self.text_widget.tag_config('h1', font=('Arial', 18, 'bold'), spacing3=10, foreground='#2c3e50')
        self.text_widget.tag_config('h2', font=('Arial', 16, 'bold'), spacing3=8, foreground='#34495e')
        self.text_widget.tag_config('h3', font=('Arial', 14, 'bold'), spacing3=6, foreground='#34495e')
        self.text_widget.tag_config('h4', font=('Arial', 12, 'bold'), spacing3=4, foreground='#34495e')
        self.text_widget.tag_config('h5', font=('Arial', 11, 'bold'), spacing3=3, foreground='#34495e')
        self.text_widget.tag_config('h6', font=('Arial', 10, 'bold'), spacing3=2, foreground='#34495e')
        
        # Text styles
        self.text_widget.tag_config('bold', font=('Arial', 10, 'bold'))
        self.text_widget.tag_config('italic', font=('Arial', 10, 'italic'))
        self.text_widget.tag_config('code_inline', font=('Courier New', 9), background='#f5f5f5', foreground='#c7254e')
        
        # Code blocks
        self.text_widget.tag_config(
            'code_block',
            font=('Courier New', 10),
            background='#f0f0f0',
            foreground='#333333',
            lmargin1=20,
            lmargin2=20,
            spacing1=6,
            spacing3=6
        )
        
        # Lists
        self.text_widget.tag_config('list', lmargin1=30, lmargin2=30, spacing1=2)
        
        # Links
        self.text_widget.tag_config('link', foreground='#0366d6', underline=True)
        self.text_widget.tag_config('link_hover', foreground='#0366d6', underline=True, background='#f0f8ff')
        
        # Blockquotes
        self.text_widget.tag_config('blockquote', lmargin1=20, lmargin2=20, foreground='#666666',
                                   background='#f9f9f9', borderwidth=1, relief=SOLID, spacing1=5, spacing3=5)
        
        # Horizontal rule
        self.text_widget.tag_config('hr', foreground='#cccccc', spacing3=10)
        
        # Tables
        self.text_widget.tag_config('table_header', font=('Arial', 10, 'bold'), background='#f0f0f0')
        self.text_widget.tag_config('table_cell', font=('Arial', 10))
        
        # Highlights (for search)
        self.text_widget.tag_config('search_highlight', background='#ffff00')
        
        # Special formatting
        self.text_widget.tag_config('emoji', font=('Segoe UI Emoji', 10))
        self.text_widget.tag_config('checkbox_checked', foreground='#28a745')
        self.text_widget.tag_config('checkbox_unchecked', foreground='#6c757d')
    
    def _load_default_document(self):
        """Load the default document (INDEX.md or README.md)."""
        if 'INDEX' in self.available_docs:
            self.load_document('INDEX')
        elif 'README' in self.available_docs:
            self.load_document('README')
        elif self.available_docs:
            # Load first available document
            first_doc = sorted(self.available_docs.keys())[0]
            self.load_document(first_doc)
    
    def load_document(self, doc_name, add_to_history=True, anchor=None):
        """
        Load and render a markdown document.
        
        Args:
            doc_name: Name of document (without .md extension)
            add_to_history: Whether to add to navigation history
        """
        if doc_name not in self.available_docs:
            messagebox.showerror("Error", f"Document '{doc_name}' not found")
            return
        
        doc_info = self.available_docs[doc_name]
        
        try:
            # Read document
            with open(doc_info['path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update history
            if add_to_history:
                # Remove any forward history
                self.history = self.history[:self.history_index + 1]
                self.history.append(doc_name)
                self.history_index = len(self.history) - 1
                self._update_nav_buttons()
            
            # Update current document
            self.current_doc = doc_name
            
            # Update UI
            self.doc_var.set(doc_name)
            self.window.title(f"BalrogNPC Documentation - {doc_info['title']}")
            self.status_var.set(f"Loaded: {doc_info['filename']}")
            
            # Render markdown
            self._render_markdown(content)

            # Jump to anchor if provided
            if anchor:
                self._jump_to_anchor(anchor)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load document:\n{str(e)}")
    
    def _render_markdown(self, content):
        """
        Render markdown content to the text widget.
        
        Args:
            content: Markdown text content
        """
        # Enable editing
        self.text_widget.config(state=NORMAL)
        
        # Clear existing content
        self.text_widget.delete('1.0', END)
        
        # Clear TOC
        self.toc_listbox.delete(0, END)
        self.toc_items = []  # Store TOC items with their positions
        # Reset anchors map for current document
        self.anchors = {}
        
        # Parse and render markdown line by line
        lines = content.split('\n')
        i = 0
        in_code_block = False
        code_block_lines = []
        in_list = False
        in_table = False
        table_lines = []
        
        while i < len(lines):
            line = lines[i]
            
            # Code blocks
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_lines = []
                    i += 1
                    continue
                else:
                    # End of code block
                    in_code_block = False
                    self._insert_code_block('\n'.join(code_block_lines))
                    code_block_lines = []
                    i += 1
                    continue
            
            if in_code_block:
                code_block_lines.append(line)
                i += 1
                continue
            
            # Headers
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                level = len(header_match.group(1))
                text = header_match.group(2).strip()
                
                # Add to TOC
                if level <= 3:  # Only H1, H2, H3 in TOC
                    indent = '  ' * (level - 1)
                    self.toc_listbox.insert(END, f"{indent}{text}")
                    # Store position for jumping
                    pos = self.text_widget.index('insert')
                    self.toc_items.append(pos)
                # Store anchor mapping for header
                anchor_key = self._make_anchor_key(text)
                self.anchors[anchor_key] = self.text_widget.index('insert')
                
                self._insert_header(level, text)
                i += 1
                continue
            
            # Horizontal rule
            if re.match(r'^[-*_]{3,}$', line.strip()):
                self._insert_hr()
                i += 1
                continue
            
            # Tables (simple detection)
            if '|' in line and not in_table:
                # Check if it's a table
                if i + 1 < len(lines) and re.match(r'^\|?[\s:|-]+\|', lines[i + 1]):
                    in_table = True
                    table_lines = [line]
                    i += 1
                    continue
            
            if in_table:
                if '|' in line:
                    table_lines.append(line)
                    i += 1
                    continue
                else:
                    # End of table
                    in_table = False
                    self._insert_table(table_lines)
                    table_lines = []
                    continue
            
            # Lists
            list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.+)$', line)
            if list_match:
                indent = len(list_match.group(1))
                text = list_match.group(3)
                self._insert_list_item(text, indent)
                i += 1
                continue
            
            # Blockquotes
            if line.strip().startswith('>'):
                quote_text = line.strip()[1:].strip()
                self._insert_blockquote(quote_text)
                i += 1
                continue
            
            # Regular paragraph
            if line.strip():
                self._insert_paragraph(line)
            else:
                # Empty line
                self.text_widget.insert(END, '\n')
            
            i += 1
        
        # Disable editing
        self.text_widget.config(state=DISABLED)
        
        # Scroll to top
        self.text_widget.see('1.0')
    
    def _insert_header(self, level, text):
        """Insert a header with appropriate formatting."""
        tag = f'h{level}'
        
        # Process inline formatting
        self._insert_formatted_text(text, base_tag=tag)
        self.text_widget.insert(END, '\n\n')
    
    def _insert_paragraph(self, text):
        """Insert a paragraph with inline formatting."""
        self._insert_formatted_text(text)
        self.text_widget.insert(END, '\n')
    
    def _insert_formatted_text(self, text, base_tag=None):
        """
        Insert text with inline markdown formatting (bold, italic, code, links).
        
        Args:
            text: Text with markdown inline formatting
            base_tag: Base tag to apply to all text
        """
        # Parse inline markdown
        i = 0
        while i < len(text):
            # Links [text](url)
            link_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', text[i:])
            if link_match:
                link_text = link_match.group(1)
                link_url = link_match.group(2)
                
                # Insert link
                start_idx = self.text_widget.index('insert')
                tags = ['link']
                if base_tag:
                    tags.append(base_tag)
                self.text_widget.insert(END, link_text, tuple(tags))
                end_idx = self.text_widget.index('insert')
                
                # Store link URL as tag
                link_tag = f'link_{start_idx}'
                self.text_widget.tag_add(link_tag, start_idx, end_idx)
                self.text_widget.tag_bind(link_tag, '<Button-1>', 
                                         lambda e, url=link_url: self._on_link_click(e, url))
                
                i += link_match.end()
                continue
            
            # Inline code `code`
            code_match = re.match(r'`([^`]+)`', text[i:])
            if code_match:
                code_text = code_match.group(1)
                tags = ['code_inline']
                if base_tag:
                    tags.append(base_tag)
                self.text_widget.insert(END, code_text, tuple(tags))
                i += code_match.end()
                continue
            
            # Bold **text** or __text__
            bold_match = re.match(r'\*\*([^*]+)\*\*|__([^_]+)__', text[i:])
            if bold_match:
                bold_text = bold_match.group(1) or bold_match.group(2)
                tags = ['bold']
                if base_tag:
                    tags.append(base_tag)
                self.text_widget.insert(END, bold_text, tuple(tags))
                i += bold_match.end()
                continue
            
            # Italic *text* or _text_
            italic_match = re.match(r'\*([^*]+)\*|_([^_]+)_', text[i:])
            if italic_match:
                italic_text = italic_match.group(1) or italic_match.group(2)
                tags = ['italic']
                if base_tag:
                    tags.append(base_tag)
                self.text_widget.insert(END, italic_text, tuple(tags))
                i += italic_match.end()
                continue
            
            # Checkboxes (GitHub style)
            checkbox_match = re.match(r'- \[([ x])\] ', text[i:])
            if checkbox_match:
                checked = checkbox_match.group(1) == 'x'
                checkbox_text = '\u2611' if checked else '\u2610'  # Unicode checkbox characters
                tag = 'checkbox_checked' if checked else 'checkbox_unchecked'
                self.text_widget.insert(END, checkbox_text + ' ', tag)
                i += checkbox_match.end()
                continue
            
            # Regular character
            tags = [base_tag] if base_tag else []
            self.text_widget.insert(END, text[i], tuple(tags) if tags else None)
            i += 1
    
    def _insert_code_block(self, code):
        """Insert code block as normal text (no special rendering)."""
        # Ensure trailing newline
        code_text = code if code.endswith('\n') else code + '\n'
        self.text_widget.insert(END, code_text)
        # Spacing after block
        self.text_widget.insert(END, '\n')
    
    def _insert_list_item(self, text, indent=0):
        """Insert a list item."""
        bullet = '  ' * (indent // 2) + '\u2022 '  # Unicode bullet character
        self.text_widget.insert(END, bullet)
        self._insert_formatted_text(text, base_tag='list')
        self.text_widget.insert(END, '\n')
    
    def _insert_blockquote(self, text):
        """Insert a blockquote."""
        self.text_widget.insert(END, '  ')
        self._insert_formatted_text(text, base_tag='blockquote')
        self.text_widget.insert(END, '\n')
    
    def _insert_table(self, lines):
        """Insert a simple table."""
        if len(lines) < 2:
            return
        
        # Parse header
        header = [cell.strip() for cell in lines[0].split('|') if cell.strip()]
        
        # Insert header
        for i, cell in enumerate(header):
            self.text_widget.insert(END, cell.ljust(20), 'table_header')
            if i < len(header) - 1:
                self.text_widget.insert(END, ' | ', 'table_header')
        self.text_widget.insert(END, '\n')
        
        # Insert separator (skip lines[1] which is the markdown separator)
        self.text_widget.insert(END, '-' * (21 * len(header)), 'hr')
        self.text_widget.insert(END, '\n')
        
        # Insert rows
        for line in lines[2:]:
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            for i, cell in enumerate(cells):
                self._insert_formatted_text(cell.ljust(20), base_tag='table_cell')
                if i < len(cells) - 1:
                    self.text_widget.insert(END, ' | ')
            self.text_widget.insert(END, '\n')
        
        self.text_widget.insert(END, '\n')
    
    def _insert_hr(self):
        """Insert a horizontal rule."""
        self.text_widget.insert(END, '\u2500' * 80 + '\n\n', 'hr')  # Unicode horizontal line
    
    def _on_link_click(self, event, url=None):
        """
        Handle link clicks.
        
        Args:
            event: Click event
            url: URL or document reference
        """
        if not url:
            return
        
        # Internal link handling: file.md, file.md#anchor, #anchor
        if url.endswith('.md') or '.md#' in url:
            doc_part, _, anchor_part = url.partition('#')
            doc_name = os.path.splitext(os.path.basename(doc_part))[0] if doc_part else None
            anchor = anchor_part if anchor_part else None
            # If no document specified, use current
            if not doc_name:
                doc_name = self.current_doc
            # Check if document exists
            if doc_name in self.available_docs:
                self.load_document(doc_name, anchor=anchor)
                return
        
        # Check for anchor links within same document
        if url.startswith('#'):
            anchor = url[1:]
            self._jump_to_anchor(anchor)
            return
        
        # External link - show info
        self.status_var.set(f"External link: {url}")
        messagebox.showinfo("External Link", 
                          f"This is an external link:\n{url}\n\nOpen this in your web browser.")

    def _make_anchor_key(self, text):
        """Create a normalized anchor key from header text similar to GitHub style."""
        key = text.strip().lower()
        # Replace spaces with hyphens and remove non-alphanum except hyphens
        key = re.sub(r'\s+', '-', key)
        key = re.sub(r'[^a-z0-9\-]', '', key)
        return key

    def _jump_to_anchor(self, anchor):
        """Jump to a header anchor within the current document."""
        if not anchor:
            return
        key = self._make_anchor_key(anchor)
        pos = self.anchors.get(key)
        if pos:
            self.text_widget.see(pos)
            self.status_var.set(f"Jumped to section: #{key}")
        else:
            self.status_var.set(f"Section not found: #{key}")
    
    def _on_doc_selected(self, event=None):
        """Handle document selection from dropdown."""
        doc_name = self.doc_var.get()
        if doc_name and doc_name in self.available_docs:
            self.load_document(doc_name)
    
    def _on_toc_select(self, event=None):
        """Handle TOC item selection."""
        selection = self.toc_listbox.curselection()
        if selection and selection[0] < len(self.toc_items):
            # Jump to position
            pos = self.toc_items[selection[0]]
            self.text_widget.see(pos)
    
    def _go_back(self):
        """Navigate back in history."""
        if self.history_index > 0:
            self.history_index -= 1
            doc_name = self.history[self.history_index]
            self.load_document(doc_name, add_to_history=False)
            self._update_nav_buttons()
    
    def _go_forward(self):
        """Navigate forward in history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            doc_name = self.history[self.history_index]
            self.load_document(doc_name, add_to_history=False)
            self._update_nav_buttons()
    
    def _update_nav_buttons(self):
        """Update navigation button states."""
        if self.history_index > 0:
            self.back_btn.state(['!disabled'])
        else:
            self.back_btn.state(['disabled'])
        
        if self.history_index < len(self.history) - 1:
            self.forward_btn.state(['!disabled'])
        else:
            self.forward_btn.state(['disabled'])
    
    def _search_in_doc(self):
        """Search for text in current document."""
        search_term = self.search_var.get().strip()
        if not search_term:
            return
        
        # Remove previous highlights
        self.text_widget.tag_remove('search_highlight', '1.0', END)
        
        # Search and highlight
        start_pos = '1.0'
        count = 0
        first_match = None
        
        while True:
            pos = self.text_widget.search(search_term, start_pos, stopindex=END, nocase=True)
            if not pos:
                break
            
            if not first_match:
                first_match = pos
            
            # Highlight match
            end_pos = f"{pos}+{len(search_term)}c"
            self.text_widget.tag_add('search_highlight', pos, end_pos)
            
            start_pos = end_pos
            count += 1
        
        if count > 0:
            # Jump to first match
            self.text_widget.see(first_match)
            self.status_var.set(f"Found {count} occurrence(s) of '{search_term}'")
        else:
            self.status_var.set(f"'{search_term}' not found")
    
    def _center_window(self):
        """Center the window on parent."""
        try:
            self.window.update_idletasks()
            
            # Get parent position
            px = self.parent.winfo_rootx()
            py = self.parent.winfo_rooty()
            pw = self.parent.winfo_width()
            ph = self.parent.winfo_height()
            
            # Get window size
            w = self.window.winfo_width()
            h = self.window.winfo_height()
            
            # Calculate position
            x = px + (pw - w) // 2
            y = py + (ph - h) // 2
            
            self.window.geometry(f"{w}x{h}+{x}+{y}")
        except:
            pass


def open_documentation_viewer(parent, docs_dir=None):
    """
    Open the documentation viewer window.
    
    Args:
        parent: Parent Tkinter window
        docs_dir: Path to docs directory (optional)
    
    Returns:
        MarkdownViewer instance
    """
    viewer = MarkdownViewer(parent, docs_dir)
    return viewer


# Test standalone
if __name__ == "__main__":
    root = Tk()
    root.title("Test Window")
    root.geometry("400x300")
    
    def open_docs():
        open_documentation_viewer(root)
    
    Button(root, text="Open Documentation", command=open_docs).pack(pady=50)
    
    root.mainloop()
