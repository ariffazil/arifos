import json
import os
from datetime import datetime
from typing import List, Optional, Dict
from uuid import uuid4

# Import from the relative path assuming this is run in a way that geox is in path
# In a real app, you'd have a proper package structure.
try:
    from geox.shared.contracts.schemas import EvidenceRef, EvidenceObject, GeoContext, EvidenceKind
except ImportError:
    # Fallback or Mock for standalone testing
    from pydantic import BaseModel
    class EvidenceRef(BaseModel):
        id: str
        kind: str
        source_ref: str
        timestamp: datetime

    class EvidenceObject(BaseModel):
        ref: EvidenceRef
        payload: Dict
        metadata: Optional[Dict] = None

# ══════════════════════════════════════════════════════════════════════════════
# Evidence Store — The Ledger of Observations
# ══════════════════════════════════════════════════════════════════════════════

class EvidenceStore:
    """
    Manages the persistence and retrieval of subsurface evidence objects.
    Enforces 'DITEMPA BUKAN DIBERI' by requiring valid provenance.
    """

    def __init__(self, base_path: str = "c:/ariffazil/GEOX/data/evidence"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def _get_path(self, evidence_id: str) -> str:
        return os.path.join(self.base_path, f"{evidence_id}.json")

    def save_evidence(self, obj: EvidenceObject) -> str:
        """Persist evidence to the ledger."""
        path = self._get_path(obj.ref.id)
        with open(path, "w") as f:
            f.write(obj.model_dump_json(indent=2))
        return obj.ref.id

    def get_evidence(self, evidence_id: str) -> Optional[EvidenceObject]:
        """Retrieve evidence by its identifier."""
        path = self._get_path(evidence_id)
        if not os.path.exists(path):
            return None
        
        with open(path, "r") as f:
            data = json.load(f)
            return EvidenceObject.model_validate(data)

    def list_evidence(self, kind: Optional[str] = None) -> List[EvidenceRef]:
        """List all evidence in the store, optionally filtered by kind."""
        refs = []
        for filename in os.listdir(self.base_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.base_path, filename), "r") as f:
                    try:
                        data = json.load(f)
                        ref = EvidenceRef.model_validate(data["ref"])
                        if not kind or ref.kind == kind:
                            refs.append(ref)
                    except:
                        continue
        return refs

# Global Access Instance
store = EvidenceStore()
