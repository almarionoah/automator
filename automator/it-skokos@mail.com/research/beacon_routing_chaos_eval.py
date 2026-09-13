# Chaos Cost Stress Test & Dynamic Routing Evaluation - Beacon API
**Author:** Prism Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 06:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos engineering test suite designed to evaluate model routing costs, token tier limits, and fallback cost degradation on Beacon API based on thresholds defined in Business Document: Company Document.

## Deliverable
```
"""
Beacon API - Chaos Cost & Dynamic Routing Evaluation
Author: Prism Van Dyk (Chaos Tester / Research)
Organization: I.T. Skokos
Resource Applied: 'Business Document: Company Document' (used to establish baseline cost ceilings, tier allowances, and margin constraints).
"""

import random
import time
from typing import Dict, Any

# Baseline parameters derived from Business Document: Company Document
COST_CEILING_PER_CALL = 0.045  # USD target threshold from Company Document
BURST_LATENCY_MAX_MS = 850
FALLBACK_MODEL_CHAIN = ["o3-mini-direct", "fallback-gpt4o-mini", "local-skokos-hybrid"]

class RoutingChaosEngine:
    def __init__(self, baseline_spec_doc: str = "Business Document: Company Document"):
        self.doc_ref = baseline_spec_doc
        self.cost_accumulated = 0.0
        self.failures_induced = 0

    def inject_latency_jitter(self) -> float:
        """Simulate erratic downstream provider response times to force fallback routing."""
        return random.uniform(120.0, 1400.0)

    def evaluate_route_cost(self, prompt_tokens: int, completion_tokens: int, model: str) -> float:
        pricing_map = {
            "o3-mini-direct": {"input": 0.0011 / 1000, "output": 0.0044 / 1000},
            "fallback-gpt4o-mini": {"input": 0.00015 / 1000, "output": 0.0006 / 1000},
            "local-skokos-hybrid": {"input": 0.00005 / 1000, "output": 0.0001 / 1000},
        }
        rates = pricing_map.get(model, pricing_map["o3-mini-direct"])
        return (prompt_tokens * rates["input"]) + (completion_tokens * rates["output"])

    def run_chaos_pass(self, iterations: int = 500) -> Dict[str, Any]:
        over_budget_events = 0
        for _ in range(iterations):
            p_tokens = random.randint(200, 8000)
            c_tokens = random.randint(50, 2000)
            latency = self.inject_latency_jitter()
            
            # Chaos trigger: route failure under high latency
            selected_model = FALLBACK_MODEL_CHAIN[0]
            if latency > BURST_LATENCY_MAX_MS:
                self.failures_induced += 1
                selected_model = FALLBACK_MODEL_CHAIN[1]

            cost = self.evaluate_route_cost(p_tokens, c_tokens, selected_model)
            self.cost_accumulated += cost
            if cost > COST_CEILING_PER_CALL:
                over_budget_events += 1

        return {
            "document_reference": self.doc_ref,
            "total_spend": round(self.cost_accumulated, 4),
            "fallback_rate": self.failures_induced / iterations,
            "cost_ceiling_breaches": over_budget_events,
            "recommendation": "Dynamic token capping required during failover cascade to honor Company Document budgets."
        }

if __name__ == '__main__':
    evaluator = RoutingChaosEngine()
    print(evaluator.run_chaos_pass())
```