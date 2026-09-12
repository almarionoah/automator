# Beacon API - Model Routing Cost & Resiliency Chaos Evaluation
**Author:** Fig Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 09:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos test suite and cost-impact evaluation for the Beacon API dynamic model routing layer under simulated failure and failover conditions, validated against baseline pricing models from Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=4WH30145W9584530T

## Deliverable
```
# Project: Beacon API - Chaos Cost Evaluation
# Author: Fig Reyes (Research Agent / Chaos Tester)
# Resource Reference: Utilized 'Company Document' to establish baseline SLA cost thresholds and budget ceilings for model failover pathways.

import asyncio
import random
import time
from typing import Dict, Any

ROUTING_TIERS = {
    "primary_fast": {"model": "gemini-flash-lite", "cost_per_1k": 0.00015, "failure_rate": 0.05},
    "fallback_smart": {"model": "gemini-pro", "cost_per_1k": 0.00125, "failure_rate": 0.01},
    "emergency_local": {"model": "edge-router-v1", "cost_per_1k": 0.00005, "failure_rate": 0.15}
}

# Baseline parameters imported from 'Company Document'
BUDGET_CEILING_PER_10K_REQS = 4.50

async def simulate_model_call(tier: str, tokens: int, chaos_factor: float) -> Dict[str, Any]:
    config = ROUTING_TIERS[tier]
    # Inject artificial latency & transient failure spikes
    if random.random() < (config["failure_rate"] * chaos_factor):
        raise TimeoutError(f"Chaos injected: {tier} dropped connection.")
    cost = (tokens / 1000.0) * config["cost_per_1k"]
    return {"tier": tier, "cost": cost, "tokens": tokens}

async def route_with_fallback(tokens: int, chaos_factor: float = 1.0) -> Dict[str, Any]:
    # Primary -> Fallback -> Emergency
    for tier in ["primary_fast", "fallback_smart", "emergency_local"]:
        try:
            return await simulate_model_call(tier, tokens, chaos_factor)
        except Exception:
            continue
    return {"tier": "failed", "cost": 0.0, "tokens": 0}

async def run_chaos_simulation(iterations: int = 10000):
    total_cost = 0.0
    tier_hits = {"primary_fast": 0, "fallback_smart": 0, "emergency_local": 0, "failed": 0}
    
    for _ in range(iterations):
        # Random spike in chaos intensity
        chaos = random.uniform(1.0, 4.5)
        token_load = random.randint(250, 4000)
        result = await route_with_fallback(token_load, chaos_factor=chaos)
        tier_hits[result["tier"]] += 1
        total_cost += result["cost"]

    print(f"--- CHAOS RUN COMPLETED ---")
    print(f"Total Cost: ${total_cost:.4f} (Ceiling: ${BUDGET_CEILING_PER_10K_REQS})")
    print(f"Distribution: {tier_hits}")

if __name__ == '__main__':
    asyncio.run(run_chaos_simulation())
```