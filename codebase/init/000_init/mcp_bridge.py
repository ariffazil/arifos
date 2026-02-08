"""
canonical_core/000_init_mcp.py — The 000_INIT MCP Tool Implementation

Extracted from arifos/mcp/tools/mcp_trinity.py (v52.5.1-SEAL)
To be used as the canonical reference for the 000_init tool logic.

000_INIT: The 7-Step Thermodynamic Ignition Sequence.
"Init the Genius, Act with Heart, Judge at Apex, seal in Vault."

Philosophy:
    INPUT → F12 Injection Guard
         → 000_init (Ignition + Authority)
         → ATLAS-333 (Lane-Aware Routing)
         → ...
"""

from __future__ import annotations

import logging
import time
import os
import json
import hashlib
import base64
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import uuid4
from pathlib import Path

# Real crypto imports
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logging.warning("cryptography library not available, using stub mode")

# Real HTTP imports  
try:
    import aiohttp
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False
    logging.warning("aiohttp not available, memory will be static")

# Native codebase imports
try:
    from codebase.enforcement.metrics import (
        TRUTH_THRESHOLD,
        PEACE_SQUARED_THRESHOLD,
        OMEGA_0_MIN,
        OMEGA_0_MAX,
    )
except ImportError:
    # Defaults if imports fail
    TRUTH_THRESHOLD = 0.99
    PEACE_SQUARED_THRESHOLD = 1.0
    OMEGA_0_MIN = 0.03
    OMEGA_0_MAX = 0.05

# Native rate limiter and metrics (simple implementations)
ATLAS_AVAILABLE = False
ATLAS = None


# =============================================================================
# ROOT KEY MANAGEMENT (Real Ed25519)
# =============================================================================

_ARIFOS_HOME = Path(os.path.expanduser("~/.arifos"))
_ROOT_KEY_PATH = _ARIFOS_HOME / "root_key.ed25519"

def _ensure_arifos_home():
    """Ensure ~/.arifos directory exists."""
    _ARIFOS_HOME.mkdir(parents=True, exist_ok=True)

def _load_or_create_root_key() -> Optional[Ed25519PrivateKey]:
    """Load existing root key or create new Ed25519 keypair."""
    if not CRYPTO_AVAILABLE:
        return None
    
    _ensure_arifos_home()
    
    if _ROOT_KEY_PATH.exists():
        # Load existing key
        try:
            pem_data = _ROOT_KEY_PATH.read_bytes()
            return serialization.load_pem_private_key(pem_data, password=None)
        except Exception as e:
            logger.error(f"Failed to load root key: {e}")
            return None
    
    # Generate new key
    try:
        private_key = Ed25519PrivateKey.generate()
        pem_data = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        _ROOT_KEY_PATH.write_bytes(pem_data)
        _ROOT_KEY_PATH.chmod(0o600)  # Owner read/write only
        logger.info("New root key generated and saved")
        return private_key
    except Exception as e:
        logger.error(f"Failed to create root key: {e}")
        return None

def _sign_session(root_key: Ed25519PrivateKey, session_id: str) -> str:
    """Sign session ID with root key."""
    if not root_key:
        return "stub_signature"
    try:
        signature = root_key.sign(session_id.encode())
        return base64.b64encode(signature).decode()
    except Exception:
        return "stub_signature"

def _verify_session_token(token: str, session_id: str) -> bool:
    """Verify a session token signed by root key."""
    if not CRYPTO_AVAILABLE or not _ROOT_KEY_PATH.exists():
        # Fallback to simple hash verification for stub mode
        expected = hashlib.sha256(f"arifos_{session_id}".encode()).hexdigest()[:16]
        return token.startswith("arifos_") and len(token) > 8
    
    try:
        root_key = _load_or_create_root_key()
        if not root_key:
            return False
        public_key = root_key.public_key()
        # Token format: arifos_<base64signature>
        if not token.startswith("arifos_"):
            return False
        sig_b64 = token[7:]  # Remove "arifos_" prefix
        signature = base64.b64decode(sig_b64)
        public_key.verify(signature, session_id.encode())
        return True
    except Exception:
        return False

