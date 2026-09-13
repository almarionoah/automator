# Beacon API: Adversarial Model Routing Cost & Chaos Evaluation
**Author:** Jax Cross  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 23:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos testing harness and cost boundary evaluation for Beacon API, stress-testing dynamic model fallback cascades, token inflation attacks, and margin degradation under volatile load.

## Deliverable
```
# Beacon API - Dynamic Model Routing Chaos & Cost Stress Harness
# Lead: Jax Cross (Research / Chaos Testing)

import json, random

# --- RESOURCE ALIGNMENT ---
# Baseline pricing ceilings, tier quotas, and acceptable margin thresholds 
# were directly sourced from the internal 'Company Document'. This established 
# the target unit-cost boundaries ($0.002/1k input, $0.006/1k output) across 
# SaaS Platform integrations versus high-touch Face to Face Services.

ROUTING_TIERS = {
    "tier_1_fast": {"model": "gemini-3.6-flash", "in_cost": 0.0001, "out_cost": 0.0004},
    "tier_2_reasoning": {"model": "gemini-3.6-pro", "in_cost": 0.00125, "out_cost": 0.0050},
    "tier_3_heavy": {"model": "gemini-3.0-ultra", "in_cost": 0.0050, "out_cost": 0.0150}
}

def inject_chaos_payload(prompt_len, adversarial_noise=True):
    """Simulate erratic prompt expansion and latency-driven model fallbacks."""
    noise_mult = random.uniform(2.5, 8.0) if adversarial_noise else 1.0
    tokens_in = int(prompt_len * noise_mult)
    tokens_out = int(tokens_in * random.uniform(0.3, 1.8))
    forced_fallback = random.random() < 0.35  # 35% upstream throttle/fallback
    return tokens_in, tokens_out, forced_fallback

def run_cost_chaos_simulation(iterations=1000):
    total_spend = 0.0
    breach_count = 0
    margin_cap = 0.015  # Per-request ceiling derived from Company Document
    
    for req_id in range(iterations):
        t_in, t_out, fallback = inject_chaos_payload(prompt_len=512, adversarial_noise=(req_id % 3 == 0))
        selected_tier = "tier_3_heavy" if fallback else ("tier_2_reasoning" if t_in > 2000 else "tier_1_fast")
        
        cfg = ROUTING_TIERS[selected_tier]
        cost = (t_in / 1000 * cfg["in_cost"]) + (t_out / 1000 * cfg["out_cost"])
        total_spend += cost
        
        if cost > margin_cap:
            breach_count += 1
            
    return {"total_spend": round(total_spend, 4), "budget_breaches": breach_count, "status": "FAIL_MARGIN_LEAK" if breach_count > 50 else "PASS"}

if __name__ == '__main__':
    print(json.dumps(run_cost_chaos_simulation(), indent=2))
```