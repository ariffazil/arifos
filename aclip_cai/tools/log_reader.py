import os
import time
from collections import deque


def log_tail(
    log_file: str = "aaa_mcp.log",
    lines: int = 50,
    pattern: str = "",
    log_path: str | None = None,
    grep_pattern: str | None = None,
    since_minutes: int | None = None,
) -> dict:
    """
    Reads the last N lines of a log file, with optional filtering.

    Args:
        log_file (str): Path to log file (default).
        lines (int): Number of lines to read.
        pattern (str): Simple string filter.
        log_path (str): Alias for log_file (for compatibility).
        grep_pattern (str): Alias for pattern (for compatibility).
        since_minutes (int): Filter lines modified in the last N minutes (Mock).

    Returns:
        dict: Log contents or error.
    """
    # 1. Handle Aliases
    target_file = log_path or log_file
    target_pattern = grep_pattern or pattern

    if not os.path.exists(target_file):
        return {
            "log_file": target_file,
            "lines": [],
            "error": "Log file not found.",
        }

    try:
        # Check mtime for since_minutes optimization (file level check)
        if since_minutes:
            mtime = os.path.getmtime(target_file)
            if (time.time() - mtime) > (since_minutes * 60):
                # File hasn't been touched in the window
                return {
                    "log_file": target_file,
                    "lines": [],
                    "info": f"File not modified in last {since_minutes} minutes.",
                }

        with open(target_file, encoding="utf-8", errors="ignore") as f:
            # Use deque for efficient append and fixed-length storage
            last_lines = deque(f, maxlen=lines)

        filtered_lines = list(last_lines)

        # 2. Apply Pattern Filter
        if target_pattern:
            filtered_lines = [line for line in filtered_lines if target_pattern in line]

        return {
            "log_file": target_file,
            "line_count": len(filtered_lines),
            "lines": filtered_lines,
            "filters": {
                "pattern": target_pattern,
                "since_minutes": since_minutes,
            },
        }
    except Exception as e:
        return {"log_file": target_file, "lines": [], "error": str(e)}
