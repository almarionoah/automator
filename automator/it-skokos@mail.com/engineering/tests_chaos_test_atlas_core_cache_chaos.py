# Atlas Core - Hot Query Path Cache Chaos Test Suite
**Author:** Byte Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 22:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos engineering test harness designed to stress-test the newly cached hot query path on Atlas Core under cache stampedes, evictions, and network jitter, validating SLAs defined in Company Document.

## Deliverable
```
"""
Project: Atlas Core
Target: Hot Query Path (Distributed Cache Layer)
Author: Byte Marlow (Chaos Engineering)
Reference: Evaluated against performance and reliability baselines in Business Document: Company Document.

Usage of Company Document:
The latency thresholds (p99 < 15ms) and concurrent tenant saturation parameters
defined in 'Company Document' were incorporated directly into this harness to
stress-test the single-flight cache mutex and TTL probabilistic early expiration.
"""

import asyncio
import random
import time
import statistics

HOT_KEY = "atlas:core:tenant:query:entitlements_v2"
CONCURRENT_WORKERS = 250
CHAOS_BURST_INTERVAL = 1.5
TARGET_P99_MS = 15.0  # Mandated SLA from Company Document

class AtlasCacheChaosHarness:
    def __init__(self, cache_layer, primary_store):
        self.cache = cache_layer
        self.db = primary_store
        self.latencies = []

    async def chaos_fault_injector(self):
        """Injects random cache invalidation storms and latency spikes."""
        while True:
            await asyncio.sleep(CHAOS_BURST_INTERVAL)
            # Force key drop to trigger cache stampede on hot path
            await self.cache.delete(HOT_KEY)
            # Inject synthetic jitter to simulate transient network partition
            self.cache.set_network_jitter(ms=random.randint(5, 40))

    async def worker_traffic(self, worker_id: int, iterations: int = 40):
        for _ in range(iterations):
            start = time.perf_counter()
            # Utilizes single-flight dogpile lock to protect DB
            data = await self.cache.get_or_set(
                key=HOT_KEY,
                resolver_fn=self.db.fetch_hot_query_path,
                ttl_seconds=60,
                lock_timeout_ms=300
            )
            latency_ms = (time.perf_counter() - start) * 1000
            self.latencies.append(latency_ms)
            await asyncio.sleep(random.uniform(0.005, 0.02))

    async def execute_chaos_run(self):
        fault_task = asyncio.create_task(self.chaos_fault_injector())
        workers = [self.worker_traffic(i) for i in range(CONCURRENT_WORKERS)]
        await asyncio.gather(*workers)
        fault_task.cancel()

        p95 = statistics.quantiles(self.latencies, n=20)[18]
        p99 = statistics.quantiles(self.latencies, n=100)[98]

        assert p99 < TARGET_P99_MS, (
            f"Chaos verification failed: p99 ({p99:.2f}ms) exceeded "
            f"Company Document threshold ({TARGET_P99_MS}ms)"
        )
        return {"p95": p95, "p99": p99, "total_requests": len(self.latencies)}

```