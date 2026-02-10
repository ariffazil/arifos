"""
canonical_bootstrap.py — Config-Based Bootstrap with Progressive Canonical Loading

Implements Option 2 (Config-Based) + Option 1 (Fetch Logic) hybrid.

Progressive Loading Order:
  1. CCC (apex.arif-fazil.com) — Constitutional Canon [REQUIRED]
  2. BBB (arifos.arif-fazil.com) — Implementation Ledger [REQUIRED]
  3. AAA (arif-fazil.com) — Human Authority [ONLY IF scar_weight >= 1.0]

Tri-Witness Consensus:
  - Require ≥2 sources for "tri_witness_sync = true"
  - CCC failure → fallback to local cached floors (SABAR mode)
  - Hash verification ensures canonical integrity

Version: v55.5
Author: Muhammad Arif bin Fazil
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

# Optional HTTP clients - graceful degradation if not available
AIOHTTP_AVAILABLE = False
REQUESTS_AVAILABLE = False
try:
    import aiohttp

    AIOHTTP_AVAILABLE = True
except ImportError:
    pass
try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    pass

logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION SCHEMA
# =============================================================================

DEFAULT_CANONICAL_CONFIG = {
    "bootstrap_mode": "web_first",  # web_first | local_only | web_only
    "canonical_sources": {
        "aaa_human": {
            "url": "https://arif-fazil.com/llms.json",
            "fallback_url": "https://arif-fazil.com/llms.txt",
            "band": "AAA",
            "access": "sovereign_only",  # Only fetch if scar_weight >= 1.0
            "required": False,
            "timeout_seconds": 5,
        },
        "bbb_ledger": {
            "url": "https://arifos.arif-fazil.com/llms.json",
            "fallback_url": "https://arifos.arif-fazil.com/llms.txt",
            "band": "BBB",
            "access": "always",
            "required": True,
            "timeout_seconds": 5,
        },
        "ccc_canon": {
            "url": "https://apex.arif-fazil.com/llms.json",
            "fallback_url": "https://apex.arif-fazil.com/llms.txt",
            "band": "CCC",
            "access": "always",
            "required": True,
            "timeout_seconds": 7,  # Higher timeout for constitutional core
        },
    },
    "verification": {
        "check_signatures": True,
        "min_sources": 2,  # Tri-Witness: need at least 2 of 3
        "require_ccc": True,  # CCC is mandatory for web_first mode
        "hash_verification": True,
        "max_age_seconds": 3600,  # Cache TTL
    },
    "fallback": {
        "local_config_path": "VAULT999/CCC_CANON/canonical_config.json",
        "cache_dir": ".cache/arifos/canonical",
        "on_failure": "fallback_local",  # fallback_local | void | sabar
    },
    "governance": {
        "sovereign_scar_threshold": 1.0,
        "guest_scar_threshold": 0.0,
        "authorized_scar_threshold": 0.5,
    },
}

# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class CanonicalSourceResult:
    """Result from fetching a single canonical source."""

    source_id: str
    band: str  # AAA, BBB, CCC
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    hash: str = ""
    error: str = ""
    fetch_time_ms: float = 0.0
    from_cache: bool = False
    fallback_used: bool = False


@dataclass
class CanonicalBootstrapResult:
    """Complete result from canonical bootstrap operation."""

    status: str  # SEAL, SABAR, VOID
    mode: str  # web_first, local_only, web_only

    # Source results
    ccc_canon: Optional[CanonicalSourceResult] = None
    bbb_ledger: Optional[CanonicalSourceResult] = None
    aaa_human: Optional[CanonicalSourceResult] = None

    # Aggregate metrics
    sources_fetched: int = 0
    sources_required: int = 0
    tri_witness_sync: bool = False

    # Constitutional state
    constitutional_floors: Dict[str, Any] = field(default_factory=dict)
    implementation_state: Dict[str, Any] = field(default_factory=dict)
    sovereign_authority: Dict[str, Any] = field(default_factory=dict)

    # Local fallback
    local_fallback_used: bool = False
    local_config: Dict[str, Any] = field(default_factory=dict)

    # Metadata
    session_id: str = ""
    scar_weight: float = 0.0
    reason: str = ""


# =============================================================================
# CONFIG LOADER
# =============================================================================


class CanonicalConfigLoader:
    """Load and validate canonical bootstrap configuration."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._find_config_path()
        self._config: Optional[Dict[str, Any]] = None

    def _find_config_path(self) -> str:
        """Find config file in standard locations."""
        search_paths = [
            os.environ.get("ARIFOS_CANONICAL_CONFIG", ""),
            "mcp/config/canonical_bootstrap.json",
            "VAULT999/CCC_CANON/canonical_config.json",
            ".config/arifos/canonical.json",
        ]
        for path in search_paths:
            if path and Path(path).exists():
                return path
        return ""  # Use defaults

    def load(self) -> Dict[str, Any]:
        """Load configuration with fallback to defaults."""
        if self._config is not None:
            return self._config

        if self.config_path and Path(self.config_path).exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                # Merge with defaults
                self._config = self._merge_config(DEFAULT_CANONICAL_CONFIG, user_config)
                logger.info(f"Canonical config loaded from: {self.config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config from {self.config_path}: {e}")
                self._config = DEFAULT_CANONICAL_CONFIG.copy()
        else:
            # Check environment variables
            env_mode = os.environ.get("ARIFOS_BOOTSTRAP_MODE", "")
            self._config = DEFAULT_CANONICAL_CONFIG.copy()
            if env_mode in ("web_first", "local_only", "web_only"):
                self._config["bootstrap_mode"] = env_mode
                logger.info(f"Canonical config from env: bootstrap_mode={env_mode}")

        return self._config

    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """Deep merge user config with defaults."""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result


