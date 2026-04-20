import sys
import os
from datetime import datetime

# Path Hack
sys.path.append(os.path.abspath("."))

from services.evidence_store.store import store
from geox.shared.contracts.schemas import EvidenceObject, EvidenceRef, GeoContext, UnitRef, VerticalDomain, EvidenceKind

def seed():
    # 1. Define Common Units
    m = UnitRef(name="meter", symbol="m", quantity="length")
    
    # 2. Define Context
    ctx = GeoContext(
        crsName="WGS 84 / UTM zone 48N",
        crsEpsg=32648,
        verticalDomain=VerticalDomain.tvdss_m,
        isTimeDomain=False,
        units={"horizontal": m, "vertical": m}
    )
    
    # 3. Create Well Evidence
    # Well W-101 in Malay Basin
    well_payload = {
        "head": {"x": 500000.0, "y": 600000.0, "epsg": 32648},
        "survey": {
            "md": [0, 500, 1000, 1500, 2000],
            "inc": [0, 2, 5, 8, 12],
            "azi": [0, 45, 90, 135, 180]
        }
    }
    
    well_obj = EvidenceObject(
        ref=EvidenceRef(
            id="W-101",
            kind=EvidenceKind.well,
            sourceUri="opendtect://Well/W-101",
            timestamp=datetime.utcnow()
        ),
        context=ctx,
        payload=well_payload
    )
    
    store.save_evidence(well_obj)
    print(f"Seeded Well: {well_obj.ref.id}")

    # 4. Create Prospect Evidence
    prospect_payload = {
        "boundary": [
            [498000, 598000], 
            [502000, 598000], 
            [502000, 602000], 
            [498000, 602000], 
            [498000, 598000]
        ]
    }
    
    prospect_obj = EvidenceObject(
        ref=EvidenceRef(
            id="PROSPECT_ALPHA",
            kind=EvidenceKind.map,
            sourceUri="geox://prospects/alpha",
            timestamp=datetime.utcnow()
        ),
        context=ctx,
        payload=prospect_payload
    )
    
    store.save_evidence(prospect_obj)
    print(f"Seeded Prospect: {prospect_obj.ref.id}")

if __name__ == "__main__":
    seed()
