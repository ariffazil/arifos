import re

content = open('aaa_mcp/server.py', 'r', encoding='utf-8').read()
matches = list(re.finditer(r'"""', content))

print(f'Total triple quotes: {len(matches)} (should be even)')
print(f'Last few at positions: {[m.start() for m in matches[-6:]]}')

# Check if odd
if len(matches) % 2 != 0:
    print('ERROR: Odd number of triple quotes - unclosed docstring!')
    # Find the problematic area
    lines = content.split('\n')
    in_docstring = False
    for i, line in enumerate(lines):
        if '"""' in line:
            if in_docstring:
                in_docstring = False
            else:
                in_docstring = True
                start_line = i + 1
    
    if in_docstring:
        print(f'Docstring opened around line {start_line} but never closed')
else:
    print('OK: All docstrings appear to be closed')
