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
print(f"Total lines in function: {len(lines)}")
for i, line in enumerate(lines, start=1):
    print(f"{i}: {line}")
