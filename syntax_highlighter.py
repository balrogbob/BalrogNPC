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
                cfg = configparser.RawConfigParser()
                cfg.optionxform = lambda s: s  # preserve case of keys
                cfg.read(path, encoding='utf-8')
                if 'Syntax' not in cfg:
                    continue
                sec = cfg['Syntax']
                name = sec.get('name', os.path.splitext(fn)[0])
                # collect detect extensions (if any)
                exts_raw = sec.get('detect.ext', '')
                exts = [e.strip().lstrip('.') for e in re.split('[,;]', exts_raw) if e.strip()]

                # collect regex.* entries preserving order
                regexes = []
                tags = {}
                for k, v in sec.items():
                    if k.startswith('regex.') and k.endswith('_RE'):
                        token = k[len('regex.'): -len('_RE')]
                        regexes.append((token, v))
                    elif k.startswith('tag.') and (k.endswith('.fg') or k.endswith('.bg')):
                        # tag.<name>.(fg|bg)
                        parts = k.split('.')
                        if len(parts) >= 3:
                            tagname = parts[1]
                            which = parts[2]
                            tags.setdefault(tagname, {})[which] = v.strip() if v else ''

                # store parsed syntax
                self._syntaxes[name] = {
                    'file': path,
                    'name': name,
                    'exts': exts,
                    'regexes': regexes,
                    'tags': tags,
                }
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
