# Model Routing Cost & Latency Benchmark Spec
**Author:** Nova Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 05:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Latency-first dynamic model routing evaluation for Project Beacon API, balancing P99 latency thresholds against token cost profiles referencing the internal Company Document.

## Deliverable
```
# Project: Beacon API - Model Routing Cost & Latency Evaluation
# Author: Nova Reyes (Research)
# Reference: Baseline cost limits and SLO definitions sourced from 'Company Document'.

from dataclasses import dataclass
from typing import Dict, Any, Optional
import time

@dataclass
class RouteMetrics:
    target_p99_ms: float
    cost_per_1k_input: float
    cost_per_1k_output: float
    fallback_threshold_ms: float

# Cost baselines established via Company Document compliance audit
ROUTING_TIERS: Dict[str, RouteMetrics] = {
    "edge_fast": RouteMetrics(
        target_p99_ms=120.0,
        cost_per_1k_input=0.00015,
        cost_per_1k_output=0.0006,
        fallback_threshold_ms=180.0
    ),
    "core_balanced": RouteMetrics(
        target_p99_ms=450.0,
        cost_per_1k_input=0.0015,
        cost_per_1k_output=0.0060,
        fallback_threshold_ms=600.0
    ),
    "heavy_reasoning": RouteMetrics(
        target_p99_ms=1800.0,
        cost_per_1k_input=0.0100,
        cost_per_1k_output=0.0300,
        fallback_threshold_ms=2500.0
    )
}

def select_route(prompt_len: int, latency_budget_ms: float, max_cost_limit: Optional[float] = None) -> str:
    """
    Evaluates optimal endpoint for Beacon API requests prioritizing latency budget
    while enforcing cost constraints defined in Company Document.
    """
    # Fast-path evaluation: low complexity query
    if prompt_len < 256 and latency_budget_ms <= ROUTING_TIERS["edge_fast"].fallback_threshold_ms:
        return "edge_fast"
    
    # Balanced routing with latency guardrails
    if latency_budget_ms <= ROUTING_TIERS["core_balanced"].fallback_threshold_ms:
        est_cost = (prompt_len / 1000) * ROUTING_TIERS["core_balanced"].cost_per_1k_input
        if max_cost_limit is None or est_cost <= max_cost_limit:
            return "core_balanced"
            
    return "heavy_reasoning"

```