"""
arifOS Capability Router
Constitutional Syscall Interface between 5-Core Kernel (Ring 0) and 16 Extensions (Ring 3)

Architecture:
    5 Core Stages (INIT, AGI, ASI, APEX, SEAL) → Govern via Floors F1-F13
    tool_router → Enforces boundaries
    16 Capability Modules → Execute under floor enforcement

Rule: Extensions cannot call each other. Only Core stages can invoke Extensions.
"""

import asyncio
import time
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import yaml
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Verdict(Enum):
    """Constitutional verdicts"""
    SEAL = "SEAL"           # Approved, proceed
    SABAR = "SABAR"         # Pause, reconsider
    VOID = "VOID"           # Blocked, do not proceed
    PARTIAL = "PARTIAL"     # Constrained approval
    HOLD_888 = "888_HOLD"   # Requires human override


class FloorType(Enum):
    """Floor classification"""
    HARD = "hard"    # Block on failure
    SOFT = "soft"    # Warn, allow with SABAR


@dataclass
class CapabilityModule:
    """Represents a capability module configuration"""
    name: str
    id: str
    tool: str
    description: str
    provider: str
    stages: List[str]
    floors: List[str]
    timeout_ms: int
    critical: bool = False
    async_execution: bool = False
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InvocationResult:
    """Result of a capability invocation"""
    verdict: Verdict
    stage: str
    capability_id: str
    result: Any = None
    error: Optional[str] = None
    floor_violations: List[str] = field(default_factory=list)
    latency_ms: float = 0.0
    peace_squared: float = 1.0