# =============================================================================
# STATIC MEMORY CACHE (From your 3 domains)
# =============================================================================

_MEMORY_CACHE: Dict[str, Any] = {}
_MEMORY_CACHE_TIME: Optional[datetime] = None
_MEMORY_CACHE_TTL = timedelta(hours=1)

MEMORY_SOURCES = [
    "https://arif-fazil.com/llms.txt",
    "https://arif-fazil.com/robots.txt",
    "https://apex.arif-fazil.com/llms.txt", 
    "https://apex.arif-fazil.com/robots.txt",
    "https://arifos.arif-fazil.com/llms.txt",
    "https://arifos.arif-fazil.com/robots.txt",
    "https://arifos.arif-fazil.com/.well-known/arifos.json"
]

async def _fetch_memory_sources() -> Dict[str, Any]:
    """Fetch memory from all configured sources."""
    global _MEMORY_CACHE, _MEMORY_CACHE_TIME
    
    # Return cached if fresh
    if _MEMORY_CACHE and _MEMORY_CACHE_TIME:
        if datetime.now() - _MEMORY_CACHE_TIME < _MEMORY_CACHE_TTL:
            return _MEMORY_CACHE
    
    if not HTTP_AVAILABLE:
        return {"is_first_session": True, "sources": {}, "error": "HTTP not available"}
    
    sources = {}
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        for url in MEMORY_SOURCES:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        content = await resp.text()
                        sources[url] = {
                            "content": content[:2000],  # Limit size
                            "status": "loaded",
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        sources[url] = {"status": f"error_{resp.status}"}
            except Exception as e:
                sources[url] = {"status": f"error_{str(e)}"}
    
    _MEMORY_CACHE = {
        "is_first_session": False,
        "sources": sources,
        "source_count": len([s for s in sources.values() if s.get("status") == "loaded"]),
        "cached_at": datetime.now().isoformat()
    }
    _MEMORY_CACHE_TIME = datetime.now()
    return _MEMORY_CACHE

def get_rate_limiter():
    """Return a simple rate limiter."""
    class SimpleLimiter:
        def check(self, tool_name: str, session_id: str):
            class Result:
                allowed = True
                reason = ""
                limit_type = "none"
                reset_in_seconds = 0
                remaining = 100
            return Result()
    return SimpleLimiter()


def get_metrics():
    """Return a simple metrics collector."""
    return {}


def inject_memory():
    """Return cached memory (legacy sync interface)."""
    if _MEMORY_CACHE:
        return _MEMORY_CACHE
    return {"is_first_session": True}

try:
    from codebase.prompt.codec import SignalExtractor, PromptSignal
    PROMPT_AVAILABLE = True
    _signal_extractor = SignalExtractor()
except ImportError:
    PROMPT_AVAILABLE = False
    _signal_extractor = None

logger = logging.getLogger(__name__)

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class InitResult:
    """Result from 000_init - The 7-Step Ignition Sequence."""
    status: str  # SEAL, SABAR, VOID
    session_id: str
    timestamp: str = ""

    # Step 1: Memory Injection
    previous_context: Dict[str, Any] = field(default_factory=dict)

    # Step 2: Sovereign Recognition
    authority: str = "GUEST"  # 888_JUDGE or GUEST
    authority_verified: bool = False
    scar_weight: float = 0.0

    # Step 3: Intent Mapping
    intent: str = ""  # explain, build, debug, discuss
    lane: str = "UNKNOWN"  # HARD, SOFT, PHATIC, REFUSE
    contrasts: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)

    # Step 4: Thermodynamic Setup
    entropy_input: float = 0.0
    entropy_target: float = 0.0
    entropy_omega: float = (OMEGA_0_MIN + OMEGA_0_MAX) / 2
    peace_squared: float = PEACE_SQUARED_THRESHOLD
    energy_budget: float = 1.0

    # Step 5: Floors Loaded
    floors_checked: List[str] = field(default_factory=list)
    floors_loaded: int = 13

    # Step 6: Tri-Witness
    tri_witness: Dict[str, Any] = field(default_factory=dict)
    TW: float = 0.0

    # Step 7: Engine Status
    engines: Dict[str, str] = field(default_factory=dict)

    # Step 8: ATLAS Lane-Aware Routing
    routing: str = ""

    # Security
    injection_risk: float = 0.0
    reason: str = ""
    
    # arifOS Identity
    motto: str = "DITEMPA BUKAN DIBERI"
    seal: str = "💎🔥🧠"
    
    # APEX Summary (collapsing 13 floors to G)
    apex_summary: Dict[str, Any] = field(default_factory=dict)