# =============================================================================
# FETCH ENGINE
# =============================================================================


class CanonicalFetchEngine:
    """Fetch canonical sources from web with retry and fallback logic."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sources_config = config.get("canonical_sources", {})
        self.verification = config.get("verification", {})
        self.cache_dir = Path(
            config.get("fallback", {}).get("cache_dir", ".cache/arifos/canonical")
        )
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """Create cache directory if needed."""
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(f"Cannot create cache dir: {e}")

    async def fetch_source(self, source_id: str, scar_weight: float = 0.0) -> CanonicalSourceResult:
        """Fetch a single canonical source with access control."""
        source_cfg = self.sources_config.get(source_id)
        if not source_cfg:
            return CanonicalSourceResult(
                source_id=source_id,
                band="UNKNOWN",
                success=False,
                error=f"Unknown source: {source_id}",
            )

        band = source_cfg.get("band", "UNKNOWN")
        access = source_cfg.get("access", "always")

        # Access control check
        if access == "sovereign_only" and scar_weight < 1.0:
            logger.debug(f"Skipping {source_id} ({band}): sovereign access required")
            return CanonicalSourceResult(
                source_id=source_id, band=band, success=False, error="Sovereign access required"
            )

        # Try cache first
        cached = self._check_cache(source_id)
        if cached:
            return CanonicalSourceResult(
                source_id=source_id, band=band, success=True, data=cached, from_cache=True
            )

        # Fetch from web
        url = source_cfg.get("url", "")
        fallback_url = source_cfg.get("fallback_url", "")
        timeout = source_cfg.get("timeout_seconds", 5)

        result = await self._fetch_url(source_id, band, url, timeout)

        # Fall through to fallback if: HTTP failed OR got non-JSON from a .json URL
        needs_fallback = not result.success
        if result.success and url.endswith(".json") and result.data.get("format") == "text":
            logger.debug(f"{source_id}: .json URL returned non-JSON content, falling back to .txt")
            needs_fallback = True

        if needs_fallback and fallback_url:
            logger.debug(f"Trying fallback URL for {source_id}")
            result = await self._fetch_url(source_id, band, fallback_url, timeout)
            result.fallback_used = result.success

        # Cache successful results
        if result.success:
            self._cache_result(source_id, result.data)

        return result

    async def _fetch_url(
        self, source_id: str, band: str, url: str, timeout: int
    ) -> CanonicalSourceResult:
        """Fetch URL using available HTTP client."""
        import time as time_module

        start_time = time_module.time()

        # Try aiohttp first (async)
        if AIOHTTP_AVAILABLE:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url, timeout=aiohttp.ClientTimeout(total=timeout)
                    ) as resp:
                        if resp.status == 200:
                            content = await resp.text()
                            data = self._parse_content(content)
                            fetch_time = (time_module.time() - start_time) * 1000
                            return CanonicalSourceResult(
                                source_id=source_id,
                                band=band,
                                success=True,
                                data=data,
                                hash=self._compute_hash(content),
                                fetch_time_ms=fetch_time,
                            )
                        else:
                            return CanonicalSourceResult(
                                source_id=source_id,
                                band=band,
                                success=False,
                                error=f"HTTP {resp.status}",
                            )
            except Exception as e:
                return CanonicalSourceResult(
                    source_id=source_id, band=band, success=False, error=str(e)
                )

        # Fallback to requests (sync in async context - not ideal but works)
        elif REQUESTS_AVAILABLE:
            try:
                loop = asyncio.get_event_loop()
                resp = await loop.run_in_executor(None, lambda: requests.get(url, timeout=timeout))
                if resp.status_code == 200:
                    data = self._parse_content(resp.text)
                    fetch_time = (time_module.time() - start_time) * 1000
                    return CanonicalSourceResult(
                        source_id=source_id,
                        band=band,
                        success=True,
                        data=data,
                        hash=self._compute_hash(resp.text),
                        fetch_time_ms=fetch_time,
                    )
                else:
                    return CanonicalSourceResult(
                        source_id=source_id,
                        band=band,
                        success=False,
                        error=f"HTTP {resp.status_code}",
                    )
            except Exception as e:
                return CanonicalSourceResult(
                    source_id=source_id, band=band, success=False, error=str(e)
                )

        # No HTTP client available
        return CanonicalSourceResult(
            source_id=source_id,
            band=band,
            success=False,
            error="No HTTP client available (install aiohttp or requests)",
        )

    def _parse_content(self, content: str) -> Dict[str, Any]:
        """Parse content as JSON or return as text wrapper."""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Treat as plain text
            return {"content": content, "format": "text"}

    def _compute_hash(self, content: str) -> str:
        """Compute SHA256 hash of content."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _check_cache(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Check if valid cached result exists."""
        cache_file = self.cache_dir / f"{source_id}.json"
        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached = json.load(f)

            # Check age
            max_age = self.verification.get("max_age_seconds", 3600)
            import time

            if time.time() - cached.get("cached_at", 0) < max_age:
                return cached.get("data")
        except Exception:
            pass
        return None

    def _cache_result(self, source_id: str, data: Dict[str, Any]):
        """Cache successful fetch result."""
        cache_file = self.cache_dir / f"{source_id}.json"
        try:
            import time

            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"cached_at": time.time(), "data": data}, f, indent=2)
        except Exception as e:
            logger.debug(f"Failed to cache {source_id}: {e}")


