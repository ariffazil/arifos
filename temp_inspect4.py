import sys
import inspect
import io
import contextlib

sys.path.insert(0, ".")

stderr_capture = io.StringIO()
with contextlib.redirect_stderr(stderr_capture):
    try:
        import arifos_aaa_mcp.governance as gov
    except ImportError as e:
        print(f"ImportError: {e}")
        sys.exit(1)

# Get source via inspect
source = inspect.getsource(gov._calculate_tri_witness_consensus)
lines = source.split("\n")
print("=== Source from inspect.getsource (first 60 lines) ===")
for i, line in enumerate(lines[:60], start=1):
    print(f"{i}: {line}")

# Now read file directly to compare
import os

file_path = os.path.join(os.path.dirname(__file__), "arifos_aaa_mcp", "governance.py")
with open(file_path, "r", encoding="utf-8") as f:
    file_lines = f.readlines()

# Find function start line
function_name = "_calculate_tri_witness_consensus"
start_line = -1
for idx, line in enumerate(file_lines, start=1):
    if line.strip().startswith("def " + function_name):
        start_line = idx
        break

print(f"\nFunction starts at line {start_line} in file")
print("File lines 220-240:")
for i in range(220, 241):
    if i <= len(file_lines):
        print(f"{i}: {file_lines[i - 1].rstrip()}")
    else:
        break

# Check exemption line existence
exemption_found = any(
    'tool == "reason_mind" and witness_name == "ai"' in line for line in file_lines
)
print(f"\nExemption line exists in file: {exemption_found}")
