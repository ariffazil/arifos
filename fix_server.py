#!/usr/bin/env python3
lines = open('aaa_mcp/server.py', 'r', encoding='utf-8').readlines()

# Find the line with 'PHASE 13' and cut there
for i, line in enumerate(lines):
    if 'PHASE 13' in line:
        print(f'Found PHASE 13 at line {i+1}')
        lines = lines[:i-1]  # Cut before the comment
        break

# Add the closing lines
lines.append('\n\n# Apply annotations at module load time\n')
lines.append('_apply_tool_annotations()\n')
lines.append('\n\nif __name__ == "__main__":\n')
lines.append('    print("arifOS Constitutional Kernel - FastMCP Mode")\n')
lines.append('    mcp.run(transport="sse", port=6274)\n')

open('aaa_mcp/server.py', 'w', encoding='utf-8').writelines(lines)
print('File fixed')
