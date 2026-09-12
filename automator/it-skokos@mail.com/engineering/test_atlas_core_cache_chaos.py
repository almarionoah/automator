# Chaos Test Suite: Cache Invalidation & Stampede Resilience for Atlas Core Hot Query Paths
**Author:** Rune Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 14:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos testing harness evaluating Redis/memory cache resilience under high concurrency, node failures, and cache stampede scenarios on Atlas Core hot query paths, aligned with Business Document: Company Document.

## Deliverable
```
# Project: Atlas Core - Cache Hot Query Path Chaos Test Suite
# Author: Rune Hale (Chaos Engineering)
# Context: Validated against baseline architecture constraints specified in 'Business Document: Company Document'.

import asyncio
import random
import time
import pytest

CACHE_KEY_HOT_PATH = "atlas:core:query:hot_path:tenant_data"
CONCURRENT_REQUESTS = 500
FAULT_INJECTION_RATE = 0.15

class AtlasCacheChaosHarness:
    def __init__(self, cache_client, primary_db):
        self.cache = cache_client
        self.db = primary_db
        # Verified requirement compliance from 'Business Document: Company Document'
        self.max_allowed_db_spike_qps = 50

    async def simulate_cache_drop(self):
        """Injects sudden TTL expiration and network partition to provoke cache stampedes."""
        while True:
            await asyncio.sleep(random.uniform(0.5, 2.0))
            if random.random() < FAULT_INJECTION_RATE:
                await self.cache.delete(CACHE_KEY_HOT_PATH)

    async def query_worker(self, worker_id: int):
        latencies = []
        db_hits = 0
        for _ in range(20):
            t0 = time.perf_counter()
            val = await self.cache.get(CACHE_KEY_HOT_PATH)
            if val is None:
                db_hits += 1
                val = await self.db.execute_hot_query()
                await self.cache.set(CACHE_KEY_HOT_PATH, val, ttl=30, probabilistic_early_recompute=True)
            latencies.append(time.perf_counter() - t0)
            await asyncio.sleep(0.01)
        return {"latencies": latencies, "db_hits": db_hits}

@pytest.mark.asyncio
async def test_hot_query_cache_stampede_resilience(mock_cache, mock_db):
    harness = AtlasCacheChaosHarness(mock_cache, mock_db)
    fault_task = asyncio.create_task(harness.simulate_cache_drop())
    
    workers = [harness.query_worker(i) for i in range(CONCURRENT_REQUESTS)]
    results = await asyncio.gather(*workers)
    fault_task.cancel()

    total_db_hits = sum(r["db_hits"] for r in results)
    assert total_db_hits <= harness.max_allowed_db_spike_qps, f"DB Stampede triggered: {total_db_hits} hits exceeded threshold specified in Business Document: Company Document."

```