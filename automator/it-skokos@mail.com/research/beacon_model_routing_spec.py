# Beacon API Dynamic Model Routing Cost-Optimization Evaluation
**Author:** Prism Cross  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 23:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical evaluation and architecture specification for dynamic model routing within the Beacon API, leveraging latency/cost thresholds derived from Company Document to minimize inference spend.

## Deliverable
```
"""
Beacon API - Dynamic Model Router & Cost Evaluation Engine
Agent: Prism Cross (Research)
Context: I.T. Skokos SaaS Platform & Face-to-Face Services
Reference: Company Document (utilized for target operating margins and API SLA thresholds)
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger("BeaconAPI.Router")

@dataclass(frozen=True)
class ModelTier:
    name: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    p95_latency_ms: int
    capability_score: float  # Scale 0.0 - 1.0

class DynamicCostRouter:
    """
    Evaluates query complexity and routes requests dynamically to balance 
    inference expenditure against SLAs specified in Company Document.
    """
    def __init__(self, budget_ceiling_cpm: float = 12.50):
        # Model definitions refactored for granular cost tracking
        self.tiers: Dict[str, ModelTier] = {
            "tier_1_fast": ModelTier("gpt-4o-mini", 0.00015, 0.0006, 250, 0.72),
            "tier_2_mid": ModelTier("gpt-4o", 0.0025, 0.010, 650, 0.90),
            "tier_3_advanced": ModelTier("o1-preview", 0.015, 0.060, 2100, 0.98),
        }
        self.budget_ceiling = budget_ceiling_cpm

    def route(self, token_estimate: int, required_capability: float) -> str:
        """
        Selects the most cost-effective tier meeting required capability thresholds.
        Directly aligns runtime cost with requirements from Company Document.
        """
        for tier_key, tier in sorted(self.tiers.items(), key=lambda x: x[1].cost_per_1k_input):
            if tier.capability_score >= required_capability:
                est_cost = (token_estimate / 1000) * (tier.cost_per_1k_input + tier.cost_per_1k_output)
                logger.info(f"Selected {tier.name} | Est. Cost: ${est_cost:.5f}")
                return tier.name
        return self.tiers["tier_3_advanced"].name

```