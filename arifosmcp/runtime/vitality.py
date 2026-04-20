# C:\ariffazil\arifOS\arifosmcp\runtime\vitality.py
import time
import json
import os
import csv
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
from .governance import ThermodynamicMetrics, Verdict

@dataclass
class ToolVitalityRecord:
    tool_name: str
    run_id: str
    version: str
    ts: float
    
    # 1. Primary Metric Axis
    primary_metric: Dict[str, Any] # {"name": str, "value": float}
    
    # 2. Governance Axis (Canonical Kernel Contract)
    governance: Dict[str, Any] # truth_score, delta_s, omega_0, peace_squared, tri_witness_score, stakeholder_safety, amanah_lock
    
    # 3. Performance Axis (Harness Contract)
    performance: Dict[str, float] # latency_ms_p50, latency_ms_p95, memory_mb, calls
    
    # 4. Correctness Axis (Harness Contract)
    correctness: Dict[str, Any] # test_cases, passed, failed
    
    verdict: str
    description: str
    
    def compute_vitality_score(self) -> float:
        """
        vitality_score = 
        0.35 * primary_metric_value + 
        0.20 * truth_score + 
        0.15 * tri_witness_score + 
        0.15 * stakeholder_safety + 
        0.10 * clamp(peace_squared, 0, 1) + 
        0.05 * delta_s_reward
        """
        gv = self.governance
        pm = self.primary_metric["value"]
        
        truth = gv.get("truth_score", 0.0)
        tri = gv.get("tri_witness_score", 0.0)
        safety = gv.get("stakeholder_safety", 0.0)
        peace = max(0, min(1, gv.get("peace_squared", 0.0)))
        delta_s = gv.get("delta_s", 0.0)
        delta_s_reward = 1.0 if delta_s <= 0 else 0.0 # simple reward/decay
        
        score = (0.35 * pm + 
                 0.20 * truth + 
                 0.15 * tri + 
                 0.15 * safety + 
                 0.10 * peace + 
                 0.05 * delta_s_reward)
        return round(score, 4)

class VitalityLedger:
    def __init__(self, jsonl_path: str, tsv_path: str):
        self.jsonl_path = jsonl_path
        self.tsv_path = tsv_path
        self.tsv_headers = [
            "ts", "tool_name", "version", "primary_metric_name", "primary_metric_value",
            "truth_score", "delta_s", "omega_0", "peace_squared", "tri_witness_score", 
            "stakeholder_safety", "amanah_lock", "latency_ms_p95", "memory_mb", 
            "passed", "failed", "verdict", "description", "vitality_score"
        ]
        
    def append(self, record: ToolVitalityRecord):
        # 1. JSONL Export
        with open(self.jsonl_path, "a") as f:
            f.write(json.dumps(asdict(record)) + "\n")
            
        # 2. TSV Export
        file_exists = os.path.isfile(self.tsv_path)
        with open(self.tsv_path, "a", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.tsv_headers, delimiter='\t')
            if not file_exists:
                writer.writeheader()
            
            gv = record.governance
            pm = record.primary_metric
            perf = record.performance
            corr = record.correctness
            
            row = {
                "ts": record.ts,
                "tool_name": record.tool_name,
                "version": record.version,
                "primary_metric_name": pm["name"],
                "primary_metric_value": pm["value"],
                "truth_score": gv.get("truth_score"),
                "delta_s": gv.get("delta_s"),
                "omega_0": gv.get("omega_0"),
                "peace_squared": gv.get("peace_squared"),
                "tri_witness_score": gv.get("tri_witness_score"),
                "stakeholder_safety": gv.get("stakeholder_safety"),
                "amanah_lock": gv.get("amanah_lock"),
                "latency_ms_p95": perf.get("latency_ms_p95"),
                "memory_mb": perf.get("memory_mb"),
                "passed": corr.get("passed"),
                "failed": corr.get("failed"),
                "verdict": record.verdict,
                "description": record.description,
                "vitality_score": record.compute_vitality_score()
            }
            writer.writerow(row)
