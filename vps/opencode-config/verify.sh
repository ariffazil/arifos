#!/bin/bash
echo "=== Verifying auth.json ==="
python3 -c "
import json
with open('/root/.local/share/opencode/auth.json') as f:
    d = json.load(f)
    print('Provider keys:', list(d.keys()))
    key = d.get('opencode', {}).get('apiKey', 'NOT FOUND')
    print('API Key prefix:', key[:15] + '...')
    print('auth.json: VALID')
"

echo ""
echo "=== Verifying .opencode.json ==="
python3 -c "
import json
with open('/root/arifOS/.opencode.json') as f:
    d = json.load(f)
    print('Model:', d.get('model'))
    print('Small model:', d.get('small_model'))
    print('Theme:', d.get('theme'))
    print('Enabled providers:', d.get('enabled_providers'))
    agents = d.get('agent', {})
    print('Agents:', list(agents.keys()))
    commands = d.get('command', {})
    print('Commands:', list(commands.keys()))
    mcp = d.get('mcp', {})
    print('MCP servers:', list(mcp.keys()))
    print('Instructions:', d.get('instructions'))
    print('.opencode.json: VALID')
"

echo ""
echo "=== OpenCode version ==="
opencode --version 2>/dev/null || echo "opencode not in PATH"
which opencode 2>/dev/null || echo "opencode binary not found"

echo ""
echo "=== VERIFICATION COMPLETE ==="
