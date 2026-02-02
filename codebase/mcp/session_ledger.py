"""
arifOS Session Ledger (v55.x) — Persistent, tamper-evident filesystem backend.

999_vault seals a session and writes an immutable chain:
  - Machine ledger: <VAULT_PATH>/sessions/*.json (hash-chained)
  - Human log:      <VAULT_PATH>/BBB_LEDGER/entries/*.md
  - Audit JSONL:    <VAULT_PATH>/vault.jsonl (append-only, optional)

000_init can inject the previous session by reading the chain head.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import threading
import logging
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from codebase.vault.ledger import VaultLedger

# Cross-platform file locking
if sys.platform == "win32":
    import msvcrt

    def _lock_file(f):
        msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)

    def _unlock_file(f):
        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)

else:
    import fcntl

    def _lock_file(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)

    def _unlock_file(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


logger = logging.getLogger(__name__)

# =============================================================================
# PATHS
# =============================================================================

# Root of arifOS (go up from codebase/mcp/ -> codebase/ -> arifOS/)
ARIFOS_ROOT = Path(__file__).parent.parent.parent
DEFAULT_VAULT_ROOT = Path(os.getenv("VAULT_PATH", ARIFOS_ROOT / "VAULT999")).resolve()
GENESIS_HASH = "0" * 64


def _merkle_root(leaves: List[str]) -> str:
    """Compute Merkle root from a list of hex hashes."""
    if not leaves:
        return hashlib.sha256(b"EMPTY_MERKLE").hexdigest()
    level = list(leaves)
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        next_level: List[str] = []
        for i in range(0, len(level), 2):
            payload = (level[i] + level[i + 1]).encode("utf-8")
            next_level.append(hashlib.sha256(payload).hexdigest())
        level = next_level
    return level[0]


# =============================================================================
# SESSION DATA
# =============================================================================


@dataclass
class SessionEntry:
    """A sealed session entry for the ledger."""

    session_id: str
    timestamp: str
    verdict: str  # SEAL, SABAR, VOID, PARTIAL

    # Trinity Results
    init_result: Dict[str, Any] = field(default_factory=dict)
    genius_result: Dict[str, Any] = field(default_factory=dict)
    act_result: Dict[str, Any] = field(default_factory=dict)
    judge_result: Dict[str, Any] = field(default_factory=dict)

    # Telemetry
    telemetry: Dict[str, Any] = field(default_factory=dict)

    # Cryptographic
    prev_hash: str = GENESIS_HASH
    merkle_root: str = ""
    entry_hash: str = ""
    sequence: int = 0
    seal_id: str = ""
    authority: str = "unknown"

    # Context for next session
    context_summary: str = ""
    key_insights: List[str] = field(default_factory=list)

    def canonical_dict(self) -> Dict[str, Any]:
        """
        Deterministic view used for hashing/merkle.
        Excludes entry_hash/merkle_root to avoid self-reference.
        """
        data = asdict(self)
        data.pop("entry_hash", None)
        data.pop("merkle_root", None)
        return data

    def compute_hash(self) -> str:
        """Compute SHA256 hash of this entry (deterministic)."""
        content = json.dumps(self.canonical_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


# =============================================================================
# SESSION LEDGER
# =============================================================================


class SessionLedger:
    """
    Manages the 999-000 loop session persistence (filesystem backend).

    Thread Safety:
    - Uses threading.Lock for in-process synchronization
    - Uses file-based locking for cross-process safety
    """

    # Class-level lock for thread safety across instances
    _class_lock = threading.Lock()

    def __init__(self, base_path: Optional[Path] = None):
        self.vault_root = Path(base_path) if base_path else DEFAULT_VAULT_ROOT
        self.session_path = self.vault_root / "sessions"
        self.bbb_path = self.vault_root / "BBB_LEDGER" / "entries"
        self.jsonl_path = self.vault_root / "vault.jsonl"
        self.vault_backend = "filesystem"
        self.vault_location = str(self.vault_root)

        self.session_path.mkdir(parents=True, exist_ok=True)
        self.bbb_path.mkdir(parents=True, exist_ok=True)
        self.vault_root.mkdir(parents=True, exist_ok=True)

        self._current_session: Optional[SessionEntry] = None
        self._chain_head: Optional[str] = None
        self._lock = threading.Lock()
        self._lock_file_path = self.session_path / ".ledger.lock"
        self._load_chain_head()

    @contextmanager
    def _acquire_lock(self):
        """
        Acquire both thread lock and file lock for safe concurrent access.
        """
        with self._lock:
            # Ensure lock file exists
            self._lock_file_path.touch(exist_ok=True)

            try:
                with open(self._lock_file_path, "r+") as lock_file:
                    try:
                        _lock_file(lock_file)
                        yield
                    finally:
                        try:
                            _unlock_file(lock_file)
                        except Exception:
                            pass  # Ignore unlock errors
            except Exception as e:
                logger.warning(f"File lock failed, proceeding with thread lock only: {e}")
                yield

    def _load_chain_head(self):
        """Load the latest entry hash from chain."""
        chain_file = self.session_path / "chain_head.txt"
        if chain_file.exists():
            self._chain_head = chain_file.read_text().strip()

    def _save_chain_head(self, hash: str):
        """Save the latest entry hash."""
        chain_file = self.session_path / "chain_head.txt"
        chain_file.write_text(hash)
        self._chain_head = hash

    # ---------------------------------------------------------------------
    # Helpers for ordered chain traversal
    # ---------------------------------------------------------------------

    def _load_entry_file(self, path: Path) -> Optional[SessionEntry]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return SessionEntry(**data)
        except Exception as e:
            logger.warning(f"Failed to read ledger entry {path}: {e}")
            return None

    def _entries_map(self) -> Dict[str, SessionEntry]:
        entries: Dict[str, SessionEntry] = {}
        for f in self.session_path.glob("*.json"):
            entry = self._load_entry_file(f)
            if entry and entry.entry_hash:
                entries[entry.entry_hash] = entry
        return entries

    def _walk_chain(self) -> List[SessionEntry]:
        """
        Return entries ordered by the hash chain (GENESIS -> head).
        If chain head is missing, fall back to best-effort ordering by timestamp.
        """
        entries = self._entries_map()
        if not entries:
            return []

        # Prefer chain head traversal
        head = self._chain_head
        if head and head in entries:
            ordered: List[SessionEntry] = []
            current_hash = head
            while current_hash and current_hash in entries:
                entry = entries[current_hash]
                ordered.append(entry)
                prev = entry.prev_hash
                if prev == GENESIS_HASH:
                    break
                current_hash = prev
            return list(reversed(ordered))

        # Fallback: try to find root (prev_hash not referenced) then walk forward
        referenced = {e.prev_hash for e in entries.values()}
        roots = [h for h in entries if h not in referenced]
        if roots:
            # pick most recent root
            root = roots[0]
            ordered = []
            cursor = root
            while cursor in entries:
                entry = entries[cursor]
                ordered.append(entry)
                cursor = entry.prev_hash
            return ordered

        # Last resort: sort by timestamp
        return sorted(entries.values(), key=lambda e: e.timestamp)

    def _next_sequence(self) -> int:
        entries = self._entries_map()
        if not entries:
            return 1
        return max((e.sequence or 0) for e in entries.values()) + 1

    def _write_json(self, entry: SessionEntry):
        filename = f"{entry.entry_hash[:16]}.json"
        filepath = self.session_path / filename
        filepath.write_text(json.dumps(asdict(entry), indent=2))

    def _write_markdown(self, entry: SessionEntry):
        filename = f"{entry.timestamp[:10]}_{entry.session_id[:8]}_{entry.sequence:04d}.md"
        filepath = self.bbb_path / filename

        md_content = f"""# Session Seal: {entry.session_id[:8]}

