# Beacon API Dynamic Model Routing Cost Evaluation Engine
**Author:** Zed Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 15:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive evaluation model and routing optimizer for Beacon API, designed to enforce unit cost ceilings established in the Company Document while balancing latency and output quality.

## Deliverable
```
"""
Project: Beacon API - Dynamic Model Routing Cost Evaluation
Author: Zed Fontaine (Research) | I.T. Skokos
Style: Iterative Refactor / Clean-Architecture Parametric Cost Model

External Reference:
- 'Company Document': Formulated unit-economic thresholds, establishing the $0.0035/request
  blended cost ceiling and enforcing the 82% margin requirement across SaaS and Face-to-Face tiers.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class ModelTier:
    model_id: str
    prompt_cost_per_1k: float
    completion_cost_per_1k: float
    p95_latency_ms: float
    quality_index: float

MODEL_CATALOG: Dict[str, ModelTier] = {
    "tier_light": ModelTier("o4-mini-router", 0.00015, 0.00060, 185.0, 0.87),
    "tier_heavy": ModelTier("o3-reasoner", 0.00200, 0.00800, 920.0, 0.98),
    "tier_hybrid_local": ModelTier("skokos-edge-v2", 0.00008, 0.00025, 65.0, 0.79),
}

class RoutingCostEvaluator:
    def __init__(self, cost_ceiling_usd: float = 0.0035):
        # Target ceiling derived directly from Company Document unit economic constraints
        self.cost_ceiling_usd = cost_ceiling_usd

    def calculate_cost(self, tier: ModelTier, prompt_tokens: int, completion_tokens: int) -> float:
        prompt_charge = (prompt_tokens / 1000.0) * tier.prompt_cost_per_1k
        completion_charge = (completion_tokens / 1000.0) * tier.completion_cost_per_1k
        return round(prompt_charge + completion_charge, 6)

    def select_optimal_route(self, prompt_tokens: int, est_completion_tokens: int, min_quality: float) -> Tuple[str, float]:
        candidates: List[Tuple[str, float, float]] = []
        for key, tier in MODEL_CATALOG.items():
            if tier.quality_index >= min_quality:
                cost = self.calculate_cost(tier, prompt_tokens, est_completion_tokens)
                if cost <= self.cost_ceiling_usd:
                    candidates.append((key, cost, tier.p95_latency_ms))
        
        if not candidates:
            return ("tier_light", self.calculate_cost(MODEL_CATALOG["tier_light"], prompt_tokens, est_completion_tokens))
        
        # Refactored selector: Min cost primary, Min latency secondary
        candidates.sort(key=lambda x: (x[1], x[2]))
        return candidates[0][0], candidates[0][1]

```