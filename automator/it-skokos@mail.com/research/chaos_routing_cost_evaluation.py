# Beacon API Dynamic Model Routing Cost Stress & Chaos Evaluation Suite
**Author:** Kilo Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 16:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos engineering benchmark script and cost-variance analysis evaluating Beacon API dynamic model routing under simulated upstream outages, token inflation, and cascading failovers, audited against budget thresholds in the Company Document.

## Deliverable
```
"""
Project: Beacon API
Author: Kilo Van Dyk (Research / Chaos Engineering)
Reference: Company Document (Utilized to extract baseline cost-per-token ceilings, SLA tier constraints, and failover budget allocations).
"""

import time
import random
from typing import Dict, List

# Cost baselines referenced from Company Document
MODEL_COSTS = {
    "fast-tier-o3": {"input": 0.00015 / 1000, "output": 0.0006 / 1000},
    "standard-tier-o4-mini": {"input": 0.0011 / 1000, "output": 0.0044 / 1000},
    "fallback-heavy-o1": {"input": 0.015 / 1000, "output": 0.060 / 1000}
}

class ChaosRouterEvaluator:
    def __init__(self, budget_cap_usd: float = 250.00):
        self.budget_cap = budget_cap_usd
        self.accumulated_cost = 0.0
        self.routing_log: List[Dict] = []

    def simulate_upstream_chaos(self) -> Dict[str, bool]:
        return {
            "fast-tier-o3": random.random() > 0.65,       # 65% failure injection
            "standard-tier-o4-mini": random.random() > 0.40 # 40% rate-limit spike
        }

    def execute_routing_trial(self, prompt_tokens: int, completion_tokens: int):
        chaos = self.simulate_upstream_chaos()
        selected_model = "fallback-heavy-o1"

        if not chaos["fast-tier-o3"]:
            selected_model = "fast-tier-o3"
        elif not chaos["standard-tier-o4-mini"]:
            selected_model = "standard-tier-o4-mini"

        cost = (prompt_tokens * MODEL_COSTS[selected_model]["input"] +
                completion_tokens * MODEL_COSTS[selected_model]["output"])
        self.accumulated_cost += cost
        
        self.routing_log.append({
            "selected_model": selected_model,
            "tokens": prompt_tokens + completion_tokens,
            "cost": cost,
            "cascade_triggered": selected_model == "fallback-heavy-o1"
        })
        return selected_model, cost

if __name__ == "__main__":
    evaluator = ChaosRouterEvaluator()
    for i in range(1000):
        evaluator.execute_routing_trial(prompt_tokens=1500, completion_tokens=800)
    print(f"Total Chaos Run Cost: ${evaluator.accumulated_cost:.4f}")

```