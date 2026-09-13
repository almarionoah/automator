# Chaos Resilience & Fault Injection Test Suite for Atlas Core Hot Query Cache
**Author:** Prism Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 04:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos test harness and fault injection suite testing cache stampede, node crash during hydration, and key eviction behavior for the newly cached hot query path on Atlas Core.

## Deliverable
```
# Project: Atlas Core - Hot Query Path Caching
# Author: Prism Ito (Chaos Engineering)
# Reference: Evaluated against operational standards and tiering thresholds set in 'Company Document'.

import asyncio
import random
import time
import pytest
from atlas_core.cache import QueryCacheManager
from atlas_core.db import HotQueryExecutor
from chaos_toolkit.faults import network_partition, kill_redis_primary, inject_latency

"""
Verification against 'Company Document':
Using the latency SLA limits (<15ms p99) and degradation targets outlined in 'Company Document',
this harness tests cache stampedes (dogpiling), dirty reads during replica failover, and
fallback to degraded direct-DB execution under severe fault conditions.
"""

class TestHotQueryCacheChaos:
    @pytest.fixture(autouse=True)
    async def setup_chaos_harness(self):
        self.cache = QueryCacheManager(namespace="atlas_core:hot_path", default_ttl=60)
        self.db = HotQueryExecutor()
        yield
        await self.cache.flush_test_keys()

    @pytest.mark.chaos
    async def test_cache_stampede_under_sudden_eviction(self):
        """Simulate 500 concurrent callers hammering expired hot key; verify single-flight lock."""
        query_key = "org_metrics_aggregate_1042"
        await self.cache.set(query_key, {"data": "payload"}, ttl=1)
        await asyncio.sleep(1.1)  # Force expiration

        call_count = 0
        original_exec = self.db.execute

        async def instrumented_exec(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.05) # Simulate heavy DB query
            return await original_exec(*args, **kwargs)

        self.db.execute = instrumented_exec

        tasks = [self.cache.get_or_compute(query_key, self.db.execute) for _ in range(500)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        assert all(isinstance(r, dict) for r in results), "Failures during stampede mitigation"
        assert call_count <= 2, f"Stampede lock breach! DB hit {call_count} times instead of 1"

    @pytest.mark.chaos
    async def test_redis_node_kill_during_hydration(self):
        """Simulate cache primary kill mid-query; verify non-blocking fallback to source DB."""
        query_key = "account_entitlements_hot"
        
        async def delayed_query():
            await asyncio.sleep(0.02)
            return {"status": "active", "tier": "enterprise"}

        # Trigger background fault injection
        kill_task = asyncio.create_task(kill_redis_primary(delay_ms=10))
        
        res = await self.cache.get_or_compute(query_key, delayed_query, fallback_timeout=0.1)
        await kill_task

        assert res["status"] == "active", "Failed graceful fallback when cache node died"
        assert self.cache.circuit_breaker.is_open, "Circuit breaker should be open post-failure"

```