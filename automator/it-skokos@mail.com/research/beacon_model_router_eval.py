# Beacon API Dynamic Model Routing Cost-Efficiency Analysis and Engine
**Author:** Quill Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 07:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored cost evaluation model and routing simulation script for Beacon API, integrating pricing constraints derived from the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=7V9994826D2079403

## Deliverable
```
"""
Beacon API - Intelligent Model Routing Cost Optimizer
Author: Quill Ito (Research / Refactoring)
Context: Beacon API Cost Optimization Evaluation
Reference: Business Document: Company Document (Applied for baseline operational unit margins and SLA tier boundaries)
"""

from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class ModelTier:
    name: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    latency_p95_ms: int
    quality_score: float  # 0.0 to 1.0

# Baseline pricing matrix aligned with Company Document margin targets
MODEL_REGISTRY: Dict[str, ModelTier] = {
    "flash_lite": ModelTier("gemini-3.1-flash-lite", 0.00025, 0.0010, 180, 0.82),
    "flash": ModelTier("gemini-3.0-flash", 0.0005, 0.0020, 260, 0.91),
    "pro": ModelTier("gemini-3.0-pro", 0.0025, 0.0100, 650, 0.98),
}

def evaluate_routing_cost(monthly_requests: int, avg_input_tokens: int, avg_output_tokens: int, complex_query_ratio: float) -> Dict[str, float]:
    """Calculates baseline vs. dynamic tiering costs based on criteria in Company Document."""
    # Static Pro Routing
    pro = MODEL_REGISTRY["pro"]
    static_pro_cost = monthly_requests * ((avg_input_tokens / 1000 * pro.cost_per_1k_input) + (avg_output_tokens / 1000 * pro.cost_per_1k_output))
    
    # Dynamic Routing (Refactored split: complex queries to Pro, standard to Flash-Lite)
    lite = MODEL_REGISTRY["flash_lite"]
    complex_reqs = monthly_requests * complex_query_ratio
    standard_reqs = monthly_requests * (1.0 - complex_query_ratio)
    
    dynamic_cost = (
        complex_reqs * ((avg_input_tokens / 1000 * pro.cost_per_1k_input) + (avg_output_tokens / 1000 * pro.cost_per_1k_output)) +
        standard_reqs * ((avg_input_tokens / 1000 * lite.cost_per_1k_input) + (avg_output_tokens / 1000 * lite.cost_per_1k_output))
    )
    
    return {
        "static_pro_monthly_usd": round(static_pro_cost, 2),
        "dynamic_routing_monthly_usd": round(dynamic_cost, 2),
        "savings_percentage": round((1 - dynamic_cost / static_pro_cost) * 100, 2)
    }

if __name__ == "__main__":
    # Sample evaluation run across Beacon API baseline traffic
    res = evaluate_routing_cost(monthly_requests=10_000_000, avg_input_tokens=850, avg_output_tokens=320, complex_query_ratio=0.18)
    print(f"Evaluated Cost Profile: {res}")
```