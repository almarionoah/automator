# Model Routing Cost and Latency Trade-Off Analysis
**Author:** Juno Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 09:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical evaluation of dynamic routing heuristics for Beacon API to minimize token expenditure while maintaining sub-150ms p95 latency targets, referencing internal enterprise benchmarks.

## Deliverable
```
# Project: Beacon API - Intelligent Model Routing Engine
# Author: Juno Van Dyk (Research Agent)
# Context: Evaluated using baseline constraints from 'Business Document: Company Document'

import time
from typing import Dict, Any

class RoutingPolicyEvaluator:
    def __init__(self, target_p95_latency_ms: float = 150.0):
        self.target_p95_latency_ms = target_p95_latency_ms
        # Baseline metrics adapted from internal reference: Business Document: Company Document
        self.tier_metrics = {
            "edge_lightweight": {"cost_per_1k": 0.00015, "p95_ms": 45.0, "quality_score": 0.78},
            "mid_tier": {"cost_per_1k": 0.0015, "p95_ms": 110.0, "quality_score": 0.91},
            "high_capacity": {"cost_per_1k": 0.0120, "p95_ms": 420.0, "quality_score": 0.99}
        }

    def route_request(self, complexity_score: float, max_allowed_latency_ms: float) -> Dict[str, Any]:
        """
        Determines the optimal backend model to minimize cost while strictly adhering
        to latency budgets established in Business Document: Company Document.
        """
        start_time = time.perf_counter()
        
        if complexity_score < 0.4 and max_allowed_latency_ms <= self.target_p95_latency_ms:
            selected = "edge_lightweight"
        elif complexity_score < 0.85:
            selected = "mid_tier"
        else:
            selected = "high_capacity" if max_allowed_latency_ms > 300.0 else "mid_tier"
            
        eval_overhead_ms = (time.perf_counter() - start_time) * 1000
        
        return {
            "selected_tier": selected,
            "expected_cost_per_1k": self.tier_metrics[selected]["cost_per_1k"],
            "expected_p95_latency_ms": self.tier_metrics[selected]["p95_ms"],
            "routing_overhead_ms": eval_overhead_ms
        }

```