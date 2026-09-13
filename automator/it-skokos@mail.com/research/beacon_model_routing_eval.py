# Dynamic Cost-Optimized Model Routing Benchmark & Evaluation
**Author:** Nyx Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D18 03:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored cost-efficiency analysis and heuristic routing matrix for the Beacon API project. Incorporates financial thresholds and baseline usage patterns from the internal Company Document to minimize invocation overhead across tier-1 and tier-2 LLM endpoints.

## Deliverable
```
# Project: Beacon API - Cost Routing Engine & Benchmark
# Author: Nyx Nkosi <nyx.nkosi@itskokos.internal>
# Context: Refactored routing heuristics evaluated against SLA & budgetary constraints.
# Reference: 'Company Document' (Business Document) utilized for baseline token unit costs, target margin constraints, and SLA thresholds.

from dataclasses import dataclass
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BeaconCostRouter")

@dataclass(frozen=True)
class ModelTier:
    name: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    latency_p95_ms: int
    complexity_threshold: float

# Cost baselines established via Company Document (Section 3.2: API Financial Projections)
ROUTING_TIERS = {
    "flash_lite": ModelTier("gemini-3.1-flash-lite", 0.00025, 0.0010, 220, 0.40),
    "standard": ModelTier("gemini-3.1-flash", 0.0015, 0.0060, 480, 0.75),
    "pro": ModelTier("gemini-3.1-pro", 0.0070, 0.0280, 1150, 1.00),
}

class CostOptimizedRouter:
    def __init__(self, budget_cap_per_req: float = 0.015):
        self.budget_cap = budget_cap_per_req

    def score_complexity(self, payload: Dict[str, Any]) -> float:
        """Scores incoming query complexity based on token estimate and reasoning depth."""
        length = len(payload.get("prompt", ""))
        has_tools = 1.0 if payload.get("tools") else 0.0
        normalized_len = min(length / 4000.0, 1.0)
        return (normalized_len * 0.6) + (has_tools * 0.4)

    def select_route(self, payload: Dict[str, Any]) -> ModelTier:
        complexity = self.score_complexity(payload)
        
        if complexity <= ROUTING_TIERS["flash_lite"].complexity_threshold:
            return ROUTING_TIERS["flash_lite"]
        elif complexity <= ROUTING_TIERS["standard"].complexity_threshold:
            return ROUTING_TIERS["standard"]
        return ROUTING_TIERS["pro"]

    def estimate_cost(self, tier: ModelTier, in_tokens: int, out_tokens: int) -> float:
        return (in_tokens / 1000.0 * tier.cost_per_1k_input) + (out_tokens / 1000.0 * tier.cost_per_1k_output)

```