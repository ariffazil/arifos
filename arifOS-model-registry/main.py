"""
arifOS Model Registry — FastAPI Service
Phase 1: Repo-backed JSON registry
Phase 2: SQLite/PostgreSQL migration

Tools exposed:
- get_model_profile
- get_model_soul
- get_runtime_profile
- get_role
- init_anchor_v2
- verify_identity_claim
"""

import json
import os
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# =============================================================================
# Registry Path
# =============================================================================
REGISTRY_PATH = Path(__file__).parent.parent
MODELS_PATH = REGISTRY_PATH / "models"
PROFILES_PATH = REGISTRY_PATH / "model_soul_profiles"
ROLES_PATH = REGISTRY_PATH / "roles"
RUNTIME_PATH = REGISTRY_PATH / "runtime_profiles"
CATALOG_PATH = REGISTRY_PATH / "catalog.json"

# =============================================================================
# Pydantic Models
# =============================================================================
class IdentityClaim(BaseModel):
    claimed_identity: str
    claimed_provider: Optional[str] = None

class InitAnchorRequest(BaseModel):
    actor_id: str
    declared_model_key: str
    declared_role: Optional[str] = None
    requested_scope: list[str] = ["read", "query"]

class DriftEvent(BaseModel):
    session_id: str
    event_type: str  # identity_mismatch, tool_claim_invalid, role_drift
    claimed: str
    expected: str
    severity: str = "medium"

# =============================================================================
# FastAPI App
# =============================================================================
app = FastAPI(
    title="arifOS Model Registry",
    description="Model identity + MODEL_SOUL governance registry",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Helper Functions
# =============================================================================
def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)

def load_catalog() -> dict:
    return load_json(CATALOG_PATH)

def load_model(model_key: str) -> dict:
    path = MODELS_PATH / f"{model_key}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Model {model_key} not found")
    return load_json(path)

def load_profile(model_key: str) -> dict:
    # Try arifOS profile first
    path = PROFILES_PATH / f"{model_key}_arifos.json"
    if not path.exists():
        path = PROFILES_PATH / f"{model_key}_default.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Profile for {model_key} not found")
    return load_json(path)

def load_role(role_key: str) -> dict:
    path = ROLES_PATH / f"{role_key}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Role {role_key} not found")
    return load_json(path)

def load_runtime(mode_key: str) -> dict:
    path = RUNTIME_PATH / f"{mode_key}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Runtime mode {mode_key} not found")
    return load_json(path)

# =============================================================================
# Tools (MCP-style)
# =============================================================================

