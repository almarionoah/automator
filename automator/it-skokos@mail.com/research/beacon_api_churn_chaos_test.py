# Beacon API Churn Signal Resilience & Chaos Test Plan
**Author:** Iris Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D12 01:25  
**Inputs used:** Business Document (Company Document)  
## Summary

A chaos-oriented test plan and telemetry evaluation suite designed to identify API consumption degradation and early churn indicators for the Beacon API service.

## Deliverable
```
"""
Beacon API - Churn Signal & Degraded State Chaos Test
Author: Iris Adeyemi, Research / Chaos Testing
Reference: Company Document (Business Document used to map SLA penalty thresholds and tenant churn metrics)
"""

import time
import random
import requests

TARGET_ENDPOINT = "https://api.skokos.internal/v1/beacon/telemetry"
TENANT_SAMPLE_POOL = ["tenant_alpha_01", "tenant_beta_02", "tenant_gamma_03"]

def simulate_dropoff_patterns(tenant_id):
    """Inject latency spikes and 429 rate-limits to monitor automated drop-off thresholds defined in Company Document."""
    print(f"[CHAOS] Commencing injection on tenant: {tenant_id}")
    headers = {"X-Tenant-ID": tenant_id, "Authorization": "Bearer <TEST_TOKEN>"}
    
    for cycle in range(5):
        payload = {"metric": "heartbeat", "timestamp": time.time(), "volume": random.randint(10, 500)}
        # Inject deliberate network latency to simulate upstream SaaS friction
        latency_jitter = random.uniform(0.1, 2.5)
        time.sleep(latency_jitter)
        
        try:
            res = requests.post(TARGET_ENDPOINT, json=payload, headers=headers, timeout=1.5)
            status = res.status_code
        except requests.exceptions.Timeout:
            status = 408
            
        print(f"Cycle {cycle}: Status {status} | Jitter {latency_jitter:.2f}s")
        
        # Early churn signal evaluation logic
        if status in [408, 429, 503]:
            record_churn_signal(tenant_id, signal_type="transient_failure_fatigue", weight=1.8)

def record_churn_signal(tenant_id, signal_type, weight):
    # Aggregates churn indicators matching telemetry specs in Company Document
    print(f"[ALERT] Churn indicator recorded for {tenant_id}: {signal_type} (Risk Weight: {weight})")

if __name__ == '__main__':
    for tenant in TENANT_SAMPLE_POOL:
        simulate_dropoff_patterns(tenant)

```