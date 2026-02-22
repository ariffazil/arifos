"""Strip all non-ASCII characters from docs site source files."""
import os, re, sys

EXTS = {'.md', '.tsx', '.ts', '.js', '.css'}
BASE = os.path.dirname(os.path.abspath(__file__))

# Map common unicode to ASCII replacements
REPLACE = {
    '\u2014': '-',   # em dash
    '\u2013': '-',   # en dash
    '\u2265': '>=',  # >=
    '\u2264': '<=',  # <=
    '\u0394': 'Delta',
    '\u03A9': 'Omega',
    '\u03A8': 'Psi',
    '\u03C4': 'tau',
    '\u03BA': 'kappa',
    '\u1D63': '_r',
    '\u2080': '_0',
    '\u00D7': 'x',
    '\u00B2': '^2',
    '\u00B3': '^3',
    '\u2026': '...',
    '\u00B7': '.',
    '\u00A9': '(c)',
}

count = 0
for root, dirs, files in os.walk(BASE):
    # Skip node_modules and .docusaurus
    dirs[:] = [d for d in dirs if d not in ('node_modules', '.docusaurus', 'build')]
    for fname in files:
        _, ext = os.path.splitext(fname)
        if ext not in EXTS:
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        # Apply known replacements first
        for k, v in REPLACE.items():
            content = content.replace(k, v)
        
        # Strip remaining non-ASCII (emoji, special chars)
        content = re.sub(r'[^\x00-\x7F]+', '', content)
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            rel = os.path.relpath(fpath, BASE)
            print(f"Fixed: {rel}")
            count += 1

print(f"\nDone. Fixed {count} files.")