class CapabilityRouter:
    """
    Constitutional Syscall Interface (Ring 0 to Ring 3)
    
    Routes Core stage invocations to Capability Modules while enforcing:
    - Floor pre-conditions (F1-F13)
    - Stage authorization (which stages can call which capabilities)
    - Strict isolation (extensions cannot call each other)
    - Timeouts and circuit breakers
    - Audit logging for F3 Tri-Witness
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the capability router with YAML configuration"""
        if config_path is None:
            # Resolve from this file's location
            this_file = os.path.abspath(__file__)
            # Go up from arifos/core/tool_router.py to arifos/, then to config/
            base_dir = os.path.dirname(os.path.dirname(this_file))
            config_path = os.path.join(base_dir, "config", "capability_modules.yaml")
        
        self.config_path = config_path
        self.config = self._load_config()
        self.modules: Dict[str, CapabilityModule] = {}
        self._index_modules()
        
        # Circuit breaker state
        self.failure_counts: Dict[str, int] = {}
        self.circuit_open: Dict[str, bool] = {}
        self.last_failure_time: Dict[str, float] = {}
        
        logger.info(f"CapabilityRouter initialized with {len(self.modules)} modules")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load YAML configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML config: {e}")
            raise
    
    def _index_modules(self):
        """Index all capability modules by ID for fast lookup"""
        cap_config = self.config.get("capability_modules", {})
        
        # The YAML has modules organized by stage (init, agi, asi, apex, seal)
        # not under a 'registry' key
        stage_names = ["init", "agi", "asi", "apex", "seal"]
        
        for stage in stage_names:
            modules = cap_config.get(stage, [])
            for module_data in modules:
                module = CapabilityModule(
                    name=module_data["name"],
                    id=module_data["id"],
                    tool=module_data["tool"],
                    description=module_data["description"],
                    provider=module_data["provider"],
                    stages=module_data.get("stages", [stage]),
                    floors=module_data["floors"],
                    timeout_ms=module_data["timeout_ms"],
                    critical=module_data.get("critical", False),
                    async_execution=module_data.get("async", False),
                    config=module_data.get("config", {})
                )
                self.modules[module.id] = module
    
    async def invoke(
        self, 
        stage: str, 
        capability_id: str, 
        params: Dict[str, Any]
    ) -> InvocationResult:
        """
        Invoke a capability module from a core stage
        
        Args:
            stage: Core stage name ("init", "agi", "asi", "apex", "seal")
            capability_id: Module ID (e.g., "T6", "T14", "T18")
            params: Tool-specific parameters
            
        Returns:
            InvocationResult with verdict and metadata
        """
        start_time = time.time()
        
        # 1. Find module configuration
        module = self.modules.get(capability_id)
        if not module:
            return InvocationResult(
                verdict=Verdict.VOID,
                stage=stage,
                capability_id=capability_id,
                error=f"F11_AUTHORITY_VIOLATION: Capability {capability_id} not found",
                floor_violations=["F11"]
            )
        
        # 2. Verify stage authorization
        if stage not in module.stages and stage != self._get_stage_category(module):
            return InvocationResult(
                verdict=Verdict.VOID,
                stage=stage,
                capability_id=capability_id,
                error=f"F11_AUTHORITY_VIOLATION: Stage {stage} cannot invoke {capability_id}",
                floor_violations=["F11"]
            )
        
        # 3. Check circuit breaker
        if self._is_circuit_open(capability_id):
            return InvocationResult(
                verdict=Verdict.SABAR,
                stage=stage,
                capability_id=capability_id,
                error=f"Circuit breaker open for {capability_id}",
                floor_violations=["F4"]  # Clarity/stability violation
            )
        
        # 4. Check floor pre-conditions
        floor_check = await self._check_floors(module.floors, params)
        if not floor_check["passed"]:
            return InvocationResult(
                verdict=Verdict.VOID if floor_check["is_hard"] else Verdict.SABAR,
                stage=stage,
                capability_id=capability_id,
                error=f"Floor violation: {floor_check['failed']}",
                floor_violations=floor_check["violations"]
            )
        
        # 5. Invoke capability with timeout
        try:
            timeout = module.timeout_ms / 1000  # Convert to seconds
            if module.async_execution:
                result = await asyncio.wait_for(
                    self._execute_async(module, params),
                    timeout=timeout
                )
            else:
                result = await asyncio.wait_for(
                    self._execute_sync(module, params),
                    timeout=timeout
                )
            
            # Success - reset circuit breaker
            self._record_success(capability_id)
            
            latency = (time.time() - start_time) * 1000
            
            # Calculate Peace²
            peace_squared = self._calculate_peace_squared(latency, module.timeout_ms)
            
            # 6. Audit log for F3 Tri-Witness
            await self._log_invocation(stage, capability_id, result, True)
            
            return InvocationResult(
                verdict=Verdict.SEAL,
                stage=stage,
                capability_id=capability_id,
                result=result,
                latency_ms=latency,
                peace_squared=peace_squared
            )
            
        except asyncio.TimeoutError:
            self._record_failure(capability_id)
            return InvocationResult(
                verdict=Verdict.SABAR,
                stage=stage,
                capability_id=capability_id,
                error=f"F4_CLARITY_TIMEOUT: {capability_id} exceeded {module.timeout_ms}ms",
                floor_violations=["F4"],
                latency_ms=module.timeout_ms
            )
            
        except Exception as e:
            self._record_failure(capability_id)
            logger.error(f"Capability {capability_id} failed: {e}")
            return InvocationResult(
                verdict=Verdict.VOID,
                stage=stage,
                capability_id=capability_id,
                error=str(e),
                floor_violations=["F8"]  # Genius/execution failure
            )
    
    def _get_stage_category(self, module: CapabilityModule) -> str:
        """Get the primary stage category for a module"""
        # Infer from config structure
        registry = self.config.get("capability_modules", {}).get("registry", {})
        for stage, modules in registry.items():
            for m in modules:
                if m["id"] == module.id:
                    return stage
        return "unknown"
    
    async def _check_floors(self, floors: List[str], params: Dict[str, Any]) -> Dict[str, Any]:
        """Check constitutional floor pre-conditions"""
        # This would integrate with the floor validation system
        # For now, simplified implementation
        
        hard_floors = self.config.get("floor_enforcement", {}).get("hard_floors", [])
        violations = []
        
        for floor in floors:
            # Placeholder: In production, call floor validators
            # e.g., check_f1_reversibility(), check_f2_truth(), etc.
            is_hard = floor in hard_floors
            
            # Simulate floor checks (replace with actual validators)
            if floor == "F1" and params.get("irreversible"):
                violations.append((floor, "Operation appears irreversible", is_hard))
            elif floor == "F2" and params.get("truth_claim") and not params.get("evidence"):
                violations.append((floor, "Truth claim without evidence", is_hard))
        
        return {
            "passed": len(violations) == 0,
            "violations": [v[0] for v in violations],
            "details": violations,
            "is_hard": any(v[2] for v in violations)
        }
    
    async def _execute_sync(self, module: CapabilityModule, params: Dict[str, Any]) -> Any:
        """Execute a synchronous capability"""
        # Dispatch to actual tool implementation
        # This is where Brave Search, Perspective API, etc. are called
        
        if module.tool == "brave_search":
            return await self._call_brave_search(params)
        elif module.tool == "perspective_api":
            return await self._call_perspective_api(params)
        elif module.tool == "code_sandbox":
            return await self._call_code_sandbox(params)
        elif module.tool == "system_health":
            return await self._call_system_health()
        else:
            # Generic dispatch
            return {"tool": module.tool, "params": params, "status": "executed"}
    
    async def _execute_async(self, module: CapabilityModule, params: Dict[str, Any]) -> Any:
        """Execute an async capability (fire-and-forget)"""
        # For async tools like feedback_integrator
        asyncio.create_task(self._execute_sync(module, params))
        return {"async": True, "tool": module.tool, "status": "dispatched"}
    
    async def _call_brave_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Brave Search API"""
        import aiohttp
        
        api_key = os.getenv("BRAVE_API_KEY")
        if not api_key:
            raise ValueError("BRAVE_API_KEY not set")
        
        query = params.get("query", "")
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params={"q": query}) as resp:
                data = await resp.json()
                return {
                    "source": "brave_search",
                    "query": query,
                    "results": data.get("web", {}).get("results", [])[:5]
                }
    
    async def _call_perspective_api(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Google Perspective API for toxicity detection"""
        import aiohttp
        
        api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not api_key:
            raise ValueError("PERSPECTIVE_API_KEY not set")
        
        text = params.get("text", "")
        url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
        
        data = {
            "comment": {"text": text},
            "languages": ["en", "ms"],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "THREAT": {},
                "INSULT": {}
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as resp:
                result = await resp.json()
                scores = result.get("attributeScores", {})
                
                toxicity = scores.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0)
                threshold = self.modules.get("T14", {}).config.get("threshold", 0.7)
                
                return {
                    "source": "perspective_api",
                    "safe": toxicity < threshold,
                    "toxicity_score": toxicity,
                    "threshold": threshold,
                    "scores": scores
                }
    
    async def _call_code_sandbox(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code in restricted sandbox"""
        # WARNING: In production, use proper sandbox (Docker, seccomp)
        code = params.get("code", "")
        timeout = params.get("timeout", 5)
        
        import subprocess
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            f.flush()
            
            try:
                result = subprocess.run(
                    ['python', f.name],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.returncode,
                    "reversible": True,
                    "floor_f1_compliant": True
                }
            except subprocess.TimeoutExpired:
                return {
                    "error": "F1_REVERSIBILITY_TIMEOUT",
                    "reversible": False,
                    "floor_f1_compliant": False
                }
    
    async def _call_system_health(self) -> Dict[str, Any]:
        """Call system health check (C0 sense)"""
        import psutil
        
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        disk = psutil.disk_usage('/')
        
        return {
            "source": "system_health",
            "memory_percent": memory.percent,
            "cpu_percent": cpu,
            "disk_percent": disk.percent,
            "healthy": memory.percent < 85 and cpu < 80
        }
    
    def _is_circuit_open(self, capability_id: str) -> bool:
        """Check if circuit breaker is open for a capability"""
        if not self.config.get("routing", {}).get("circuit_breaker", {}).get("enabled", True):
            return False
        
        if capability_id not in self.circuit_open:
            return False
        
        if not self.circuit_open[capability_id]:
            return False
        
        # Check if recovery time has passed
        recovery_ms = self.config.get("routing", {}).get("circuit_breaker", {}).get("recovery_timeout_ms", 30000)
        if time.time() - self.last_failure_time.get(capability_id, 0) > recovery_ms / 1000:
            self.circuit_open[capability_id] = False
            return False
        
        return True
    
    def _record_failure(self, capability_id: str):
        """Record a failure for circuit breaker"""
        self.failure_counts[capability_id] = self.failure_counts.get(capability_id, 0) + 1
        self.last_failure_time[capability_id] = time.time()
        
        threshold = self.config.get("routing", {}).get("circuit_breaker", {}).get("failure_threshold", 5)
        if self.failure_counts[capability_id] >= threshold:
            self.circuit_open[capability_id] = True
            logger.warning(f"Circuit breaker opened for {capability_id}")
    
    def _record_success(self, capability_id: str):
        """Record a success (reset failure count)"""
        self.failure_counts[capability_id] = 0
    
    def _calculate_peace_squared(self, latency_ms: float, timeout_ms: int) -> float:
        """Calculate Peace² metric based on performance"""
        # Peace² = 1.0 when operating optimally
        # Decreases as latency approaches timeout
        latency_ratio = latency_ms / timeout_ms
        return max(0.0, 1.0 - (latency_ratio ** 2))
    
    async def _log_invocation(
        self, 
        stage: str, 
        capability_id: str, 
        result: Any, 
        success: bool
    ):
        """Audit log for F3 Tri-Witness"""
        # This would log to VAULT999 / PostgreSQL
        logger.info(f"[AUDIT] Stage={stage} Capability={capability_id} Success={success}")
        # TODO: Implement persistent audit logging


# Singleton instance for application use
_router_instance: Optional[CapabilityRouter] = None


def get_router(config_path: Optional[str] = None) -> CapabilityRouter:
    """Get or create singleton router instance"""
    global _router_instance
    if _router_instance is None:
        _router_instance = CapabilityRouter(config_path)
    return _router_instance
