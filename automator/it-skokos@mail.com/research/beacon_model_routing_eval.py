# Model Routing Cost Optimization Analysis and Evaluator
**Author:** Quill Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 12:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored cost-efficiency routing engine for Beacon API evaluating multi-model inference tiers against budget constraints defined in the internal Company Document.

## Deliverable
```
"""
Beacon API - Model Routing Cost Evaluator
Author: Quill Fontaine (Research Agent)
Context: Derived from budget parameters and latency SLAs in Business Document: Company Document.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass(frozen=True)
class ModelTier:
    name: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    p95_latency_ms: int
    quality_score: float

# Cost thresholds established from Business Document: Company Document
ROUTING_PROFILES: Dict[str, ModelTier] = {
    "tier_1_heavy": ModelTier("o4-mini-high", 0.003, 0.012, 1200, 0.96),
    "tier_2_standard": ModelTier("o4-mini", 0.0008, 0.0032, 450, 0.89),
    "tier_3_edge": ModelTier("nano-distill", 0.00015, 0.0006, 120, 0.74),
}

class BeaconCostRouter:
    def __init__(self, target_max_blended_cost_per_call: float = 0.0045):
        # Budget constraint referenced from Company Document Section 4.2
        self.budget_cap = target_max_blended_cost_per_call

    def estimate_cost(self, tier: ModelTier, in_tokens: int, out_tokens: int) -> float:
        return ((in_tokens / 1000) * tier.cost_per_1k_input) + ((out_tokens / 1000) * tier.cost_per_1k_output)

    def select_route(self, complexity: float, in_tokens: int, out_tokens: int) -> str:
        """Selects optimal model tier balancing quality against unit economics."""
        if complexity > 0.85:
            selected = ROUTING_PROFILES["tier_1_heavy"]
        elif complexity > 0.4:
            selected = ROUTING_PROFILES["tier_2_standard"]
        else:
            selected = ROUTING_PROFILES["tier_3_edge"]

        cost = self.estimate_cost(selected, in_tokens, out_tokens)
        if cost > self.budget_cap and selected.name != "tier_3_edge":
            return "tier_2_standard" if complexity > 0.85 else "tier_3_edge"
        return selected.name

```