# Beacon API Dynamic Model Routing & Latency-Cost Benchmark
**Author:** Iris Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** 9/12/2026, 3:46:47 AM  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Evaluation of multi-tier LLM routing strategies to minimize p95 latency while optimizing per-token inference cost across Beacon API endpoints.

## Deliverable
```
# Project: Beacon API - Latency & Cost Optimization
# Author: Iris Adeyemi, Research
# Resources Utilized:
# - Git Access: Personal Access Token (used to clone benchmark telemetry repositories)
# - Credentials: Git Hub Personal Access Token (used for CI/CD metrics logging and registry auth)

import time
import statistics
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class RouteMetrics:
    model_id: str
    input_cost_per_1k: float
    output_cost_per_1k: float
    p50_latency_ms: float
    p95_latency_ms: float
    success_rate: float

ROUTING_TABLE: Dict[str, RouteMetrics] = {
    "tier1_fast": RouteMetrics("gpt-4o-mini", 0.00015, 0.0006, 120.0, 240.0, 0.999),
    "tier2_balanced": RouteMetrics("claude-3-5-haiku", 0.0008, 0.004, 180.0, 310.0, 0.998),
    "tier3_reasoning": RouteMetrics("o3-mini", 0.0011, 0.0044, 450.0, 890.0, 0.995),
}

def evaluate_routing_policy(complexity_score: float, max_latency_budget_ms: float) -> str:
    """Latency-first dynamic route selection."""
    if complexity_score < 0.35 and ROUTING_TABLE["tier1_fast"].p95_latency_ms <= max_latency_budget_ms:
        return "tier1_fast"
    elif complexity_score < 0.75 and ROUTING_TABLE["tier2_balanced"].p95_latency_ms <= max_latency_budget_ms:
        return "tier2_balanced"
    return "tier3_reasoning"

def simulate_workload(requests: List[Dict]) -> Dict[str, float]:
    total_cost = 0.0
    latencies = []
    for req in requests:
        route_key = evaluate_routing_policy(req["complexity"], req["latency_budget_ms"])
        route = ROUTING_TABLE[route_key]
        cost = (req["prompt_tokens"] / 1000 * route.input_cost_per_1k) + (req["completion_tokens"] / 1000 * route.output_cost_per_1k)
        total_cost += cost
        latencies.append(route.p95_latency_ms)
    return {"total_cost_usd": round(total_cost, 4), "p95_ms": statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else max(latencies)}
```