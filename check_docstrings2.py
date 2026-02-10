import re

content = open('aaa_mcp/server.py', 'r', encoding='utf-8').read()
lines = content.split('\n')

# Find all lines with triple quotes
for i, line in enumerate(lines):
    if '"""' in line:
        # Count how many triple quotes on this line
        count = line.count('"""')
        if count > 0:
            print(f'Line {i+1}: {count} triple-quote(s)')
            if i+1 >= 2880 or i+1 <= 10:
                print(f'  Content: {line[:80]}...')
