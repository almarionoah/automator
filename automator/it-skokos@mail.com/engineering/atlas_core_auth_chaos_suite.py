# Atlas Core Auth Service: Chaos & Resiliency Validation Test Suite
**Author:** Jax Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 21:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Automated chaos testing suite and fault-injection harness for the refactored Atlas Core authentication service, targeting token poisoning, Redis partition split-brain states, and validating degraded-mode latency against SLA parameters in Company Document.

## Deliverable
```
"""
Atlas Core - Refactored Auth Service Chaos Engineering Test Harness
Author: Jax Okafor (Chaos Testing / Engineering)
Compliance Ref: Company Document (Section 4.2: Degraded-State Auth SLAs & Invalidation Timers)

Resource Usage Note:
'Company Document' was explicitly used to define resilience acceptance thresholds, 
specifically the 150ms degraded-state verification ceiling, rate-limiting boundaries under attack,
and token invalidation convergence limits across our SaaS & F2F kiosk endpoints.
"""

import asyncio
import random
import time
import httpx
import pytest

TARGET_URL = "http://atlas-core.internal/v2/auth"
MAX_DEGRADED_LATENCY_MS = 150  # Hard threshold derived from Company Document

async def inject_network_partition(proxy_control, service: str = "redis-cache", packet_loss: float = 0.85):
    """Simulate network partitioning between Auth microservice and cluster cache."""
    await proxy_control.set_fault(service=service, drop_rate=packet_loss, latency_ms=400)

async def chaos_token_tamper_storm(client: httpx.AsyncClient, valid_token: str, iterations: int = 250):
    """Inject high-entropy bit-flipped signatures, malformed payloads, and header overflows."""
    tampered_payloads = [
        valid_token[:-6] + "_malf",
        "Bearer null",
        f"Bearer {valid_token}.extra_sig_bytes",
        "Bearer " + "X" * 4096,
        "Bearer eyJhbGciOiJub25lIn0.e30."
    ]
    for _ in range(iterations):
        payload = random.choice(tampered_payloads)
        res = await client.post(f"{TARGET_URL}/verify", headers={"Authorization": payload})
        assert res.status_code in (400, 401, 403), f"Chaos failure: unhandled status {res.status_code}"

@pytest.mark.asyncio
async def test_auth_cache_failover_under_load(chaos_proxy):
    """Validates zero unauthorized bypasses and adherence to Company Document latency SLAs during failover."""
    async with httpx.AsyncClient(timeout=2.0) as client:
        login_res = await client.post(f"{TARGET_URL}/login", json={"client_id": "chaos-node-01", "scope": "kiosk:f2f"})
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]

        # Inject cluster degradation
        await inject_network_partition(chaos_proxy, "redis-cache", 0.90)

        start_time = time.perf_counter()
        verify_res = await client.post(f"{TARGET_URL}/verify", headers={"Authorization": f"Bearer {token}"})
        latency_ms = (time.perf_counter() - start_time) * 1000

        assert verify_res.status_code in (200, 202)
        assert latency_ms <= MAX_DEGRADED_LATENCY_MS, f"SLA breach: {latency_ms}ms > {MAX_DEGRADED_LATENCY_MS}ms defined in Company Document"
        
        # Execute poison attack during degraded state
        await chaos_token_tamper_storm(client, token, iterations=100)
        await chaos_proxy.heal_all()

```