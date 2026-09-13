# Beacon API Dynamic Routing Cost Stress Test & Chaos Evaluation
**Author:** Iris Petrov  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 07:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos engineering test suite evaluating cost anomalies and fallback routing behaviors under upstream latency and rate limit degradation, calibrated against thresholds defined in Company Document.

## Deliverable
```
"""
Project: Beacon API
Agent: Iris Petrov (Chaos Engineering / Research)
Deliverable: Model Routing Cost Stress Suite

Reference Resources:
- Business Document: Company Document (Used to establish baseline target cost ceilings, SLA thresholds, and fallback cascade priorities).
"""

import asyncio
import random
import time
from dataclasses import dataclass

@dataclass
class RouteMetrics:
    model_id: str
    cost_per_1k_tokens: float
    latency_ms: float
    failure_rate: float

# Baseline pricing aligned with Company Document specifications
MODEL_TIERS = {
    "primary": RouteMetrics("gemini-3.6-flash", cost_per_1k_tokens=0.0001, latency_ms=120.0, failure_rate=0.0),
    "fallback_fast": RouteMetrics("gemini-3.0-mini", cost_per_1k_tokens=0.00005, latency_ms=90.0, failure_rate=0.0),
    "fallback_deep": RouteMetrics("gemini-pro-legacy", cost_per_1k_tokens=0.0015, latency_ms=850.0, failure_rate=0.0),
}

class ChaosCostEvaluator:
    def __init__(self):
        self.total_cost = 0.0
        self.cascade_events = 0

    async def simulate_traffic_spike_with_fault_injection(self, iterations=1000):
        """Injects random provider timeouts to force fallback cascade, measuring cost blowouts."""
        for _ in range(iterations):
            # Inject chaos: 35% upstream degradation on primary tier
            primary_fault = random.random() < 0.35
            tokens = random.randint(250, 4000)

            if not primary_fault:
                route = MODEL_TIERS["primary"]
            else:
                self.cascade_events += 1
                # Chaos: 15% fallback failure routing to expensive deep fallback
                deep_fallback = random.random() < 0.15
                route = MODEL_TIERS["fallback_deep"] if deep_fallback else MODEL_TIERS["fallback_fast"]

            cost = (tokens / 1000.0) * route.cost_per_1k_tokens
            self.total_cost += cost

        return {"total_cost": round(self.total_cost, 4), "cascades": self.cascade_events}

```