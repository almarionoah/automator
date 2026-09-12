# Chaos & Resilience Test Suite: Refactored Atlas Core Auth Service
**Author:** Iris Petrov  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D14 02:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos verification script and resilience test suite for the refactored Atlas Core Auth Service, executing fault injections, token corruption, and cache failovers against compliance thresholds established in Business Document: Company Document.

## Deliverable
```
"""
Project: Atlas Core
Service: Auth Service (Refactor Verification)
Author: Iris Petrov (Chaos Engineering)
Resource Reference: Business Document: Company Document was utilized to extract authoritative rate-limiting thresholds, session eviction policies, and SLA bounds for degraded fallback states.
"""

import asyncio
import pytest
import httpx
from chaos_toolkit import inject_latency, drop_redis_connection, corrupt_jwks_cache

AUTH_BASE_URL = "https://internal.itskokos.local/atlas/v2/auth"

@pytest.mark.chaos
@pytest.mark.asyncio
async def test_redis_session_cache_failure_fallback():
    """Verifies auth falls back to read-replica DB without exposing 500s during cache crash (Ref: Business Document: Company Document §4.2 SLA)."""
    async with httpx.AsyncClient(base_url=AUTH_BASE_URL) as client:
        token = (await client.post("/login", json={"user": "chaos_agent", "key": "t3st_p@ss"})).json()["access_token"]
        with drop_redis_connection(target_cluster="auth-cache-primary", duration_sec=5):
            responses = await asyncio.gather(*[
                client.get("/verify", headers={"Authorization": f"Bearer {token}"})
                for _ in range(50)
            ])
            for res in responses:
                assert res.status_code in (200, 429), f"Unexpected status {res.status_code} during cache drop"
                assert "X-Auth-Degraded" in res.headers

@pytest.mark.chaos
@pytest.mark.asyncio
async def test_jwks_rotation_poisoning_and_concurrency_race():
    """Injects corrupted JWKS payloads during high-concurrency token refresh spikes."""
    async with httpx.AsyncClient(base_url=AUTH_BASE_URL) as client:
        with corrupt_jwks_cache(error_rate=0.4):
            tasks = [client.post("/refresh", json={"refresh_token": f"fuzz_tok_{i}"}) for i in range(100)]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            valid_codes = {400, 401, 503}
            for r in results:
                if isinstance(r, httpx.Response):
                    assert r.status_code in valid_codes

```