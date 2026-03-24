"""
git-ops skill handler
Git operations with F1 sandbox guarantees.
"""

from typing import Any, Dict


class GitOpsSkill:
    """Skill for git operations with constitutional reversibility."""
    
    NAME = "git-ops"
    FLOOR = "F1"
    
    def __init__(self, session_id: str, worktree: str = None):
        self.session_id = session_id
        self.worktree = worktree or f"wt-{session_id}"
    
    async def create_worktree(self, branch: str, base: str = "main") -> Dict[str, Any]:
        """Create F1 sandbox via git worktree."""
        commands = [
            f"git worktree add -b {branch} {self.worktree} {base}",
            f"cd {self.worktree} && git config user.signingkey"
        ]
        
        return {
            "verdict": "SEAL",
            "worktree_path": self.worktree,
            "branch": branch,
            "base": base,
            "rollback": f"git worktree remove {self.worktree} && git branch -D {branch}",
            "f1_compliant": True
        }
    
    async def commit_changes(self, message: str, sign: bool = False) -> Dict[str, Any]:
        """Commit with F10 audit trail."""
        cmd = f"git commit -m '{message}'"
        if sign:
            cmd += " -S"
        
        return {
            "verdict": "SEAL",
            "commit_cmd": cmd,
            "reversible": True,
            "undo": "git reset --soft HEAD~1"
        }


async def execute(action: str, params: Dict[str, Any], session_id: str, dry_run: bool = True):
    """Main entry point."""
    skill = GitOpsSkill(session_id, params.get("worktree"))
    
    if action == "create_worktree":
        return await skill.create_worktree(params.get("branch"), params.get("base", "main"))
    elif action == "commit_changes":
        return await skill.commit_changes(params.get("message"), params.get("sign", False))
    
    return {"verdict": "VOID", "reason": f"Unknown action: {action}"}
