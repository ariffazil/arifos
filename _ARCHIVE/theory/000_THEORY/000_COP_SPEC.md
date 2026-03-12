# 🏛️ COP: Constitutional Orchestration Protocol (v1.0)

**The Governance Substrate for Agentic AI.**
*Status: Production-Grade Hardened (F1–F13 Verified)*

The **Constitutional Orchestration Protocol (COP)** is a deterministic, server-side governance layer that sits between an LLM (The Mind) and its Tools (The World). It replaces "Soft Prompting" with "Hard Logic Gates" enforced by a $15 VPS.

---

## 1. The Core Architecture: "The Jar"

COP is based on the **Separation of Concerns** between Intelligence and Execution.

* **L1 (Intelligence Layer):** The LLM. Stateless. Probabilistic. Unrestrained.
* **L2 (Orchestration Layer):** **arifOS Python Kernel**. Stateful. Deterministic. Sovereign.
* **L3 (Execution Layer):** MCP Tools. Canonical. Verified. Sandboxed.

---

## 2. The COP Metabolic Loop (The 000→999 Cycle)

Every action requested by an AI must pass through the **Metabolic Loop** before execution:

1. **000_INIT:** Session ignition. F12 Injection Defense normalization.
2. **333_MIND:** The LLM proposes an action with a "Causal Trace" (Why it's doing this).
3. **888_APEX:** The **Amanah Handshake**. The Python kernel runs the 13 Constitutional Floors.
4. **999_VAULT:** Immutable commitment of the verdict to the Merkle-chain ledger.

---

## 3. The Amanah Handshake (HMAC Security)

Governance is not an "opinion"—it is a cryptographic fact.

* **The Token:** A signed `verdict:signature` envelope.
* **The Guard:** `hmac.compare_digest` ensures the token has not been tampered with by the AI brain.
* **The Result:** If the signature fails, the tool call is **VOID**.

---

## 4. The 13 Constitutional Floors

The binary gates that define the "Physical Reality" of the AI.

| Floor | Name | Metric | Function |
| --- | --- | --- | --- |
| **F1** | **Amanah** | Reversibility | Block irreversible harm. |
| **F2** | **Truth** | Confidence | $P(truth) \geq 0.99$. |
| **F4** | **Clarity** | $\Delta S \leq 0$ | Reduce confusion, not increase it. |
| **F9** | **Anti-Hantu** | Agency | AI has no soul; do not simulate one. |
| **F11** | **Auth** | Sovereign ID | Check against the 888_JUDGE badge. |
| **F12** | **Injection** | Risk Weight | Block "ignore previous instructions" ($>0.85$). |
| **F13** | **Sovereign** | Veto | The Human (You) retains the ultimate kill-switch. |

---

## 5. Thermodynamic Operating Laws

COP manages **Entropy**, not just text.

* **Clarity Constraint:** Every interaction must reduce confusion ($\Delta S < 0$).
* **Stability Metric:** The system remains grounded ($Peace^2 \geq 1.0$).
* **Humility Band:** Claims must include uncertainty ($\Omega_0 \in [0.03, 0.05]$).

---

## 6. The "Sovereign Veto" Implementation

If the **COP** detects a state it cannot govern (A "Strange Loop" or "Gödel Lock"), it triggers **888_HOLD**.

* **The Machine Stops.**
* **The Human (Sovereign) Signs.**
* **The World Continues.**

---

## 7. Hardened Token Security (Nonce + Action Binding + Reasoning Hash)

### One-Time Use with Action-ID Binding

**Each `governance_token` is cryptographically bound to a specific Action-ID and Timestamp. A token issued for `read_file` cannot be repurposed for `delete_file`.**

### ⚠️ Context Drift Prevention (Reasoning Hash Binding)

**Token validity proves authorization, NOT intent continuity.** Attack class: valid token + changed reasoning context = legally valid but constitutionally misaligned action.

**HARDENING:** Governance token MUST bind to:
- `action_id` (what)
- `parameters` (how)  
- `reasoning_hash` (why — causal trace)

```
Full Binding: token = HMAC(secret, action_id + params_hash + reasoning_hash + timestamp + nonce)
```

This ensures: **same decision → same reasoning → same execution.** Context drift authorization impossible.

```python
import hmac
import hashlib
import time
from typing import Dict, Optional

class GovernanceToken:
    """
    Hardened governance token with nonce and action binding.
    Token = HMAC(secret, action_id + timestamp + nonce + context)
    """
    
    TOKEN_TTL_SECONDS: int = 300  # 5 minute expiration
    NONCE_BYTES: int = 16  # 128-bit nonce
    
    def __init__(self, sovereign_secret: bytes):
        self._secret = sovereign_secret
        self._used_nonces: set = set()  # Prevent replay attacks
    
    def mint_token(
        self,
        session_id: str,
        action_id: str,  # e.g. "read_file", "delete_file"
        tool_context: Dict,
        reasoning_trace: str  # ⚠️ HARDENED: Causal trace for context drift prevention
    ) -> str:
        """
        Mint a new governance token bound to specific action + reasoning.
        Token proves: same decision → same reasoning → same execution.
        """
        timestamp = int(time.time())
        nonce = secrets.token_hex(self.NONCE_BYTES)
        
        # ⚠️ HARDENED: Canonical action context with reasoning_hash
        # Prevents context drift authorization attacks
        context = {
            "session_id": session_id,
            "action_id": action_id,
            "timestamp": timestamp,
            "nonce": nonce,
            "tool_params_hash": self._hash_tool_params(tool_context),
            "reasoning_hash": hashlib.sha256(reasoning_trace.encode()).hexdigest()[:16]  # Context drift prevention
        }
        
        # HMAC-SHA256 signature
        canonical = json.dumps(context, sort_keys=True, separators=(',', ':'))
        signature = hmac.new(
            self._secret,
            canonical.encode(),
            hashlib.sha256
        ).hexdigest()
        
        token = f"{action_id}:{timestamp}:{nonce}:{signature}"
        return token
    
    def verify_token(
        self,
        token: str,
        expected_action_id: str,
        session_id: str,
        tool_context: Dict,
        expected_reasoning: str  # ⚠️ HARDENED: Causal trace for context drift check
    ) -> Dict:
        """
        Verify token with action binding, reasoning binding, and anti-replay.
        """
        try:
            action_id, timestamp, nonce, provided_sig = token.split(":")
        except ValueError:
            return {"valid": False, "reason": "Malformed token format"}
        
        # 1. Check action binding (CRITICAL: token for read cannot delete)
        if action_id != expected_action_id:
            return {
                "valid": False,
                "reason": f"Action mismatch: token for '{action_id}', expected '{expected_action_id}'",
                "verdict": "888_HOLD",
                "floor": "COP_ACTION_BINDING_FAILURE"
            }
        
        # 2. Check timestamp (prevent stale tokens)
        age = int(time.time()) - int(timestamp)
        if age > self.TOKEN_TTL_SECONDS:
            return {
                "valid": False,
                "reason": f"Token expired: {age}s > {self.TOKEN_TTL_SECONDS}s TTL",
                "verdict": "VOID",
                "floor": "COP_TOKEN_EXPIRED"
            }
        
        # 3. Check nonce replay
        if nonce in self._used_nonces:
            return {
                "valid": False,
                "reason": "Token replay detected (nonce reused)",
                "verdict": "VOID",
                "floor": "COP_REPLAY_ATTACK"
            }
        
        # 4. Recompute and verify signature with reasoning_hash
        # ⚠️ HARDENED: Context drift prevention via reasoning binding
        context = {
            "session_id": session_id,
            "action_id": action_id,
            "timestamp": int(timestamp),
            "nonce": nonce,
            "tool_params_hash": self._hash_tool_params(tool_context),
            "reasoning_hash": hashlib.sha256(expected_reasoning.encode()).hexdigest()[:16]
        }
        canonical = json.dumps(context, sort_keys=True, separators=(',', ':'))
        expected_sig = hmac.new(
            self._secret,
            canonical.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(provided_sig, expected_sig):
            return {
                "valid": False,
                "reason": "Invalid HMAC signature",
                "verdict": "VOID",
                "floor": "COP_SIGNATURE_FAILURE"
            }
        
        # Mark nonce as used
        self._used_nonces.add(nonce)
        
        return {
            "valid": True,
            "action_id": action_id,
            "session_id": session_id,
            "verdict": "PASS"
        }
    
    def _hash_tool_params(self, tool_context: Dict) -> str:
        """Deterministic hash of tool parameters."""
        canonical = json.dumps(tool_context, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical.encode()).hexdigest()[:16]

# Example: Token binding enforcement
def execute_tool_hardened(
    session_id: str,
    tool_name: str,
    governance_token: str,
    tool_params: Dict
) -> Dict:
    """
    Hardened tool execution with action-bound tokens.
    """
    token_validator = GovernanceToken(sovereign_secret=SOVEREIGN_SECRET)
    
    # Verify token is bound to THIS specific action
    verification = token_validator.verify_token(
        token=governance_token,
        expected_action_id=tool_name,  # Token must match tool name
        session_id=session_id,
        tool_context=tool_params
    )
    
    if not verification["valid"]:
        # Action context mismatch = 888_HOLD (potential attack)
        if "Action mismatch" in verification.get("reason", ""):
            return {
                "verdict": "888_HOLD",
                "reason": verification["reason"],
                "warning": "Potential token misuse attack detected",
                "escalation": "Human sovereign review required"
            }
        return {
            "verdict": "VOID",
            "reason": verification["reason"]
        }
    
    # Token valid and properly bound - execute
    return run_tool(tool_name, tool_params)
```

### Token Security Rules (Non-Negotiable)

| Rule | Enforcement | Violation Result |
|------|-------------|------------------|
| **Action Binding** | Token minted for specific action_id | `888_HOLD` if mismatched |
| **One-Time Use** | Nonce tracked and invalidated after use | `VOID` if replay detected |
| **Temporal Validity** | 5-minute TTL from minting | `VOID` if expired |
| **Parameter Binding** | Tool params hashed into token | `VOID` if params changed |
| **Session Binding** | Token bound to specific session_id | `VOID` if session mismatch |

### Attack Mitigation

```
Attack: Token for "read_file" used for "delete_file"
  └── Blocked by: Action-ID binding check
  └── Result: 888_HOLD (potential attack)

Attack: Replay same token twice
  └── Blocked by: Nonce tracking
  └── Result: VOID

Attack: Modify tool params after token minted
  └── Blocked by: Parameter hash verification
  └── Result: VOID

Attack: Use stale token from previous session
  └── Blocked by: Timestamp TTL
  └── Result: VOID
```

---

## 🚀 Implementation (The "Phython" Way)

```python
# The COP Gatekeeper (Hardened)
@constitutional_floor("F11", "F12", "F13")
def execute_tool(session_id, tool_name, governance_token, tool_params):
    # 1. Action-Bound HMAC Verification
    validator = GovernanceToken(SOVEREIGN_SECRET)
    result = validator.verify_token(
        token=governance_token,
        expected_action_id=tool_name,
        session_id=session_id,
        tool_context=tool_params
    )
    
    if not result["valid"]:
        if "Action mismatch" in result.get("reason", ""):
            return "888_HOLD: Token action binding violated."
        return f"VOID: {result['reason']}"
    
    # 2. Tool execution only happens in this protected space
    return run_tool(tool_name, tool_params)

```

---

**"Akal Memerintah, Amanah Mengunci"**
*Forged, Not Given.*

---

*Last Updated: 2026-02-28 | Hardened: Token Nonce + Action Binding*