**Timestamp:** {entry.timestamp}
**Verdict:** {entry.verdict}
**Authority:** {entry.authority}
**Entry Hash:** `{entry.entry_hash}`
**Previous:** `{entry.prev_hash}`
**Merkle Root:** `{entry.merkle_root}`
**Sequence:** {entry.sequence}

---

## Summary

{entry.context_summary}

## Key Insights

{chr(10).join(f"- {i}" for i in entry.key_insights) if entry.key_insights else "- No key insights recorded"}

---

## Telemetry

```yaml
verdict: {entry.verdict}
p_truth: {entry.telemetry.get('p_truth', 'N/A')}
TW: {entry.telemetry.get('TW', 'N/A')}
dS: {entry.telemetry.get('dS', 'N/A')}
peace2: {entry.telemetry.get('peace2', 'N/A')}
kappa_r: {entry.telemetry.get('kappa_r', 'N/A')}
omega_0: {entry.telemetry.get('omega_0', 'N/A')}
```

---

**DITEMPA BUKAN DIBERI**
"""
        filepath.write_text(md_content)

    def _append_jsonl(self, entry: SessionEntry):
        """
        Mirror entry to vault.jsonl for MCP resource readers.
        """
        vault = VaultLedger(str(self.vault_root))
        vault.append_entry(
            {
                "session_id": entry.session_id,
                "seal_id": entry.seal_id,
                "timestamp": entry.timestamp,
                "verdict": entry.verdict,
                "authority": entry.authority,
                "entry_hash": entry.entry_hash,
                "prev_hash": entry.prev_hash,
                "merkle_root": entry.merkle_root,
                "sequence": entry.sequence,
            }
        )

    def seal_session(
        self,
        session_id: str,
        verdict: str,
        init_result: Dict[str, Any],
        genius_result: Dict[str, Any],
        act_result: Dict[str, Any],
        judge_result: Dict[str, Any],
        telemetry: Dict[str, Any],
        context_summary: str = "",
        key_insights: List[str] = None,
        authority: str = "unknown",
        seal_id: Optional[str] = None,
    ) -> SessionEntry:
        """
        Seal a session and write to ledger (append-only, hash-chained).
        """
        key_insights = key_insights or []

        with self._acquire_lock():
            existing_chain = self._walk_chain()
            existing_hashes = [e.entry_hash for e in existing_chain]

            seq = self._next_sequence()
            prev_hash = existing_hashes[-1] if existing_hashes else GENESIS_HASH
            timestamp = datetime.now(timezone.utc).isoformat() + "Z"
            seal_identifier = seal_id or str(uuid.uuid4())

            entry = SessionEntry(
                session_id=session_id,
                timestamp=timestamp,
                verdict=verdict,
                init_result=init_result,
                genius_result=genius_result,
                act_result=act_result,
                judge_result=judge_result,
                telemetry=telemetry,
                prev_hash=prev_hash,
                sequence=seq,
                seal_id=seal_identifier,
                authority=authority or "unknown",
                context_summary=context_summary or self._generate_summary(judge_result),
                key_insights=key_insights,
            )

            entry.entry_hash = entry.compute_hash()
            ledger_hashes = existing_hashes + [entry.entry_hash]
            entry.merkle_root = _merkle_root(ledger_hashes)

            self._write_json(entry)
            self._write_markdown(entry)
            self._append_jsonl(entry)
            self._save_chain_head(entry.entry_hash)

            return entry

    def verify_chain(self) -> Tuple[bool, str]:
        """
        Verify the entire chain:
        1) prev_hash links
        2) entry_hash recomputation
        3) merkle_root recomputation
        Returns (ok, merkle_root_or_reason)
        """
        entries = self._walk_chain()
        if not entries:
            return True, _merkle_root([])

        hashes: List[str] = []
        prev = GENESIS_HASH
        for idx, entry in enumerate(entries, start=1):
            recomputed_hash = entry.compute_hash()
            if recomputed_hash != entry.entry_hash:
                return False, f"hash-mismatch at sequence {idx}"
            if entry.prev_hash != prev:
                return False, f"prev-hash-mismatch at sequence {idx}"
            hashes.append(entry.entry_hash)
            expected_root = _merkle_root(hashes)
            if entry.merkle_root and entry.merkle_root != expected_root:
                return False, f"merkle-mismatch at sequence {idx}"
            prev = entry.entry_hash

        # Chain head should equal last entry
        if self._chain_head and self._chain_head != entries[-1].entry_hash:
            return False, "chain-head-mismatch"

        return True, _merkle_root(hashes)

    # ---------------------------------------------------------------------
    # Context helpers
    # ---------------------------------------------------------------------

    def get_last_session(self) -> Optional[SessionEntry]:
        """Get the last sealed session for 000_init to inject."""
        chain = self._walk_chain()
        return chain[-1] if chain else None

    def get_context_for_init(self) -> Dict[str, Any]:
        """
        Get context to inject into 000_init.
        """
        last = self.get_last_session()

        if not last:
            return {
                "is_first_session": True,
                "previous_session": None,
                "context_summary": "First session - no prior context",
                "key_insights": [],
                "chain_length": 0,
            }

        return {
            "is_first_session": False,
            "previous_session": {
                "session_id": last.session_id,
                "timestamp": last.timestamp,
                "verdict": last.verdict,
                "entry_hash": last.entry_hash,
            },
            "context_summary": last.context_summary,
            "key_insights": last.key_insights,
            "chain_length": len(self._walk_chain()),
        }

    def _generate_summary(self, judge_result: Dict[str, Any]) -> str:
        synthesis = judge_result.get("synthesis", "")
        verdict = judge_result.get("verdict", "UNKNOWN")
        return f"Previous session ended with {verdict}. {synthesis[:200]}"

    def _compute_merkle(self, items: List[Dict]) -> str:
        """Legacy per-entry merkle (kept for compatibility)."""
        if not items:
            return hashlib.sha256(b"EMPTY").hexdigest()

        hashes = [
            hashlib.sha256(json.dumps(item, sort_keys=True).encode()).hexdigest()
            for item in items
        ]

        while len(hashes) > 1:
            if len(hashes) % 2:
                hashes.append(hashes[-1])
            hashes = [
                hashlib.sha256((hashes[i] + hashes[i + 1]).encode()).hexdigest()
                for i in range(0, len(hashes), 2)
            ]

        return hashes[0]


# =============================================================================
# OPEN SESSION TRACKING (Loop Bootstrap)
# =============================================================================

OPEN_SESSIONS_FILE = None  # defined after SESSION_PATH is known


def _open_sessions_file(session_path: Path) -> Path:
    return session_path / "open_sessions.json"


@dataclass
class OpenSession:
    """An in-progress session (not yet sealed)."""

    session_id: str
    token: str
    pid: int
    started_at: str
    authority: str = "GUEST"


def _load_open_sessions(session_path: Path) -> Dict[str, Dict]:
    """Load open sessions from disk."""
    file_path = _open_sessions_file(session_path)
    if not file_path.exists():
        return {}
    try:
        return json.loads(file_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"Failed to load open_sessions.json: {e}")
        return {}


def _save_open_sessions(session_path: Path, sessions: Dict[str, Dict]) -> None:
    """Save open sessions to disk."""
    try:
        _open_sessions_file(session_path).write_text(json.dumps(sessions, indent=2))
    except OSError as e:
        logger.error(f"Failed to save open_sessions.json: {e}")


def open_session(session_id: str, token: str, pid: int, authority: str = "GUEST", base_path: Optional[Path] = None) -> None:
    """
    Record a session as 'in progress' (called by 000_init).
    """
    ledger = SessionLedger(base_path=base_path)
    sessions = _load_open_sessions(ledger.session_path)
    sessions[session_id] = {
        "session_id": session_id,
        "token": token,
        "pid": pid,
        "started_at": datetime.now(timezone.utc).isoformat() + "Z",
        "authority": authority,
    }
    _save_open_sessions(ledger.session_path, sessions)
    logger.info(f"Session opened: {session_id[:8]} (pid={pid})")


def close_session(session_id: str, base_path: Optional[Path] = None) -> bool:
    """
    Mark a session as sealed (called by 999_vault).
    """
    ledger = SessionLedger(base_path=base_path)
    sessions = _load_open_sessions(ledger.session_path)
    if session_id in sessions:
        del sessions[session_id]
        _save_open_sessions(ledger.session_path, sessions)
        logger.info(f"Session closed: {session_id[:8]}")
        return True
    logger.warning(f"Session not found in open_sessions: {session_id[:8]}")
    return False


def get_orphaned_sessions(timeout_minutes: int = 30, base_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Find sessions that started but never sealed (Loop Bootstrap).
    """
    ledger = SessionLedger(base_path=base_path)
    sessions = _load_open_sessions(ledger.session_path)
    orphans = []
    now = datetime.now(timezone.utc)

    for session_id, session_data in sessions.items():
        is_orphaned = False
        reason = ""

        pid = session_data.get("pid", 0)
        if pid and not _pid_exists(pid):
            is_orphaned = True
            reason = f"Process {pid} no longer running"

        if not is_orphaned:
            started_at = session_data.get("started_at", "")
            if started_at:
                try:
                    start_time = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
                    age_minutes = (now - start_time.replace(tzinfo=None)).total_seconds() / 60
                    if age_minutes > timeout_minutes:
                        is_orphaned = True
                        reason = f"Session open for {age_minutes:.1f} minutes (timeout={timeout_minutes})"
                except (ValueError, TypeError):
                    pass

        if is_orphaned:
            orphans.append({**session_data, "orphan_reason": reason})
            logger.warning(f"Orphaned session detected: {session_id[:8]} - {reason}")

    return orphans


