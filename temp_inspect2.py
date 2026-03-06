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

source = inspect.getsource(gov._calculate_tri_witness_consensus)
lines = source.split("\n")
for i, line in enumerate(lines[219:240], start=220):
    print(f"{i}: {line}")

# Check exemption line exists
if 'tool == "reason_mind" and witness_name == "ai"' in source:
    print("\nExemption line exists: YES")
else:
    print("\nExemption line exists: NO")
