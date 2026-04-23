"""
conftest.py — arifos.core.governance mock for all test modules.

CONFLICT RESOLUTION:
- test_000_init.py does module-level mock injection that overwrites governed_return
- test_333_mind.py has `from arifos.core.governance import governed_return` at module scope
- Module-scope imports are resolved ONCE at first import; patching sys.modules after
  the import does NOT change existing module-level bindings
- Solution: conftest patches arifos.tools._333_mind.governed_return DIRECTLY in a
  pytest hook that runs BEFORE test collection (beforeimport hook)

FAILS WITHOUT this approach when both files run together:
- test_000_init.py collected first → module-level injection corrupts mock
- _333_mind.py imported after → gets wrong governed_return
"""
import sys
import os
import types

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ── Mock objects ───────────────────────────────────────────────────────────────
class _MockVerdict:
    CLAIM_ONLY = "CLAIM_ONLY"
    PARTIAL = "PARTIAL"
    SABAR = "SABAR"
    VOID = "VOID"
    HOLD_888 = "888_HOLD"
    SEAL = "SEAL"


class _MockThermodynamicMetrics:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class _MockAppendVault999Event:
    _events = []

    def __call__(self, event_type, payload, operator_id, session_id):
        self._events.append({"event_type": event_type})
        return {"zkpc_receipt": "mock-receipt"}


class _MockGovernedReturn:
    """
    Returns report dict with envelope fields merged at top level.
    Satisfies:
    - test_000: report dict keys at top level (status, verdict, etc.)
    - test_333: result["output"] == report dict
    """
    def __call__(self, tool_name, report, metrics, operator_id, session_id):
        base = {
            "status": "ACTIVE",
            "verdict": "CLAIM_ONLY",
            "tool": tool_name,
            "metrics": {},
            "identity": {"operator_id": operator_id, "session_id": session_id},
            "zkpc_receipt": "mock-receipt",
            "invariant_failures": [],
        }
        result = {**base, **report}   # report keys at top level
        result["output"] = report     # envelope["output"] = report
        result["raw_output"] = report
        return result


# ── Build fake module hierarchy (installed at collection time) ─────────────────
_gov_stub = types.ModuleType("arifos.core.governance")
_gov_stub.Verdict = _MockVerdict()
_gov_stub.ThermodynamicMetrics = _MockThermodynamicMetrics
_gov_stub.append_vault999_event = _MockAppendVault999Event()
_gov_stub.governed_return = _MockGovernedReturn()
_gov_stub.PEACE_SQUARED_FLOOR = 0.80
_gov_stub.TRI_WITNESS_PARTIAL = 0.33
_gov_stub.VAULT999_LEDGER_PATH = "/tmp/vault999/test.jsonl"
_gov_stub.SABAR = "SABAR"
_gov_stub.HOLD_888 = "888_HOLD"
_gov_stub.VERDICT_SABAR = "SABAR"
_gov_stub.VERDICT_HOLD_888 = "888_HOLD"
_gov_stub.PARTIAL = "PARTIAL"

_core_stub = types.ModuleType("arifos.core")
setattr(_core_stub, "governance", _gov_stub)

sys.modules["arifos.core.governance"] = _gov_stub
sys.modules["arifos.core"] = _core_stub


# ── Patch _333_mind BEFORE collection (solves module-scope import race) ────────
def pytest_configure(config):
    """
    Runs BEFORE test collection starts. Patches arifos.tools._333_mind.governed_return
    with our envelope mock. This runs BEFORE test_000's module-level injection
    corrupts the mock, ensuring _333_mind always gets the correct binding.
    """
    try:
        import arifos.tools._333_mind as _mind_mod
        _mind_mod.governed_return = _MockGovernedReturn()
    except (ImportError, AttributeError):
        pass


def pytest_sessionstart(session):
    """
    Alternative: patch before FIRST test runs (after all collection).
    This runs after collection but before any test executes.
    """
    try:
        import arifos.tools._333_mind as _mind_mod
        _mind_mod.governed_return = _MockGovernedReturn()
    except (ImportError, AttributeError):
        pass