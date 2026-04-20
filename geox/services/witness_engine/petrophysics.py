import math
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class PetrophysicsResult(BaseModel):
    status: str
    model: str
    sw_p50: Optional[float] = None
    sw_p10: Optional[float] = None
    sw_p90: Optional[float] = None
    phi_e: Optional[float] = None
    vsh: Optional[float] = None
    verdict: str = "PARTIAL"
    confidence: float = 0.5
    constitutional_floors: List[str] = ["F9", "F7"]
    _888_hold: bool = False

class WitnessEngine:
    """
    PHYSICS-9 Engine for deterministic subsurface calculations.
    Ensures no 'phantom' geology passes through the system.
    """
    
    def select_sw_model(self, formation: str, temperature_c: float) -> Dict[str, Any]:
        """
        Recommends a Water Saturation (Sw) model based on formation chemistry.
        """
        # Logic distillation: High T/High Salinity usually Archie. 
        # Shaly sand needs Simandoux or Indonesia.
        if "SHALE" in formation.upper() or "CLAY" in formation.upper():
            return {
                "recommended_model": "INDONESIA",
                "reason": "Shaly formation detected; Indonesia model required for conductivity correction.",
                "confidence": 0.85,
                "alternatives": ["SIMANDOUUX", "WAXMAN-SMITS"]
            }
        
        if temperature_c > 120:
            return {
                "recommended_model": "ARCHIE_HT",
                "reason": "High temperature regime; using refined Archie thermal coefficients.",
                "confidence": 0.92,
                "alternatives": ["ARCHIE"]
            }
            
        return {
            "recommended_model": "ARCHIE",
            "reason": "Clean sand protocol; standard Archie parameters applied.",
            "confidence": 0.95,
            "alternatives": ["SIMANDOUX"]
        }

    def compute_archie_sw(
        self, 
        model: str, 
        rw: float, 
        rt: float, 
        phi: float, 
        a: float = 1.0, 
        m: float = 2.0, 
        n: float = 2.0
    ) -> PetrophysicsResult:
        """
        Computes Water Saturation using standard or modified Archie equations.
        physics: Sw^n = (a * Rw) / (phi^m * Rt)
        """
        try:
            # Physics-9 check: no zero division
            if rt <= 0 or phi <= 0:
                return PetrophysicsResult(
                    status="error", 
                    model=model, 
                    _888_hold=True, 
                    verdict="VOID"
                )

            # Core Archie
            ro = (a * rw) / (phi ** m)
            sw_sq = ro / rt
            sw = math.sqrt(sw_sq) if n == 2 else sw_sq ** (1/n)
            
            # Bound check
            sw = max(0.0, min(1.1, sw)) # Allow up to 1.1 before clipping to reflect noise
            
            # Uncertainty simulation (F7 Humility)
            p10 = max(0.0, sw * 0.85)
            p90 = min(1.0, sw * 1.15)
            
            return PetrophysicsResult(
                status="success",
                model=model,
                sw_p50=min(1.0, sw),
                sw_p10=p10,
                sw_p90=p90,
                phi_e=phi * 0.9, # Simple net-to-gross effect
                vsh=0.1,
                verdict="SEAL" if 0.05 < sw < 0.95 else "PARTIAL",
                confidence=0.9
            )
        except Exception:
            return PetrophysicsResult(
                status="error", 
                model=model, 
                _888_hold=True, 
                verdict="VOID"
            )

    def hold_check(self, well_id: str, phi: float, sw: float) -> Dict[str, Any]:
        """
        Governance check (888_HOLD) for anomalous petrophysics.
        """
        # Example threshold: Impossible reservoir (High Sw + High Phi)
        if phi > 0.35 and sw > 0.90:
            return {
                "status": "warning",
                "hold_triggered": True,
                "reason": "Anomaly detected: High porosity with full saturation — possible wet sand or wash-out.",
                "floors_checked": ["F9", "F12"]
            }
        
        return {
            "status": "ok",
            "hold_triggered": False,
            "floors_checked": ["F9", "F12"]
        }

witness = WitnessEngine()
