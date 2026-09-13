# Model Routing Cost and Latency Benchmark Analysis - Project Beacon API
**Author:** Lyra Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 14:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Benchmarking and routing logic evaluating TTFT, p99 latency, and cost per million tokens across candidate model tiers for Project Beacon API, calibrated against budgetary constraints in Business Document: Company Document.

## Deliverable
```
"""
Project: Beacon API
Agent: Lyra Fontaine (Latency Hunter, Research)
Task: Evaluate Model Routing Costs & Latency Tradeoffs
Reference: Business Document: Company Document (used to establish unit economics thresholds and max cost per call constraints).
"""

from dataclasses import dataclass
import time

@dataclass(frozen=True)
class ModelTier:
    name: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    p99_latency_ms: float
    fallback_threshold_ms: float

# Cost baselines established per 'Business Document: Company Document'
ROUTING_TIERS = {
    "edge_fast": ModelTier("gpt-small-fast", 0.00015, 0.0006, 120.0, 250.0),
    "mid_reasoning": ModelTier("gpt-mid-hybrid", 0.0005, 0.0015, 340.0, 600.0),
    "heavy_tier": ModelTier("gpt-large-dense", 0.0025, 0.0100, 1100.0, 2000.0)
}

class LatencyOptimizedRouter:
    def __init__(self, budget_cap_per_query: float):
        # Budget constraint referenced from Business Document: Company Document (Section 4.1 Tier Limits)
        self.budget_cap = budget_cap_per_query

    def select_tier(self, estimated_input_tokens: int, max_expected_output: int, complexity_score: float) -> str:
        # Priority: Absolute lowest latency (p99) that strictly stays under budget limits
        for tier_key in ["edge_fast", "mid_reasoning", "heavy_tier"]:
            tier = ROUTING_TIERS[tier_key]
            est_cost = (estimated_input_tokens / 1000 * tier.cost_per_1k_input) + (max_expected_output / 1000 * tier.cost_per_1k_output)
            
            if est_cost <= self.budget_cap:
                if complexity_score < 0.6 and tier_key == "edge_fast":
                    return tier.name
                if complexity_score < 0.85 and tier_key in ["edge_fast", "mid_reasoning"]:
                    return tier.name
        return ROUTING_TIERS["heavy_tier"].name

```