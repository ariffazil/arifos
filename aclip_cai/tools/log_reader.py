import os
from collections import deque

def log_tail(log_file: str = "aaa_mcp.log", lines: int = 50, pattern: str = "") -> dict:
    """
    Reads the last N lines of a log file, with an optional filter pattern.

    Args:
        log_file (str): The path to the log file.
        lines (int): The number of lines to read from the end of the file.
        pattern (str): A string pattern to filter for. Only lines containing
                       this pattern will be returned.

    Returns:
        dict: A dictionary containing the log file path and a list of
              the requested log lines.
    """
    if not os.path.exists(log_file):
        return {"log_file": log_file, "lines": [], "error": "Log file not found."}

    try:
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            # Use deque for efficient append and fixed-length storage
            last_lines = deque(f, maxlen=lines)

        if pattern:
            # Filter lines based on the pattern
            filtered_lines = [line for line in last_lines if pattern in line]
        else:
            filtered_lines = list(last_lines)

        return {
            "log_file": log_file,
            "line_count": len(filtered_lines),
            "lines": filtered_lines,
        }
    except Exception as e:
        return {"log_file": log_file, "lines": [], "error": str(e)}
