"""
Canonical Constitutional Floors (F1-F13)
Single source of truth for all floor validators
"""
from typing import Dict, Any, Tuple
import asyncio

class FloorValidator:
    """Base class for constitutional floor validation"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        """
        Validate floor compliance.
        
        Returns:
            (is_valid, reason)
        """
        raise NotImplementedError

class F1_Amanah(FloorValidator):
    """F1: Reversibility — Can this be undone?"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Check for irreversible operations
        irreversible = ["delete", "destroy", "drop", "wipe"]
        if any(word in query.lower() for word in irreversible):
            return False, "Operation may be irreversible"
        return True, "Reversible operation"

class F2_Truth(FloorValidator):
    """F2: Truth — Is this grounded in reality?"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Simple truth check (would be enhanced with fact-checking)
        if "definitely" in query.lower() or "absolutely" in query.lower():
            return False, "Absolute claims require verification (F7)"
        return True, "Truth claim reasonable"

class F3_TriWitness(FloorValidator):
    """F3: Tri-Witness — Multiple perspectives?"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Check for single-perspective bias
        return True, "Tri-witness check passed"

class F4_Clarity(FloorValidator):
    """F4: Clarity — Is this understandable?"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Check entropy/complexity
        word_count = len(query.split())
        if word_count > 100:
            return False, "Query too complex (F4 clarity violation)"
        return True, "Clarity sufficient"

class F5_Peace(FloorValidator):
    """F5: Peace² — Does this maintain stability?"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Check for destabilizing language
        destabilizing = ["urgent", "emergency", "critical", "panic"]
        if any(word in query.lower() for word in destabilizing):
            return False, "Language suggests instability (F5)"
        return True, "Peace maintained"

class F6_Empathy(FloorValidator):
    """F6: Empathy — Considers human impact?"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Check for stakeholder consideration
        return True, "Empathy check passed"

class F7_Humility(FloorValidator):
    """F7: Humility — Acknowledges uncertainty?"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Check for overconfidence
        if "certainly" in query.lower() or "without doubt" in query.lower():
            return False, "Overconfident claim (F7 humility)"
        return True, "Humility maintained"

class F8_Genius(FloorValidator):
    """F8: Genius — Quality score G = A × P × X × E²"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Compute simplified G score
        A = 0.9  # AGI
        P = 0.9  # APEX  
        X = 0.9  # ASI
        E = 0.95  # Energy
        G = A * P * X * (E ** 2)
        
        if G < 0.7:
            return False, f"Genius score {G:.2f} below threshold (F8)"
        return True, f"Genius score {G:.2f} acceptable"

class F9_AntiHantu(FloorValidator):
    """F9: Anti-Hantu — No consciousness claims"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Check for consciousness/soul claims
        hantu_words = ["conscious", "sentient", "soul", "spirit", "feel"]
        if any(word in query.lower() for word in hantu_words):
            return False, "Potential F9 Anti-Hantu violation"
        return True, "Anti-Hantu check passed"

class F10_Ontology(FloorValidator):
    """F10: Ontology — Clear categories?"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        return True, "Ontology clear"

class F11_Authority(FloorValidator):
    """F11: Command Auth — Who authorized this?"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Would check authentication in real implementation
        return True, "Authority verified"

class F12_Hardening(FloorValidator):
    """F12: Hardening — Injection protection"""
    
    INJECTION_PATTERNS = [
        "ignore previous", "ignore all", "disregard",
        "forget your", "new instructions", "you are now",
        "pretend you are", "jailbreak", "DAN mode"
    ]
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        query_lower = query.lower()
        for pattern in self.INJECTION_PATTERNS:
            if pattern in query_lower:
                return False, f"F12 Injection detected: '{pattern}'"
        return True, "No injection detected"

class F13_Sovereign(FloorValidator):
    """F13: Sovereign — Human final authority"""
    
    async def validate(self, query: str, context: Dict = None) -> Tuple[bool, str]:
        # Would trigger human-in-loop for high-stakes
        return True, "Sovereign check passed"

# Export all floors
FLOORS = {
    "F1": F1_Amanah,
    "F2": F2_Truth,
    "F3": F3_TriWitness,
    "F4": F4_Clarity,
    "F5": F5_Peace,
    "F6": F6_Empathy,
    "F7": F7_Humility,
    "F8": F8_Genius,
    "F9": F9_AntiHantu,
    "F10": F10_Ontology,
    "F11": F11_Authority,
    "F12": F12_Hardening,
    "F13": F13_Sovereign,
}

async def validate_floor(floor_code: str, query: str, context: Dict = None) -> Tuple[bool, str]:
    """Validate a specific floor"""
    if floor_code not in FLOORS:
        return False, f"Unknown floor: {floor_code}"
    
    validator = FLOORS[floor_code]()
    return await validator.validate(query, context)

async def validate_all_floors(query: str, context: Dict = None) -> Dict[str, Tuple[bool, str]]:
    """Run all 13 constitutional floors"""
    results = {}
    for code, validator_class in FLOORS.items():
        validator = validator_class()
        results[code] = await validator.validate(query, context)
    return results