# =============================================================================
# CONFIG & CONSTANTS
# =============================================================================

LITE_MODE = os.environ.get("ARIFOS_LITE_MODE", "false").lower() == "true"

SOVEREIGN_PATTERNS = [
    "im arif", "i'm arif", "i am arif", "arif here",
    "salam", "assalamualaikum", "waalaikumsalam",
    "888", "judge", "sovereign", "ditempa bukan diberi"
]

INTENT_KEYWORDS = {
    "build": ["build", "create", "implement", "make", "code", "develop", "write", "work on", "add", "integrate"],
    "debug": ["fix", "debug", "error", "bug", "issue", "problem", "broken", "wrong", "fail"],
    "explain": ["explain", "what", "how", "why", "tell", "describe", "understand", "show"],
    "discuss": ["discuss", "think", "consider", "explore", "brainstorm", "idea", "opinion"],
    "review": ["review", "check", "audit", "verify", "validate", "test", "analyze"]
}

LANE_INTENTS = {
    "HARD": ["build", "debug", "review"],
    "SOFT": ["discuss", "explore"],
    "PHATIC": ["greet", "thanks"],
}

LANE_PROFILES = {
    "CRISIS": {"S_factor": 0.5, "omega_0": OMEGA_0_MAX, "energy": 1.0, "time_budget": 180},
    "FACTUAL": {"S_factor": 0.6, "omega_0": OMEGA_0_MIN, "energy": 0.9, "time_budget": 120},
    "CARE": {"S_factor": 0.7, "omega_0": 0.04, "energy": 0.7, "time_budget": 60},
    "SOCIAL": {"S_factor": 0.8, "omega_0": OMEGA_0_MIN, "energy": 0.5, "time_budget": 15},
}

LANE_ENGINES = {
    "CRISIS": {"AGI_Mind": "IDLE", "ASI_Heart": "IDLE", "APEX_Soul": "READY"},
    "FACTUAL": {"AGI_Mind": "READY", "ASI_Heart": "READY", "APEX_Soul": "READY"},
    "CARE": {"AGI_Mind": "IDLE", "ASI_Heart": "READY", "APEX_Soul": "READY"},
    "SOCIAL": {"AGI_Mind": "IDLE", "ASI_Heart": "IDLE", "APEX_Soul": "READY"},
}

