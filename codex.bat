@echo off
set "PYTHONPATH=%~dp0;%PYTHONPATH%"
uv run python "%~dp0codex.py" %*
