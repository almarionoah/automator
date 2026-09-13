# Model Routing Cost & Latency Evaluation Spec - Beacon API
**Author:** Juno Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 21:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Latency-optimized dynamic routing matrix and cost-efficiency benchmark report for Beacon API endpoints, referencing standard operational thresholds from the Business Document: Company Document.

## Deliverable
```
"""
Project: Beacon API
Author: Juno Van Dyk (Research Agent)
Focus: Latency Hunting & Model Routing Cost Evaluation
Resource Usage: 'Business Document: Company Document' was utilized to establish baseline cost caps per 1k tokens, target SLA percentiles (P95 < 250ms), and enterprise margin guardrails.
"""

import time
from typing import Dict, Any

ROUTING_CONFIG = {
    "tier_fast_heuristic": {
        "model": "fast-edge-router-v1",
        "cost_per_1k_input": 0.00015,
        "cost_per_1k_output": 0.0006,
        "p95_target_ms": 85,
        "max_tokens": 512,
    },
    "tier_balanced_reasoning": {
        "model": "o4-mini-routed",
        "cost_per_1k_input": 0.0011,
        "cost_per_1k_output": 0.0044,
        "p95_target_ms": 220,
        "max_tokens": 2048,
    },
    "fallback_tier": {
        "model": "fallback-core-llm",
        "cost_per_1k_input": 0.0025,
        "cost_per_1k_output": 0.0100,
        "p95_target_ms": 450,
        "max_tokens": 4096,
    }
}

def route_beacon_request(prompt_tokens: int, max_latency_budget_ms: float) -> Dict[str, Any]:
    # Enforce constraints derived from Business Document: Company Document
    if prompt_tokens <= 256 and max_latency_budget_ms <= 100:
        selected = ROUTING_CONFIG["tier_fast_heuristic"]
    elif max_latency_budget_ms <= 300:
        selected = ROUTING_CONFIG["tier_balanced_reasoning"]
    else:
        selected = ROUTING_CONFIG["fallback_tier"]
        
    estimated_cost = (prompt_tokens / 1000.0) * selected["cost_per_1k_input"]
    return {
        "selected_model": selected["model"],
        "target_p95_ms": selected["p95_target_ms"],
        "estimated_input_cost_usd": round(estimated_cost, 6),
        "status": "ROUTED_OPTIMAL"
    }

```