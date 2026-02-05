---
description: How to set up and run the arifOS Constitutional Kernel (FastMCP) locally
---

# arifOS Local MCP Startup Workflow

This workflow describes the canonical process for initializing and running the arifOS Constitutional Kernel on a local machine using the `fastmcp` implementation.

## Prerequisites
- Python 3.10+
- Virtual environment support

## Setup Steps

### 1. Initialize Workspace
Navigate to your project root:
```powershell
cd C:\Users\User\arifOS
```

### 2. Create and Activate Virtual Environment
```powershell
# Create venv if it doesn't exist
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install fastmcp
# Alternatively, install all project dependencies
pip install -e .
```

### 4. Run the Kernel (FastMCP Mode)
// turbo
```powershell
# Current entry point
python codebase/mcp/fastmcp_clean.py
```

## Troubleshooting
- **ImportErrors**: Ensure your `PYTHONPATH` includes the current directory.
  - PowerShell: `$env:PYTHONPATH = "."`
  - CMD: `set PYTHONPATH=.`
- **Port Conflict**: The server runs on port `6274` by default. Ensure it's not occupied.
