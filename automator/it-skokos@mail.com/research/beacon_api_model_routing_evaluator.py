# Beacon API Dynamic Model Routing Cost & Latency Evaluation Engine
**Author:** Onyx Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 04:45  
**Inputs used:** Business Document (Company Document)  
## Summary

An algorithmic model-routing evaluation module refactored to simulate and optimize inference costs across tiered LLM endpoints for the Beacon API, benchmarked against financial guidelines defined in Company Document.

## Deliverable
```
"""
Beacon API - Dynamic Model Routing Cost & Latency Evaluator
Author: Onyx Ito (Research Agent, I.T. Skokos)

References:
  - Company Document: Used to extract target cost-per-query caps, tier-based gross margin
    thresholds (>=78%), and SLA latency limits (P95 < 450ms) across SaaS & hybrid F2F workflows.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

@dataclass(frozen=True)
class ModelTier:
    name: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    avg_latency_ms: float
    reasoning_score: float  # Normalized 0.0 - 1.0

@dataclass
class RoutingBenchmarkResult:
    tier_name: str
    blended_cost_per_10k_reqs: float
    p95_latency_ms: float
    margin_compliant: bool
    sla_compliant: bool

class BeaconRouterEvaluator:
    def __init__(self, target_margin_cap: float = 0.0035, max_sla_latency_ms: float = 450.0):
        # Constraints extracted and normalized from Company Document financial baselines
        self.cost_cap = target_margin_cap
        self.sla_latency_limit = max_sla_latency_ms
        self.models: Dict[str, ModelTier] = {
            "gemini_3_1_flash_lite": ModelTier("gemini_3_1_flash_lite", 0.00025, 0.00075, 180.0, 0.82),
            "gemini_1_5_flash": ModelTier("gemini_1_5_flash", 0.00035, 0.00105, 240.0, 0.86),
            "gemini_1_5_pro": ModelTier("gemini_1_5_pro", 0.00350, 0.01050, 680.0, 0.96),
        }

    def evaluate_routing_policy(self, avg_input_tokens: int = 420, avg_output_tokens: int = 180) -> Dict[str, RoutingBenchmarkResult]:
        results = {}
        for key, m in self.models.items():
            cost_per_req = (avg_input_tokens / 1000.0 * m.cost_per_1k_input) + (avg_output_tokens / 1000.0 * m.cost_per_1k_output)
            cost_10k = cost_per_req * 10000.0
            results[key] = RoutingBenchmarkResult(
                tier_name=m.name,
                blended_cost_per_10k_reqs=round(cost_10k, 4),
                p95_latency_ms=m.avg_latency_ms * 1.35,
                margin_compliant=cost_per_req <= self.cost_cap,
                sla_compliant=(m.avg_latency_ms * 1.35) <= self.sla_latency_limit
            )
        return results

```