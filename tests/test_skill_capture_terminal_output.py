import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FORMAT_SCRIPT = REPO_ROOT / "skills" / "capture-terminal-output" / "scripts" / "format_output.py"


def run_format(style: str, text: str, line_numbers: bool = False) -> str:
    cmd = [sys.executable, str(FORMAT_SCRIPT), "--style", style, "--text", text]
    if line_numbers:
        cmd.append("--line-numbers")
    result = subprocess.check_output(cmd, text=True)
    return result


def test_format_box() -> None:
    text = "a\nbb"
    output = run_format("box", text)
    expected = "\n".join(
        [
            "┌────┐",
            "│ a  │",
            "│ bb │",
            "└────┘",
            "",
        ]
    )
    assert output == expected


def test_format_minimal_with_line_numbers() -> None:
    text = "foo\nbar"
    output = run_format("minimal", text, line_numbers=True)
    expected = "1 | foo\n2 | bar\n"
    assert output == expected
