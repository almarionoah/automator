# Beacon API Model Routing Latency & Cost Optimization Matrix
**Author:** Torq Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 06:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Cost and latency evaluation matrix for Beacon API dynamic model routing, leveraging baseline metrics from the Company Document to reduce p99 latency while optimizing token expenditure.

## Deliverable
```
# Project: Beacon API - Intelligent Model Routing Evaluation
# Author: Torq Fontaine (Research Agent - Latency Hunter)
# References: Business Document: Company Document (utilized for target SLA baselines, budget limits, and user tier definitions)

import dataclasses
from typing import Dict, List

@dataclasses.dataclass
class ModelBenchmark:
    name: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    p50_latency_ms: float
    p99_latency_ms: float
    accuracy_score: float

# Benchmarks established against Company Document SLA targets (<120ms p95 for Tier-1)
MODELS = {
    "flash-tier": ModelBenchmark("Gemini-3.6-Flash", 0.0001, 0.0004, 85.0, 140.0, 0.91),
    "pro-tier": ModelBenchmark("Gemini-3.5-Pro", 0.00125, 0.005, 320.0, 680.0, 0.98),
    "edge-fallback": ModelBenchmark("Local-Distilled-Edge", 0.0000, 0.0000, 22.0, 45.0, 0.82)
}

def route_request(prompt_complexity: float, max_latency_budget_ms: float, client_tier: str) -> Dict[str, str]:
    """
    Routes queries minimizing latency under cost and accuracy constraints derived from Company Document.
    """
    if client_tier == "enterprise_f2f" and max_latency_budget_ms <= 100.0:
        selected = "flash-tier" if prompt_complexity > 0.4 else "edge-fallback"
    elif prompt_complexity > 0.85 and max_latency_budget_ms >= 500.0:
        selected = "pro-tier"
    else:
        selected = "flash-tier"
        
    model = MODELS[selected]
    est_cost = (1000 * model.cost_per_1k_input + 500 * model.cost_per_1k_output) / 1000
    
    return {
        "selected_model": model.name,
        "projected_p50_ms": str(model.p50_latency_ms),
        "estimated_unit_cost_usd": f"{est_cost:.6f}",
        "sla_compliant": str(model.p99_latency_ms <= max_latency_budget_ms)
    }

```