def _pid_exists(pid: int) -> bool:
    """Check if a process ID exists (cross-platform)."""
    if sys.platform == "win32":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if handle:
                kernel32.CloseHandle(handle)
                return True
        except Exception:
            return False
        return False
    else:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True


def recover_orphaned_session(session_data: Dict[str, Any], base_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Seal an orphaned session with SABAR verdict to keep the chain consistent.
    """
    session_id = session_data.get("session_id", "UNKNOWN")
    reason = session_data.get("orphan_reason", "Unknown crash")

    telemetry = {
        "verdict": "SABAR",
        "recovery": True,
        "orphan_reason": reason,
        "original_started_at": session_data.get("started_at", ""),
        "recovered_at": datetime.now(timezone.utc).isoformat() + "Z",
    }

    result = seal_memory(
        session_id=session_id,
        verdict="SABAR",
        init_result={"recovered": True, "original_session": session_data},
        genius_result={},
        act_result={},
        judge_result={"synthesis": f"Session recovered after crash: {reason}"},
        telemetry=telemetry,
        context_summary=(
            f"RECOVERED SESSION: {reason}. "
            f"Original session started at {session_data.get('started_at', 'unknown')}."
        ),
        key_insights=[
            "Session was recovered via Loop Bootstrap",
            f"Reason: {reason}",
        ],
        authority="system-recovery",
        base_path=base_path,
    )

    close_session(session_id, base_path=base_path)
    logger.info(f"Orphaned session recovered: {session_id[:8]} -> SABAR")
    return result


# =============================================================================
# SINGLETON
# =============================================================================

_ledger: Optional[SessionLedger] = None


def get_ledger() -> SessionLedger:
    """Get the singleton session ledger."""
    global _ledger
    if _ledger is None:
        _ledger = SessionLedger()
    return _ledger


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def inject_memory() -> Dict[str, Any]:
    """
    Called by 000_init to inject previous session context.
    """
    return get_ledger().get_context_for_init()


def seal_memory(
    session_id: str,
    verdict: str,
    init_result: Dict,
    genius_result: Dict,
    act_result: Dict,
    judge_result: Dict,
    telemetry: Dict,
    context_summary: str = "",
    key_insights: List[str] = None,
    authority: str = "unknown",
    seal_id: Optional[str] = None,
    base_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Called by 999_vault to seal session.
    Returns: Seal result with entry hash and merkle root
    """
    ledger = SessionLedger(base_path=base_path) if base_path else get_ledger()

    entry = ledger.seal_session(
        session_id=session_id,
        verdict=verdict,
        init_result=init_result,
        genius_result=genius_result,
        act_result=act_result,
        judge_result=judge_result,
        telemetry=telemetry,
        context_summary=context_summary,
        key_insights=key_insights,
        authority=authority,
        seal_id=seal_id,
    )

    return {
        "sealed": True,
        "session_id": entry.session_id,
        "seal_id": entry.seal_id,
        "entry_hash": entry.entry_hash,
        "merkle_root": entry.merkle_root,
        "timestamp": entry.timestamp,
        "verdict": entry.verdict,
        "prev_hash": entry.prev_hash,
        "sequence": entry.sequence,
        "vault_backend": "filesystem",
        "vault_location": ledger.vault_location,
    }
