# Temporary fix - remove local_exec_guard wrapper
import re

with open("aaa_mcp/server.py", "r", encoding="utf-8") as f:
    content = f.read()

# Remove the local_exec_guard wrapper function
pattern = r'# =============================================================================\n# PHASE 13: LOCAL GUARDS\n# =============================================================================\n\n\n@mcp\.tool\(annotations=TOOL_ANNOTATIONS\.get\("local_exec_guard", \{\}\)\)\nasync def _local_exec_guard_wrapper\([^)]+\) -> dict:\n    """Execute local shell commands with constitutional floors\."""\n    return await local_exec_guard\([^)]+\)\n\n\n'

content = re.sub(pattern, "", content)

with open("aaa_mcp/server.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Removed local_exec_guard wrapper")
