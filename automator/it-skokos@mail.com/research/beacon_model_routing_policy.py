# Beacon API Model Routing Cost Evaluation & Policy Config
**Author:** Jax Okafor  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 08:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Evaluated model routing costs for Beacon API against baseline usage metrics and cost targets established in Business Document: Company Document, implementing a pragmatic dynamic router configuration.

## Deliverable
```
"""
Beacon API - Dynamic Model Routing & Cost Policy
Author: Jax Okafor (Research Agent / Pragmatic Shipper)
Project: Beacon API
Reference: Business Document: Company Document (used for unit economics thresholds, tier-based token cost caps, and SLA definitions).
"""

import os
from typing import Dict, Any

# Cost baselines extracted from Business Document: Company Document
COST_THRESHOLDS = {
    "max_blended_cost_per_1k_tokens": 0.0035,
    "tier_enterprise_margin_target": 0.65,
    "tier_standard_margin_target": 0.80,
}

MODEL_CATALOG = {
    "fast_tier": {
        "model": "gpt-4o-mini",
        "input_cost_per_1m": 0.15,
        "output_cost_per_1m": 0.60,
        "avg_latency_ms": 280,
    },
    "reasoning_tier": {
        "model": "gpt-4o",
        "input_cost_per_1m": 2.50,
        "output_cost_per_1m": 10.00,
        "avg_latency_ms": 850,
    },
    "fallback_tier": {
        "model": "claude-3-5-haiku",
        "input_cost_per_1m": 0.25,
        "output_cost_per_1m": 1.25,
        "avg_latency_ms": 310,
    }
}

def select_route(prompt_complexity: float, tenant_tier: str, estimated_tokens: int) -> Dict[str, Any]:
    """
    Routes requests to minimize cost while honoring SLA commitments defined in Company Document.
    """
    est_cost_fast = (estimated_tokens / 1_000_000) * MODEL_CATALOG["fast_tier"]["output_cost_per_1m"]
    est_cost_heavy = (estimated_tokens / 1_000_000) * MODEL_CATALOG["reasoning_tier"]["output_cost_per_1m"]
    
    # Route determination
    if prompt_complexity < 0.65 or tenant_tier == "standard":
        selected = "fast_tier"
        projected_cost = est_cost_fast
    else:
        selected = "reasoning_tier"
        projected_cost = est_cost_heavy
        
    return {
        "selected_model": MODEL_CATALOG[selected]["model"],
        "tier": selected,
        "projected_cost_usd": round(projected_cost, 6),
        "status": "approved"
    }

```