@app.get("/")
def root():
    return {
        "service": "arifOS Model Registry",
        "version": "0.1.0",
        "status": "operational"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/catalog")
def get_catalog():
    """Get the full catalog index"""
    return load_catalog()

@app.get("/model/{model_key}")
def get_model_profile(model_key: str):
    """Get full model profile + capabilities"""
    model = load_model(model_key)
    return {
        "ok": True,
        "tool": "get_model_profile",
        "status": "SUCCESS",
        "result_type": "model_profile",
        "result": model
    }

@app.get("/model/{model_key}/soul")
def get_model_soul(model_key: str):
    """Get MODEL_SOUL governance profile for a model"""
    profile = load_profile(model_key)
    return {
        "ok": True,
        "tool": "get_model_soul",
        "status": "SUCCESS",
        "result_type": "model_soul_profile",
        "result": profile
    }

@app.get("/role/{role_key}")
def get_role(role_key: str):
    """Get role constraints"""
    role = load_role(role_key)
    return {
        "ok": True,
        "tool": "get_role",
        "status": "SUCCESS",
        "result_type": "role",
        "result": role
    }

@app.get("/runtime/{mode_key}")
def get_runtime_profile(mode_key: str):
    """Get runtime deployment profile"""
    runtime = load_runtime(mode_key)
    return {
        "ok": True,
        "tool": "get_runtime_profile",
        "status": "SUCCESS",
        "result_type": "runtime_profile",
        "result": runtime
    }

@app.post("/verify/identity")
def verify_identity_claim(claim: IdentityClaim):
    """Verify declared identity against registry"""
    catalog = load_catalog()
    
    # Find matching model
    matched = None
    for m in catalog.get("models", []):
        if m["model_key"] == claim.claimed_identity:
            matched = m
            break
    
    if matched:
        model = load_model(matched["model_key"])
        return {
            "ok": True,
            "tool": "verify_identity_claim",
            "status": "CONFIRMED",
            "result_type": "identity_verification",
            "result": {
                "verification_status": "confirmed",
                "declared": claim.claimed_identity,
                "verified": matched["model_key"],
                "model": model
            }
        }
    else:
        return {
            "ok": True,
            "tool": "verify_identity_claim",
            "status": "UNCONFIRMED",
            "result_type": "identity_verification",
            "result": {
                "verification_status": "unconfirmed",
                "declared": claim.claimed_identity,
                "verified": None,
                "mismatch_detected": True,
                "drift_risk": "high"
            }
        }

@app.post("/init_anchor_v2")
def init_anchor_v2(req: InitAnchorRequest):
    """Create a MODEL_SOUL-bound session anchor"""
    catalog = load_catalog()
    
    # Load model
    try:
        model = load_model(req.declared_model_key)
    except HTTPException:
        return {
            "ok": False,
            "tool": "init_anchor_v2",
            "status": "FAIL",
            "result_type": "init_anchor_result",
            "errors": [f"Model {req.declared_model_key} not found in registry"]
        }
    
    # Load profile
    try:
        profile = load_profile(req.declared_model_key)
    except HTTPException:
        profile = None
    
    # Load role
    role = None
    if req.declared_role:
        try:
            role = load_role(req.declared_role)
        except HTTPException:
            pass
    
    # Determine verification status
    verification_status = "confirmed"
    mismatch_detected = False
    
    # For now, we assume declared matches verified (Phase 1)
    # Phase 2 will add actual runtime introspection
    
    # Build response
    result = {
        "session_anchor": {
            "session_id": f"sess_{req.actor_id}_{int(__import__('time').time())}",
            "organ_stage": "000_INIT",
            "actor_id": req.actor_id,
            "scope": {"granted": req.requested_scope}
        },
        "identity_anchor": {
            "declared": {
                "model_key": req.declared_model_key,
                "provider": model.get("provider")
            },
            "verified": {
                "model_key": req.declared_model_key,
                "provider": model.get("provider")
            },
            "verification_status": verification_status,
            "mismatch_detected": mismatch_detected
        },
        "model_soul_anchor": {
            "declared": {
                "model_family": model.get("family"),
                "runtime_class": model.get("runtime_class")
            },
            "verified": {
                "model_family": model.get("family"),
                "runtime_class": model.get("runtime_class")
            },
            "verification_status": verification_status,
            "capabilities": model.get("capabilities")
        },
        "role_anchor": None,
        "self_claim_boundary": None,
        "runtime_truth": None
    }
    
    # Add role if provided
    if role:
        result["role_anchor"] = {
            "declared": {"requested_role": req.declared_role},
            "verified": {"bound_role": req.declared_role},
            "verification_status": "bound",
            "role_constraints": role.get("role_constraints")
        }
        result["self_claim_boundary"] = profile.get("self_claim_boundary") if profile else None
    
    # Add runtime if available
    try:
        runtime = load_runtime("vault_backed")
        result["runtime_truth"] = {
            "declared": {"memory_mode": "vault_backed"},
            "verified": {"memory_mode": "vault_backed"},
            "verification_status": "confirmed",
            "tools_live": runtime.get("tools_live"),
            "web_on": runtime.get("web_on"),
            "execution_mode": runtime.get("execution_mode")
        }
    except HTTPException:
        pass
    
    return {
        "ok": True,
        "tool": "init_anchor_v2",
        "status": "SUCCESS",
        "machine_status": "READY",
        "risk_class": "low",
        "result_type": "init_anchor_result@v2",
        "result": result
    }

@app.get("/models")
def list_models():
    """List all registered models"""
    catalog = load_catalog()
    models = []
    for m in catalog.get("models", []):
        models.append({
            "model_key": m["model_key"],
            "provider": m["provider"],
            "family": m["family"],
            "variant": m["variant"],
            "status": m["status"]
        })
    return {
        "ok": True,
        "tool": "list_models",
        "result_type": "model_list",
        "result": {"models": models}
    }

@app.get("/roles")
def list_roles():
    """List all available roles"""
    return {
        "ok": True,
        "tool": "list_roles",
        "result_type": "role_list",
        "result": {
            "roles": ["architect", "engineer", "auditor", "researcher", "judge", "planner"]
        }
    }

# =============================================================================
# Run
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=18792)