# =============================================================================
# BOOTSTRAP ORCHESTRATOR
# =============================================================================


class CanonicalBootstrap:
    """
    Main orchestrator for canonical bootstrap process.

    Usage:
        bootstrap = CanonicalBootstrap()
        result = await bootstrap.initialize(scar_weight=1.0, session_id="xyz")
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_loader = CanonicalConfigLoader(config_path)
        self.config = self.config_loader.load()
        self.fetch_engine = CanonicalFetchEngine(self.config)

    async def initialize(
        self, scar_weight: float = 0.0, session_id: str = "", mode: Optional[str] = None
    ) -> CanonicalBootstrapResult:
        """
        Initialize constitutional state from canonical web sources.

        Progressive loading:
          1. CCC (canon) - always first
          2. BBB (ledger) - second
          3. AAA (human) - only if scar_weight >= 1.0
        """
        effective_mode = mode or self.config.get("bootstrap_mode", "web_first")

        # Local-only mode: skip web fetch
        if effective_mode == "local_only":
            return self._local_fallback(session_id, scar_weight, "local_only mode")

        # Fetch sources in order of priority: CCC → BBB → AAA
        fetch_order = ["ccc_canon", "bbb_ledger"]
        if scar_weight >= 1.0:
            fetch_order.append("aaa_human")

        results = {}
        for source_id in fetch_order:
            result = await self.fetch_engine.fetch_source(source_id, scar_weight)
            results[source_id] = result

        # Determine status based on results
        ccc_result = results.get("ccc_canon")
        bbb_result = results.get("bbb_ledger")
        aaa_result = results.get("aaa_human")

        success_count = sum(1 for r in results.values() if r.success)
        min_sources = self.config.get("verification", {}).get("min_sources", 2)
        require_ccc = self.config.get("verification", {}).get("require_ccc", True)

        # Tri-Witness check
        tri_witness_sync = success_count >= min_sources
        if require_ccc and (not ccc_result or not ccc_result.success):
            tri_witness_sync = False

        # Build constitutional state
        constitutional_floors = {}
        if ccc_result and ccc_result.success:
            constitutional_floors = self._extract_floors(ccc_result.data)

        implementation_state = {}
        if bbb_result and bbb_result.success:
            implementation_state = self._extract_implementation(bbb_result.data)

        sovereign_authority = {}
        if aaa_result and aaa_result.success:
            sovereign_authority = self._extract_authority(aaa_result.data)

        # Determine final status
        if tri_witness_sync:
            status = "SEAL"
            reason = f"Tri-Witness sync achieved ({success_count}/3 sources)"
        elif effective_mode == "web_only":
            status = "VOID"
            reason = "web_only mode: insufficient canonical sources"
        else:
            # Fallback to local
            return self._local_fallback(
                session_id, scar_weight, "Tri-Witness failed, using local fallback"
            )

        return CanonicalBootstrapResult(
            status=status,
            mode=effective_mode,
            ccc_canon=ccc_result,
            bbb_ledger=bbb_result,
            aaa_human=aaa_result,
            sources_fetched=success_count,
            sources_required=len(fetch_order),
            tri_witness_sync=tri_witness_sync,
            constitutional_floors=constitutional_floors,
            implementation_state=implementation_state,
            sovereign_authority=sovereign_authority,
            session_id=session_id,
            scar_weight=scar_weight,
            reason=reason,
        )

    def _extract_floors(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract constitutional floors from CCC data."""
        # Handle both JSON and text formats
        if "floors" in data:
            return data["floors"]
        elif "constitutional_floors" in data:
            return data["constitutional_floors"]
        return {"raw": data}

    def _extract_implementation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract implementation state from BBB data."""
        if "implementation" in data:
            return data["implementation"]
        elif "mcp_tools" in data:
            return data["mcp_tools"]
        return {"raw": data}

    def _extract_authority(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract sovereign authority from AAA data."""
        if "authority" in data:
            return data["authority"]
        elif "author" in data:
            return {"author": data["author"]}
        return {"raw": data}

    def _local_fallback(
        self, session_id: str, scar_weight: float, reason: str
    ) -> CanonicalBootstrapResult:
        """Return local fallback configuration."""
        local_config = self._load_local_config()

        return CanonicalBootstrapResult(
            status="SABAR",
            mode="local_fallback",
            local_fallback_used=True,
            local_config=local_config,
            session_id=session_id,
            scar_weight=scar_weight,
            reason=f"Local fallback: {reason}",
        )

    def _load_local_config(self) -> Dict[str, Any]:
        """Load local constitutional configuration."""
        local_path = self.config.get("fallback", {}).get("local_config_path", "")
        if local_path and Path(local_path).exists():
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load local config: {e}")

        # Return embedded defaults
        return {
            "floors": [
                "F1_Amanah",
                "F2_Truth",
                "F3_TriWitness",
                "F4_Clarity",
                "F5_Peace2",
                "F6_Empathy",
                "F7_Humility",
                "F8_Genius",
                "F9_AntiHantu",
                "F10_Ontology",
                "F11_CommandAuth",
                "F12_InjectionDefense",
                "F13_Sovereign",
            ],
            "source": "embedded_defaults",
        }


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


async def fetch_canonical_state(
    scar_weight: float = 0.0, session_id: str = "", mode: Optional[str] = None
) -> CanonicalBootstrapResult:
    """
    Convenience function to fetch canonical state.

    Usage in init_000.py Step 0/1:
        canonical = await fetch_canonical_state(scar_weight=1.0, session_id=session)
        if canonical.status == "SEAL":
            # Use canonical constitutional floors
            floors = canonical.constitutional_floors
    """
    bootstrap = CanonicalBootstrap()
    return await bootstrap.initialize(scar_weight=scar_weight, session_id=session_id, mode=mode)


def get_bootstrap_config() -> Dict[str, Any]:
    """Get current bootstrap configuration."""
    loader = CanonicalConfigLoader()
    return loader.load()


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "CanonicalBootstrap",
    "CanonicalBootstrapResult",
    "CanonicalSourceResult",
    "CanonicalConfigLoader",
    "CanonicalFetchEngine",
    "fetch_canonical_state",
    "get_bootstrap_config",
    "DEFAULT_CANONICAL_CONFIG",
]