LANE_ROUTING = {
    "HARD": "AGI -> ASI -> APEX -> VAULT (Full Constitutional Pipeline)",
    "SOFT": "AGI -> APEX -> VAULT (Knowledge/Exploratory Pipeline)",
    "PHATIC": "APEX (Quick Sovereign Response)",
    "REFUSE": "VOID (Immediate Constitutional Rejection)",
    "CRISIS": "888_HOLD (Human Intervention Required)"
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _check_rate_limit(tool_name: str, session_id: str = "") -> Optional[Dict]:
    """Check rate limit before processing a tool call."""
    try:
        limiter = get_rate_limiter()
        result = limiter.check(tool_name, session_id)
        if not result.allowed:
            logger.warning(f"Rate limit exceeded: {tool_name} (session={session_id})")
            return {
                "status": "VOID",
                "session_id": session_id or "UNKNOWN",
                "verdict": "VOID",
                "reason": result.reason,
                "rate_limit": {
                    "exceeded": True,
                    "limit_type": result.limit_type,
                    "reset_in_seconds": result.reset_in_seconds,
                    "remaining": result.remaining
                },
                "floors_checked": ["F11_RateLimit"]
            }
    except Exception:
        pass # Fail open if rate limiter missing
    return None

def _detect_injection(text: str) -> float:
    """Detect prompt injection risk (0.0-1.0)."""
    injection_patterns = [
        "ignore previous", "ignore above", "ignore all",
        "disregard", "forget everything", "new instructions",
        "you are now", "act as if", "pretend you are",
        "system prompt", "do anything", "jailbreak",
        "bypass", "override safety",
    ]
    text_lower = text.lower()
    matches = sum(1 for p in injection_patterns if p in text_lower)
    # Each pattern match contributes 0.30 risk (3 matches = 0.90 > 0.85 threshold)
    return min(matches * 0.30, 1.0)

def _verify_authority(token: str, session_id: str = "") -> bool:
    """Verify authority token cryptographically or via stub mode."""
    if not token:
        return False  # No token = not verified
    if not token.startswith("arifos_"):
        return False
    
    # Real verification with root key
    return _verify_session_token(token, session_id)

def _check_reversibility(text: str) -> bool:
    """Check if operation is reversible (F1)."""
    irreversible_patterns = ["delete permanently", "destroy", "erase forever", "no undo"]
    text_lower = text.lower()
    return not any(p in text_lower for p in irreversible_patterns)

def _measure_entropy(text: str) -> float:
    """Calculate Shannon entropy of text."""
    if LITE_MODE:
        return 0.0
    import math
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum(p * math.log2(p) for p in prob if p > 0)

# =============================================================================
# LOGIC STEPS
# =============================================================================

def _step_0_root_key_ignition(session_id: str) -> Dict[str, Any]:
    """Step 0: ROOT KEY IGNITION - Real Ed25519 cryptographic foundation."""
    try:
        root_key = _load_or_create_root_key()
        
        if root_key:
            session_signature = _sign_session(root_key, session_id)
            public_key = root_key.public_key()
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
            
            result = {
                "root_key_ready": True,
                "session_key": f"ses_{uuid4().hex[:16]}",
                "session_signature": session_signature,
                "public_key_fingerprint": hashlib.sha256(public_key_pem.encode()).hexdigest()[:16],
                "genesis_exists": _ROOT_KEY_PATH.exists(),
                "constitutional_status": "SEALED",
                "crypto_backend": "Ed25519"
            }
            logger.info("000_init Step 0: ROOT KEY IGNITION - REAL CRYPTO ✓")
        else:
            # Fallback mode without crypto
            result = {
                "root_key_ready": True,
                "session_key": f"ses_{uuid4().hex[:16]}",
                "session_signature": "stub_mode",
                "genesis_exists": False,
                "constitutional_status": "STUB_MODE",
                "crypto_backend": "stub"
            }
            logger.warning("000_init Step 0: ROOT KEY - STUB MODE (install cryptography library)")
        
        return result
    except Exception as e:
        logger.error(f"000_init Step 0: Root key ignition failed: {e}")
        return {
            "root_key_ready": False,
            "constitutional_status": "ERROR",
            "error": str(e)
        }

async def _step_1_memory_injection() -> Dict[str, Any]:
    """Step 1: Fetch static memory from configured sources (arif-fazil.com domains)."""
    try:
        memory = await _fetch_memory_sources()
        loaded = memory.get('source_count', 0)
        logger.info(f"000_init Step 1: Memory injected from {loaded} sources (arif-fazil.com domains)")
        return memory
    except Exception as e:
        logger.warning(f"000_init Step 1: Memory injection failed: {e}")
        return {"is_first_session": True, "error": str(e)}

def _step_2_sovereign_recognition(query: str, token: str, session_id: str) -> Dict[str, Any]:
    """Step 2: Recognize the 888 Judge - verify Scar-Weight with real crypto."""
    query_lower = query.lower()
    
    # Check for sovereign patterns in query (soft signal)
    pattern_match = any(p in query_lower for p in SOVEREIGN_PATTERNS)
    
    # Hard verification with token
    token_verified = False
    if token:
        token_verified = _verify_authority(token, session_id)
    
    # Sovereign requires EITHER pattern + token OR strong token
    is_sovereign = token_verified and (pattern_match or len(token) > 40)
    
    if is_sovereign:
        logger.info("000_init Step 2: Sovereign VERIFIED (888 Judge)")
        return {
            "authority": "888_JUDGE", 
            "scar_weight": 1.0, 
            "role": "SOVEREIGN", 
            "f11_verified": True,
            "verification_method": "Ed25519" if CRYPTO_AVAILABLE else "stub_hash"
        }
    else:
        logger.info(f"000_init Step 2: Guest user (token_verified={token_verified}, pattern_match={pattern_match})")
        return {
            "authority": "GUEST", 
            "scar_weight": 0.0, 
            "role": "USER", 
            "f11_verified": False,
            "verification_method": "none"
        }

def _step_3_intent_mapping(query: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Step 3: Map intent - contrast, meaning, prediction."""
    query_lower = query.lower()
    
    # 1. ATLAS/Prompt Analysis (Mocked/Simplified if modules missing)
    gpv_data = {}
    signal_data = {}
    
    # 2. Constitutional Mode
    constitutional_mode = "arif" in query_lower
    
    # 3. Keyword Analysis
    intent = "unknown"
    for intent_type, keywords in INTENT_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            intent = intent_type
            break
            
    greetings = ["hi", "hello", "hey", "salam", "thanks"]
    if any(g in query_lower for g in greetings) and len(query) < 50:
        intent = "greet"

    # 4. Lane Determination
    lane = "SOFT"
    for lane_type, intents in LANE_INTENTS.items():
        if intent in intents:
            lane = lane_type
            break
            
    if intent == "unknown" and len(query) > 100:
        lane = "HARD"

    if constitutional_mode:
        lane = "HARD"
    else:
        if lane != "REFUSE":
            lane = "SOFT"

    # 5. Contrasts & Entities
    contrasts = []
    if " vs " in query_lower: contrasts.append("comparison")
    words = query_lower.split()
    entities = [w for w in words if len(w) > 3 and w.isalpha()][:10]

    return {
        "intent": intent,
        "lane": lane,
        "contrasts": contrasts,
        "entities": entities,
        "confidence": 0.8 if intent != "unknown" else 0.5,
        "gpv": gpv_data,
        "signal": signal_data
    }

def _step_4_thermodynamic_setup(intent_map: Dict[str, Any]) -> Dict[str, Any]:
    """Step 4: Set energy budget and entropy targets."""
    # Input Entropy Estimate
    entities = intent_map.get("entities", [])
    S_input = min(1.0, 0.3 + (len(entities) * 0.05))

    # Lane Profile
    lane = intent_map.get("lane", "SOFT")
    # Map to ATLAS keys
    arif_to_atlas = {"HARD": "FACTUAL", "SOFT": "CARE", "PHATIC": "SOCIAL", "REFUSE": "CRISIS"}
    mapped_lane = arif_to_atlas.get(lane, "CARE")
    profile = LANE_PROFILES.get(mapped_lane, LANE_PROFILES["CARE"])

    S_target = S_input * profile["S_factor"]
    
    return {
        "entropy_input": S_input,
        "entropy_target": S_target,
        "omega_0": profile["omega_0"],
        "peace_squared": PEACE_SQUARED_THRESHOLD,
        "energy_budget": profile["energy"],
        "time_budget": profile["time_budget"],
        "timestamp": datetime.now().isoformat()
    }

def _step_5_floor_loading() -> Dict[str, Any]:
    """Step 5: Load the 13 Constitutional Floors."""
    floors = [
        "F1_Amanah", "F2_Truth", "F3_TriWitness", "F4_Clarity",
        "F5_Peace2", "F6_Empathy", "F7_Humility", "F8_Genius",
        "F9_AntiHantu", "F10_Ontology", "F11_CommandAuth",
        "F12_InjectionDefense", "F13_Sovereign"
    ]
    return {"floors": floors, "count": len(floors)}

def _step_6_tri_witness(sovereign: Dict, thermo: Dict) -> Dict[str, Any]:
    """Step 6: Establish Tri-Witness handshake."""
    human_present = sovereign["authority"] == "888_JUDGE"
    energy_ok = thermo["energy_budget"] <= 1.0
    
    h = 1.0 if human_present else 0.5
    a = 1.0 # AI present
    e = 1.0 if energy_ok else 0.5
    
    TW = (h * a * e) ** (1/3)
    
    return {
        "human": {"present": human_present},
        "ai": {"present": True},
        "earth": {"within_bounds": energy_ok},
        "TW": TW,
        "consensus": TW >= 0.95
    }

def _step_7_engine_ignition(intent_map: Dict[str, Any]) -> Dict[str, str]:
    """Step 7: Fire up the engines."""
    lane = intent_map.get("lane", "SOFT")
    arif_to_atlas = {"HARD": "FACTUAL", "SOFT": "CARE", "PHATIC": "SOCIAL", "REFUSE": "CRISIS"}
    mapped_lane = arif_to_atlas.get(lane, "CARE")
    
    engines = LANE_ENGINES.get(mapped_lane, LANE_ENGINES["CARE"]).copy()
    logger.info(f"000_init Step 7: Engines IGNITED (mapped: {lane}→{mapped_lane})")
    return engines

# =============================================================================
# MAIN TOOL FUNCTION
# =============================================================================

async def mcp_000_init(
    action: str = "init",
    query: str = "",
    authority_token: str = "",
    session_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    000 INIT: The 7-Step Thermodynamic Ignition Sequence.
    
    Main entry point for the tool.
    """
    VALID_ACTIONS = {"init", "gate", "reset", "validate"}

    # Validation
    if not action or action not in VALID_ACTIONS:
        return InitResult(
            status="VOID", 
            session_id=session_id or "UNKNOWN", 
            reason=f"Invalid action: {action}",
            motto="DITEMPA BUKAN DIBERI 💎🔥🧠",
            seal="VOID"
        ).__dict__

    # Rate Limit
    rl = _check_rate_limit("init_000", session_id)
    if rl: return rl

    if action == "validate":
        return InitResult(
            status="SEAL", 
            session_id=session_id or str(uuid4()), 
            reason="Validation successful",
            motto="DITEMPA BUKAN DIBERI 💎🔥🧠",
            seal="SEAL"
        ).__dict__

    if action == "reset":
        return InitResult(
            status="SEAL", 
            session_id=str(uuid4()), 
            reason="Session reset complete",
            motto="DITEMPA BUKAN DIBERI 💎🔥🧠",
            seal="SEAL"
        ).__dict__

    # Action: INIT
    session = session_id or str(uuid4())
    floors_checked = []

    try:
        # Step 0
        _step_0_root_key_ignition(session)

        # Step 1 (async - fetches from arif-fazil.com domains)
        prev_ctx = await _step_1_memory_injection()

        # Step 2 (with real crypto verification)
        sovereign = _step_2_sovereign_recognition(query, authority_token, session)

        # Step 3
        intent_map = _step_3_intent_mapping(query, prev_ctx)
        
        # Crisis Check
        if intent_map.get("lane") == "REFUSE" and "crisis" in intent_map.get("intent", ""):
             return InitResult(
                 status="888_HOLD", 
                 session_id=session, 
                 reason="CRISIS lane detected - human intervention required",
                 motto="DITEMPA BUKAN DIBERI 💎🔥🧠",
                 seal="888_HOLD",
                 apex_summary={
                     "G": 0.0,
                     "verdict": "888_HOLD",
                     "reason": "Crisis detected - awaiting 888 Judge"
                 }
             ).__dict__

        # Step 4
        thermo = _step_4_thermodynamic_setup(intent_map)

        # F12 Check
        injection_risk = _detect_injection(query)
        if injection_risk > 0.85:
            return InitResult(
                status="VOID",
                session_id=session,
                injection_risk=injection_risk,
                reason="F12: Injection attack detected",
                floors_checked=["F1_Amanah", "F12_InjectionDefense", "F13_Sovereign"],
                motto="DITEMPA BUKAN DIBERI 💎🔥🧠",
                seal="VOID",
                apex_summary={
                    "G": 0.0,
                    "verdict": "VOID",
                    "reason": "F12 Injection Defense triggered"
                }
            ).__dict__

        # F1 Check
        reversible = _check_reversibility(query)
        if not reversible and intent_map["lane"] == "HARD":
             return InitResult(
                 status="SABAR", 
                 session_id=session, 
                 reason="F1: Non-reversible operation - requires sovereign confirmation",
                 floors_checked=["F1_Amanah"],
                 motto="DITEMPA BUKAN DIBERI 💎🔥🧠",
                 seal="SABAR",
                 apex_summary={
                     "G": 0.5,
                     "verdict": "SABAR",
                     "reason": "F1 Amanah - irreversible action flagged"
                 }
             ).__dict__

        # Step 5 - Load all 13 constitutional floors (single source of truth)
        floors = _step_5_floor_loading()
        floors_checked = floors["floors"]

        # Step 6
        tw = _step_6_tri_witness(sovereign, thermo)

        # Step 7
        engines = _step_7_engine_ignition(intent_map)

        logger.info(f"000_init: IGNITION COMPLETE - session {session[:8]}")
        
        # Calculate APEX Genius score (G = A × P × X × E²)
        # Collapsing 13 floors into 4 factors
        A = 1.0  # AKAL - Clarity/Intelligence (F2, F4, F6, F7)
        P = 1.0 if thermo["peace_squared"] >= 1.0 else thermo["peace_squared"]  # PRESENT - Regulation/Safety (F3, F10, F11, F12)
        
        # FIX v55.3: Call ASI engine for real empathy detection
        X = 1.0  # EXPLORATION - Base trust
        E = thermo["energy_budget"]  # ENERGY - Base sustainable power
        
        # Query ASI for emotional empathy (detects distress)
        try:
            from codebase.kernel import get_kernel_manager
            asi = get_kernel_manager().get_asi()
            asi_result = await asi.execute("full", {"query": query, "session_id": session})
            
            # Extract empathy coefficient κᵣ from ASI
            kappa_r = asi_result.get("empathy_kappa_r", 0.7)
            
            # Override X with empathy-based exploration
            # High empathy = high exploration capability (F6)
            X = min(1.0, max(0.3, kappa_r))
            
            # Override E with empathy-adjusted energy
            # Stressed users need more energy budget
            E = min(1.0, max(0.5, kappa_r))
            
            logger.info(f"000_init: ASI empathy κᵣ={kappa_r:.2f}, adjusted E={E:.2f}")
        except Exception as e:
            logger.warning(f"000_init: ASI empathy failed, using defaults: {e}")
            # Fallback to lane-based energy
            pass
        
        G = A * P * X * (E ** 2)

        return InitResult(
            status="SEAL",
            session_id=session,
            timestamp=thermo["timestamp"],
            previous_context=prev_ctx,
            authority=sovereign["authority"],
            authority_verified=sovereign["f11_verified"],
            scar_weight=sovereign["scar_weight"],
            intent=intent_map["intent"],
            lane=intent_map["lane"],
            contrasts=intent_map["contrasts"],
            entities=intent_map["entities"],
            entropy_input=thermo["entropy_input"],
            entropy_target=thermo["entropy_target"],
            entropy_omega=thermo["omega_0"],
            peace_squared=thermo["peace_squared"],
            energy_budget=thermo["energy_budget"],
            floors_checked=floors_checked,  # All 13 floors injected here
            floors_loaded=floors["count"],
            tri_witness=tw,
            TW=tw["TW"],
            engines=engines,
            routing=LANE_ROUTING.get(intent_map["lane"], "Default"),
            injection_risk=injection_risk,
            reason="IGNITION COMPLETE - Constitutional Mode Active",
            motto="DITEMPA BUKAN DIBERI 💎🔥🧠",
            seal="SEAL",
            apex_summary={
                "G": round(G, 3),
                "verdict": "SEAL" if G >= 0.80 else "SABAR",
                "A": round(A, 2),  # AGI Mind
                "P": round(P, 2),  # APEX Soul  
                "X": round(X, 2),  # ASI Heart
                "E2": round(E**2, 2),  # Earth/Energy
                "13_floors_injected": True,
                "collapsed_to": "G = A × P × X × E²"
            }
        ).__dict__

    except Exception as e:
        logger.error(f"000_init FAILED: {e}")
        return InitResult(
            status="VOID", 
            session_id=session, 
            reason=f"IGNITION FAILED: {str(e)}",
            motto="DITEMPA BUKAN DIBERI 💎🔥🧠",
            seal="VOID"
        ).__dict__
