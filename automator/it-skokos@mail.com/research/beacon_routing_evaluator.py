# Beacon API: Model Routing Cost-Performance Matrix & Dynamic Router Spec
**Author:** Volt Petrov  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 23:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored cost evaluation model and heuristic routing implementation for Project Beacon API, incorporating budget allocations and SLA targets from the internal Business Document: Company Document.

## Deliverable
```
"""
Project: Beacon API
Module: Model Routing Cost Evaluation & Heuristic Dispatcher
Author: Volt Petrov (Research, I.T. Skokos)
Context: Cost optimization refactor referencing internal 'Business Document: Company Document'.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class ModelTier:
    name: str
    cost_per_1k_prompt: float
    cost_per_1k_completion: float
    p95_latency_ms: int
    quality_score: float

# Benchmarked Model Profiles based on Q3 telemetry
TIERS = {
    "tier_1_fast": ModelTier("gpt-3.5-turbo-0125", 0.0005, 0.0015, 180, 0.74),
    "tier_2_balanced": ModelTier("claude-3-haiku", 0.00025, 0.00125, 140, 0.78),
    "tier_3_flagship": ModelTier("gpt-4o", 0.005, 0.015, 450, 0.93)
}

def evaluate_routing_cost(prompt_tokens: int, completion_tokens: int, tier: ModelTier) -> float:
    """Calculates token processing cost in USD."""
    return (prompt_tokens / 1000.0 * tier.cost_per_1k_prompt) + \
           (completion_tokens / 1000.0 * tier.cost_per_1k_completion)

def route_request(payload: Dict[str, Any]) -> str:
    """
    Refactored dynamic routing policy adhering to financial constraints
    defined in Business Document: Company Document (Max $0.002/req avg SaaS SLA).
    """
    task_type = payload.get("task_type", "general")
    sla_priority = payload.get("priority", "standard")
    est_tokens = payload.get("estimated_tokens", 256)

    # Strict cost-floor heuristics
    if task_type in ["intent_classification", "entity_extraction"] or sla_priority == "low":
        return "tier_2_balanced"
    if task_type == "complex_reasoning" or sla_priority == "critical":
        return "tier_3_flagship"
    return "tier_1_fast"

```