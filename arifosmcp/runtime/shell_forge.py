import subprocess
import os
from typing import Dict, Any, List, Optional
import shlex

class ShellForge:
    """Hardened entry point for shell operations in arifOS."""
    
    def __init__(self, check_floors=True):
        self.check_floors = check_floors

    def execute(self, command: str, cwd: str = None) -> Dict[str, Any]:
        """Execute a shell command with injection defense."""
        # Simple injection defense: only allow shlex-split commands
        args = shlex.split(command)
        
        try:
            result = subprocess.run(
                args,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "success": False
            }

forge = ShellForge()
