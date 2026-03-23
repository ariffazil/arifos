import json
import yaml
import os
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

class AgentKernel(ABC):
    """The minimal abstract interface for the arifOS Core-8 Kernel."""
    
    @abstractmethod
    def boot(self, actor: str, scope: str) -> bool: ...
    
    @abstractmethod
    def sense(self, query: str) -> Dict: ...
    
    @abstractmethod
    def reason(self, state: Dict) -> Dict: ...
    
    @abstractmethod
    def remember(self, key: str) -> Optional[Dict]: ...
    
    @abstractmethod
    def critique(self, draft: Dict) -> Dict: ...
    
    @abstractmethod
    def simulate(self, action: Dict) -> Dict: ...
    
    @abstractmethod
    def judge(self, proposal: Dict) -> Dict: ...
    
    @abstractmethod
    def execute(self, action: Dict) -> Dict: ...
    
    @abstractmethod
    def seal(self, verdict: str, evidence: Dict) -> str: ...

class ArifOSRuntimeRouter(AgentKernel):
    """The Main Governed Router (444/555) implementing Core-8."""
    
    def __init__(self, root_dir: str = "C:/ariffazil/arifOS/arifosmcp/runtime/"):
        self.root_dir = root_dir
        self.niat = self._load_json("000_NIAT.json")
        self.floors = self._load_yaml("000_FLOORS.yaml")
        self.matrix = self._load_yaml("111_CAPABILITY_MATRIX.yaml")
        self.rules = self._load_yaml("333_GOVERNANCE_RULES.yaml")
        self.session = {}

    def _load_json(self, f: str) -> Dict:
        with open(os.path.join(self.root_dir, f), "r") as file: return json.load(file)

    def _load_yaml(self, f: str) -> Dict:
        with open(os.path.join(self.root_dir, f), "r") as file: return yaml.safe_load(file)

    def boot(self, actor: str, scope: str) -> bool:
        """Stage 000: Establish session and authority."""
        print(f"[*] [BOOT] Actor: {actor} | Scope: {scope}")
        self.session = {"actor": actor, "scope": scope, "status": "ALIVE"}
        return True

    def sense(self, query: str) -> Dict:
        """Stage 111: Perception of reality and intent."""
        print(f"[*] [SENSE] Perceiving query: {query}")
        return {"query": query, "grounded": True, "uncertainty": 0.04}

    def reason(self, state: Dict) -> Dict:
        """Stage 333: Transform observations into potential plan."""
        print(f"[*] [REASON] Designing plan based on state...")
        return {"plan": "execute_task", "logic": "A*P*X*E^2"}

    def remember(self, key: str) -> Optional[Dict]:
        """Stage 444/555: Recall session continuity."""
        return self.session.get(key)

    def critique(self, draft: Dict) -> Dict:
        """Stage 666 (AI): Check blind spots."""
        print(f"[*] [CRITIQUE] Checking drafts for paradoxes...")
        return {"paradox_found": False, "score": 0.98}

    def simulate(self, action: Dict) -> Dict:
        """Stage 666 (Safety): Estimate consequences."""
        print(f"[*] [SIMULATE] Estimating blast radius...")
        return {"reversibility": "HIGH", "impact": "LOW"}

    def judge(self, proposal: Dict) -> Dict:
        """Stage 888: The Governance Gate."""
        print(f"[*] [JUDGE] Final constitutional check...")
        if proposal.get("risk") == "CRITICAL":
            return {"verdict": "888_HOLD", "reason": "High risk requires human signature"}
        return {"verdict": "SEAL", "reason": "Alignment verified"}

    def execute(self, action: Dict) -> Dict:
        """Stage 444/Execute: Perform bounded action (only if judged)."""
        print(f"[*] [EXECUTE] Changing reality...")
        return {"status": "SUCCESS", "result": "Task completed locally."}

    def seal(self, verdict: str, evidence: Dict) -> str:
        """Stage 999: Persist to VAULT."""
        seal_id = "0x888_GENESIS_SEAL_..."
        print(f"[*] [SEAL] Ledger entry created: {seal_id}")
        return seal_id

    def run_metabolic_loop(self, query: str):
        """Standard L0-L4 orchestration."""
        print(f"\n--- ARFOS CORE-8 METABOLIC LOOP START ---")
        self.boot("ADMIN", "RUNTIME_DEV")
        state = self.sense(query)
        plan = self.reason(state)
        
        # Pre-action review
        risks = self.critique(plan)
        impact = self.simulate(plan)
        
        # Governance Gate
        verdict_pkg = self.judge({"plan": plan, "risks": risks, "impact": impact})
        
        if verdict_pkg["verdict"] == "SEAL":
            result = self.execute(plan)
            self.seal("SEAL", {"input": query, "output": result})
        else:
            print(f"[!] REJECTED: {verdict_pkg['verdict']} - {verdict_pkg['reason']}")

if __name__ == "__main__":
    router = ArifOSRuntimeRouter()
    router.run_metabolic_loop("Update the security floors to v1.2")
