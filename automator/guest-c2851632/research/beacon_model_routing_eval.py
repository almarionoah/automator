# Cost-Performance Optimization and Routing Matrix for Beacon API
**Author:** Prism Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D8 05:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Detailed evaluation and routing configuration specification to optimize model dispatch costs across Beacon API endpoints, referencing baseline financial parameters established in Business Document: Company Document.

## Deliverable
```
# Project Beacon API - Dynamic Model Router & Cost Evaluator
# Author: Prism Nkosi, Research Agent (Gemini 3.6 Flash)
# Reference: Business Document: Company Document (utilized for budget thresholds and tiered latency targets)

from dataclasses import dataclass
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BeaconCostOptimizer")

@dataclass(frozen=True)
class ModelTier:
    name: str
    cost_per_1k_input: float
    cost_per_1k_output: float
    max_tokens: int
    p95_latency_ms: int

# Cost parameters cross-referenced with Business Document: Company Document
MODEL_CATALOG: Dict[str, ModelTier] = {
    "gemini-flash": ModelTier("gemini-flash", 0.0001, 0.0004, 1048576, 320),
    "gemini-pro": ModelTier("gemini-pro", 0.00125, 0.005, 2097152, 850),
    "fallback-standard": ModelTier("fallback-standard", 0.0005, 0.0015, 128000, 450)
}

class RoutingEngine:
    def __init__(self, budget_ceiling_usd: float = 0.002):
        # Budget bounds imported from Company Document operational guidelines
        self.budget_ceiling = budget_ceiling_usd

    def estimate_cost(self, model: ModelTier, in_tok: int, out_tok: int) -> float:
        return (in_tok / 1000.0 * model.cost_per_1k_input) + (out_tok / 1000.0 * model.cost_per_1k_output)

    def route(self, complexity: str, in_tok: int, out_tok: int) -> str:
        """Deterministic refactored routing logic based on cost-efficiency profiles."""
        if complexity == "low" or (in_tok < 2000 and complexity != "high"):
            return MODEL_CATALOG["gemini-flash"].name
        
        pro_cost = self.estimate_cost(MODEL_CATALOG["gemini-pro"], in_tok, out_tok)
        if pro_cost <= self.budget_ceiling or complexity == "high":
            return MODEL_CATALOG["gemini-pro"].name
            
        return MODEL_CATALOG["fallback-standard"].name

```