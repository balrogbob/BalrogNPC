import os
import re
import configparser
from tkinter import END


class SyntaxHighlighter:
    """Load .ini syntax files and apply highlighting to a Tk Text widget.

    This is intentionally simple: it reads files from a `syntax` directory, loads
    regex.* entries as patterns and tag.*.fg/bg entries as colors, then applies
    tags by searching the whole buffer. Highlighting is scheduled via
    `after` to avoid running on every keystroke.
    """

    def __init__(self, text_widget, syntax_dir=None):
        self.text = text_widget
        self.root = self.text.winfo_toplevel()
        self.syntax_dir = syntax_dir or os.path.join(os.path.dirname(__file__), 'syntax')
        self._syntaxes = {}  # name -> dict
        self._current = None
        self._after_id = None
        self._load_all_syntaxes()

    def _load_all_syntaxes(self):
        if not os.path.isdir(self.syntax_dir):
            return

        for fn in sorted(os.listdir(self.syntax_dir)):
            if not fn.lower().endswith('.ini'):
                continue
            path = os.path.join(self.syntax_dir, fn)
            try:
                # Prefer a line-based parser for the [Syntax] section to preserve
                # complex regex RHS exactly as written in the INI file.
                regexes = []
                tags = {}
                csv_lists = {}
                name = None
                exts = []
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        in_syntax = False
                        for raw in f:
                            line = raw.rstrip('\n')
                            s = line.strip()
                            if not in_syntax:
                                if s.startswith('[') and s.lower().startswith('[syntax'):
                                    in_syntax = True
                                continue
                            # end of syntax section
                            if s.startswith('[') and in_syntax:
                                break
                            if not s or s.startswith(';') or s.startswith('#'):
                                continue
                            # name
                            m = re.match(r'^name\s*=\s*(.*)$', line, flags=re.I)
                            if m:
                                name = m.group(1).strip()
                                continue
                            m = re.match(r'^detect\.ext\s*=\s*(.*)$', line, flags=re.I)
                            if m:
                                exts_raw = m.group(1).strip()
                                exts = [e.strip().lstrip('.') for e in re.split('[,;]', exts_raw) if e.strip()]
                                continue
                            # regex lines: regex.<TOKEN>_RE = <pattern>
                            m = re.match(r'^\s*regex\.([^.=\s]+)_RE\s*=\s*(.*)$', line)
                            if m:
                                token = m.group(1)
                                pat = m.group(2).rstrip()
                                # Unwrap raw-style R"..." or R'...' fragments inside the
                                # pattern so they're valid Python regex syntax.
                                try:
                                    pat = re.sub(r'[rR]"((?:\\.|[^"\\])*)"', r'\1', pat, flags=re.DOTALL)
                                    pat = re.sub(r"[rR]'((?:\\.|[^'\\])*)'", r"\1", pat, flags=re.DOTALL)
                                    # If the entire RHS is quoted, unwrap it
                                    if (pat.startswith('"') and pat.endswith('"')) or (pat.startswith("'") and pat.endswith("'")):
                                        pat = pat[1:-1]
                                except Exception:
                                    pass
                                regexes.append((token, pat))
                                continue
                            # tag.<name>.(fg|bg)
                            m = re.match(r'^\s*tag\.([^.\s]+)\.(fg|bg)\s*=\s*(.*)$', line)
                            if m:
                                tagname = m.group(1)
                                which = m.group(2)
                                val = m.group(3).strip()
                                tags.setdefault(tagname, {})[which] = val
                                continue
                            # csv lists like keywords.csv = a,b,c
                            m = re.match(r'^\s*([A-Za-z0-9_]+)\.csv\s*=\s*(.*)$', line)
                            if m:
                                tok = m.group(1)
                                val = m.group(2).strip()
                                csv_lists[tok] = val
                                continue
                except Exception:
                    # fallback: skip file on read error
                    continue
                if not name:
                    name = os.path.splitext(fn)[0]

                # If CSV keyword lists were present, convert them to regexes
                for tok, csv in csv_lists.items():
                    try:
                        words = [w.strip() for w in re.split('[,\s]+', csv) if w.strip()]
                        if words:
                            parts = [re.escape(w) for w in words]
                            pat = r'\b(?:' + '|'.join(parts) + r')\b'
                            tname = tok.rstrip('s') if tok.endswith('s') else tok
                            regexes.append((tname.upper(), pat))
                    except Exception:
                        pass

                # store parsed syntax
                self._syntaxes[name] = {
                    'file': path,
                    'name': name,
                    'exts': exts,
                    'regexes': regexes,
                    'tags': tags,
                }
                # Optional debug: print parsed regex tokens and tag keys when enabled
                try:
                    if os.environ.get('SYNTAX_DEBUG'):
                        print(f"[SYNTAX_DEBUG] Loaded syntax: {name}")
                        print(f"  file: {path}")
                        print(f"  exts: {exts}")
                        print(f"  regex tokens: {[t for t, _ in regexes]}")
                        print(f"  tag keys: {list(tags.keys())}")
                except Exception:
                    pass
            except Exception:
                # ignore file parse errors
                continue

    def get_syntax_for_file(self, filepath):
        if not filepath:
            return None
        ext = os.path.splitext(filepath)[1].lstrip('.').lower()
        for name, s in self._syntaxes.items():
            if ext and ext in s.get('exts', []):
                return name
        return None

    def set_syntax(self, name):
        if name is None or name not in self._syntaxes:
            self._current = None
            return
        if self._current == name:
            return
        self._current = name
        # create tags on text widget
        syn = self._syntaxes[name]
        for token, _ in syn['regexes']:
            tag_key = self._choose_tag_key(token, syn['tags'])
            tagname = self._tagname(name, token)
            # make sure tag exists
            if tag_key and syn['tags'].get(tag_key):
                fg = syn['tags'][tag_key].get('fg') or None
                bg = syn['tags'][tag_key].get('bg') or None
                cfg = {}
                if fg:
                    cfg['foreground'] = fg
                if bg:
                    cfg['background'] = bg
                try:
                    self.text.tag_configure(tagname, **cfg)
                except Exception:
                    # fallback to simple configure
                    try:
                        if fg:
                            self.text.tag_configure(tagname, foreground=fg)
                        if bg:
                            self.text.tag_configure(tagname, background=bg)
                    except Exception:
                        pass
            else:
                # define empty tag so it can be removed/used
                try:
                    self.text.tag_configure(tagname)
                except Exception:
                    pass

    def _choose_tag_key(self, token, tagdict):
        # token typically like STRING, COMMENT, CLASS etc. Try to find matching
        # tag name in tagdict. Return the key or None.
        t = token.lower()
        if t in tagdict:
            return t
        # common substitutions
        subs = [t + '_name', t + 's', t.rstrip('s')]
        for s in subs:
            if s in tagdict:
                return s
        # fallback: find any tag that contains token
        for k in tagdict.keys():
            if t in k:
                return k
        return None

    def _tagname(self, syntax_name, token):
        return f"syn_{syntax_name}_{token.lower()}"

    def schedule_highlight(self, delay=200):
        try:
            if self._after_id:
                self.root.after_cancel(self._after_id)
        except Exception:
            pass
        self._after_id = self.root.after(delay, self.highlight)

    def highlight(self):
        self._after_id = None
        if not self._current:
            return
        syn = self._syntaxes.get(self._current)
        if not syn:
            return

        try:
            content = self.text.get('1.0', 'end-1c')
        except Exception:
            return

        # remove all current syntax tags
        for token, _ in syn['regexes']:
            try:
                self.text.tag_remove(self._tagname(self._current, token), '1.0', END)
            except Exception:
                pass

        # apply each regex in order
        for token, pat in syn['regexes']:
            if not pat:
                continue
            tagname = self._tagname(self._current, token)
            try:
                # compile with multiline/dotall to honor most patterns in ini
                regex = re.compile(pat, re.MULTILINE | re.DOTALL)
            except re.error:
                # invalid pattern: skip
                continue
            try:
                for m in regex.finditer(content):
                    try:
                        start_off = m.start()
                        end_off = m.end()
                        sidx = f'1.0 + {start_off}c'
                        eidx = f'1.0 + {end_off}c'
                        self.text.tag_add(tagname, sidx, eidx)
                    except Exception:
                        # if indexes fail, try using index arithmetic from spans
                        pass
            except Exception:
                # runtime error while iterating matches
                continue

    def set_syntax_for_file(self, filepath):
        name = self.get_syntax_for_file(filepath)
        if name:
            self.set_syntax(name)
        return name
