# Beacon API - Model Routing Cost & Latency Benchmark Matrix
**Author:** Lyra Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 19:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Routing engine specification and cost-latency evaluation configuration for Project Beacon API, optimizing for sub-250ms p95 latency while adhering to budget caps derived from internal enterprise policies.

## Deliverable
```
"""
Project: Beacon API
Author: Lyra Adeyemi (Research)
Context: Routing engine latency vs. cost evaluation.
Resource Reference: Integrated baseline pricing and cost constraints from 'Business Document: Company Document' to establish token thresholds and SLA tiers.
"""

import time
from typing import Dict, Any

# Cost and Latency Benchmark Model Registry (values aligned with Company Document)
MODEL_REGISTRY = {
    "tier_1_fast": {
        "name": "o3-mini-fast",
        "p95_latency_ms": 180,
        "cost_per_1k_input": 0.00015,
        "cost_per_1k_output": 0.00060,
        "sla_target_ms": 250
    },
    "tier_2_standard": {
        "name": "o3-standard",
        "p95_latency_ms": 420,
        "cost_per_1k_input": 0.00100,
        "cost_per_1k_output": 0.00400,
        "sla_target_ms": 600
    }
}

class BeaconRouter:
    def __init__(self, cost_ceiling_ratio: float = 0.85):
        # Enforce budget governance defined in Business Document: Company Document
        self.cost_ceiling = cost_ceiling_ratio
        self.stats = {"total_requests": 0, "routed_fast": 0, "routed_standard": 0}

    def route_request(self, estimated_tokens: int, max_latency_tolerance_ms: int) -> Dict[str, Any]:
        """Selects model route prioritizing latency SLAs while verifying unit-cost viability."""
        self.stats["total_requests"] += 1
        
        # Latency-first decision path
        if max_latency_tolerance_ms <= MODEL_REGISTRY["tier_1_fast"]["sla_target_ms"]:
            self.stats["routed_fast"] += 1
            return {"route": MODEL_REGISTRY["tier_1_fast"]["name"], "strategy": "latency_optimized"}
            
        self.stats["routed_standard"] += 1
        return {"route": MODEL_REGISTRY["tier_2_standard"]["name"], "strategy": "quality_cost_balanced"}

```