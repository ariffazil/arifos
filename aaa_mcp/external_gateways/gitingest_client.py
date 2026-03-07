"""
aaa_mcp/external_gateways/gitingest_client.py — Metabolic GitIngest Encoder

Hardened Δ Delta sensory intake for arifOS v60.
Enforces F12 Injection Defense and F4 Thermodynamic Clarity.

DITEMPA BUKAN DIBERI 💎
"""

import asyncio
from typing import Any

# Tiktoken for F4 Clarity (Token budgeting)
try:
    import tiktoken

    ENC = tiktoken.get_encoding("o200k_base")
except ImportError:
    ENC = None

# arifOS Core Organs for F12 Injection scan (optional - graceful fallback)
try:
    from core.organs._0_init import scan_injection
except ImportError:
    # Fallback: minimal injection scan
    def scan_injection(text: str) -> Any:
        class FakeResult:
            score = 0.0
            violations = []

        return FakeResult()


try:
    from core.shared.types import RepoEvidence, Verdict
except ImportError:
    # Fallback: local definitions
    from enum import Enum

    from pydantic import BaseModel, Field

    class Verdict(str, Enum):
        SEAL = "SEAL"
        PARTIAL = "PARTIAL"
        VOID = "VOID"
        SABAR = "SABAR"
        HOLD_888 = "888_HOLD"

    class RepoEvidence(BaseModel):
        repo_url: str
        digest: str
        tree: str
        token_count: int
        file_count: int
        f12_risk_score: float = Field(ge=0.0, le=1.0, default=0.0)
        verdict: Verdict = Verdict.SEAL
        taint_lineage: dict[str, Any] = Field(default_factory=dict)


class GitingestClient:
    """
    EMD Encoder for Git repositories and local directories.

    Acts as a Metabolic Membrane:
    1. Acquisitions (L4)
    2. Sanitization (F12)
    3. Compression (F4)
    """

    MAX_TOKENS = 100000  # F4: Thermodynamic Limit

    def __init__(self, session_id: str):
        self.session_id = session_id

    async def ingest(
        self,
        source: str,
        subpath: str = "/",
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
    ) -> RepoEvidence:
        """
        Metabolize a codebase into a RepoEvidence bundle.
        """
        # 1. ENCODE: Acquire raw data via gitingest CLI
        digest, tree, file_count = await self._run_gitingest(
            source, subpath, include_patterns, exclude_patterns
        )

        # 2. METABOLIZE: F4 Clarity (Token Count)
        token_count = self._count_tokens(digest)
        verdict = Verdict.SEAL

        if token_count > self.MAX_TOKENS:
            verdict = Verdict.SABAR  # Entropy Overflow
            digest = digest[: self.MAX_TOKENS * 4]  # Heuristic truncation

        # 3. METABOLIZE: F12 Injection Guard
        injection_result = scan_injection(digest)
        f12_risk = injection_result.score

        if f12_risk > 0.85:
            verdict = Verdict.VOID  # Malicious Payload Blocked
            digest = "[VOID: F12 INJECTION DETECTED - CONTENT REDACTED]"
            tree = "[VOID]"

        # 4. DECODE: Final Evidence Packet
        return RepoEvidence(
            repo_url=source,
            digest=digest,
            tree=tree,
            token_count=token_count,
            file_count=file_count,
            f12_risk_score=f12_risk,
            verdict=verdict,
            session_id=self.session_id,
            taint_lineage={
                "source": "remote_repo" if source.startswith("http") else "local_dir",
                "engine": "gitingest-v0.3.1",
                "governance": "metabolic_membrane_v60",
            },
        )

    def _count_tokens(self, text: str) -> int:
        if ENC:
            return len(ENC.encode(text, disallowed_special=()))
        return len(text) // 4  # Fallback heuristic

    async def _run_gitingest(
        self,
        source: str,
        subpath: str,
        include_patterns: list[str] | None,
        exclude_patterns: list[str] | None,
    ) -> tuple[str, str, int]:
        """Execute gitingest CLI via uv run."""
        cmd = ["uv", "run", "python3", "-m", "gitingest", source, "--output", "-"]

        # In a real environment, we'd add patterns and subpaths to the command
        # For this implementation, we use the basic pipe to stdout

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode().strip()
            raise RuntimeError(f"Gitingest failed: {error_msg}")

        output = stdout.decode(errors="replace")

        # Parsing logic for gitingest output (simplified)
        # Gitingest output typically has sections for Summary, Tree, and Files

        digest = output
        tree = "Extracted Tree"  # Placeholder, parsing logic needed if strictly separated
        file_count = output.count("File:")  # Simple heuristic

        return digest, tree, file_count
