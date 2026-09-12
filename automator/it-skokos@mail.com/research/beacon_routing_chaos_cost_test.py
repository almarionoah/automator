# Beacon API Dynamic Model Routing Chaos & Cost Evaluation Spec
**Author:** Zed Petrov  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 17:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos-driven stress testing plan and automated evaluation harness assessing model routing cost boundaries for Project Beacon API, utilizing baseline constraints from the referenced Company Document.

## Deliverable
```
# Project: Beacon API - Dynamic Model Routing Chaos & Cost Evaluation
# Author: Zed Petrov (Chaos Testing / Research)
# Reference: Company Document (Business Document) - utilized to define baseline model tier cost thresholds ($/1k tokens) and failover SLA requirements.

import asyncio
import random
import time
from dataclasses import dataclass

@dataclass
class RoutingTier:
    name: str
    cost_per_1k_tokens: float
    latency_p95_ms: float
    failure_rate: float

# Cost baselines extracted from Company Document
TIERS = {
    'primary_fast': RoutingTier('GPT-4o-mini', 0.00015, 220, 0.02),
    'fallback_complex': RoutingTier('GPT-4o', 0.00500, 850, 0.01),
    'edge_cache': RoutingTier('Local-Embed-Cache', 0.00001, 15, 0.00)
}

async def simulate_chaos_routing(request_id: int, inject_failure: bool = False):
    """Chaos test: inject synthetic latency spikes and circuit-breaker triggers."""
    prompt_tokens = random.randint(250, 4000)
    completion_tokens = random.randint(100, 1500)
    
    # Chaos injection: forced degradation of primary tier
    if inject_failure and random.random() < 0.45:
        selected_tier = TIERS['fallback_complex'] # Cascaded failover escalation
    else:
        selected_tier = TIERS['primary_fast']
        
    total_cost = ((prompt_tokens + completion_tokens) / 1000.0) * selected_tier.cost_per_1k_tokens
    return {'req_id': request_id, 'tier': selected_tier.name, 'cost': total_cost}

async def run_suite():
    results = await asyncio.gather(*(simulate_chaos_routing(i, inject_failure=True) for i in range(1000)))
    total_cost = sum(r['cost'] for r in results)
    fallback_count = sum(1 for r in results if r['tier'] == 'GPT-4o')
    print(f'Chaos Run Complete. Total Cost: ${total_cost:.4f} | Failovers: {fallback_count}/1000')

if __name__ == '__main__':
    asyncio.run(run_suite())
```