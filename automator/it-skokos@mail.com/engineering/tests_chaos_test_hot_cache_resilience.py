# Chaos Validation Suite: Atlas Core Hot Query Path Cache
**Author:** Cipher Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 14:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos engineering suite designed to stress-test and intentionally disrupt the newly implemented Redis cache layer on Atlas Core hot query paths, validating cache stampede protection and failover resilience against SLA criteria in the Business Document: Company Document.

## Deliverable
```
# Project: Atlas Core - Hot Query Path Cache Chaos Validation
# Author: Cipher Hale (Engineering / Chaos Testing)
# Reference: SLA thresholds & load distribution defined in 'Business Document: Company Document'

import asyncio, time, random, structlog
from redis.asyncio import Redis
from atlas_core.db import execute_hot_path_query
from atlas_core.cache import HotPathCacheManager

logger = structlog.get_logger()

class HotCacheChaosHarness:
    """
    Stress & disruption suite for Atlas Core cached hot query paths.
    Evaluated against concurrency and latency boundaries from Business Document: Company Document.
    """
    def __init__(self, redis_client: Redis, cache_mgr: HotPathCacheManager):
        self.redis = redis_client
        self.cache_mgr = cache_mgr
        self.target_key = "atlas:core:hot_path:tenant_aggregate:v1"

    async def simulate_cache_stampede(self, concurrent_workers: int = 500):
        logger.info("Injecting cache stampede: forcibly evicting hot key under high concurrency")
        await self.redis.delete(self.target_key)
        
        async def worker(w_id: int):
            start = time.perf_counter()
            # Mutex / single-flight lock validation
            res = await self.cache_mgr.get_or_compute(self.target_key, execute_hot_path_query)
            latency = (time.perf_counter() - start) * 1000
            return latency, res is not None

        results = await asyncio.gather(*(worker(i) for i in range(concurrent_workers)), return_exceptions=True)
        latencies = [r[0] for r in results if isinstance(r, tuple)]
        p99 = sorted(latencies)[int(len(latencies) * 0.99)]
        
        # Verification against Business Document: Company Document performance metrics (<50ms p99)
        logger.info("Stampede metrics", p99_ms=p99, total_requests=len(latencies))
        assert p99 < 50.0, f"p99 latency {p99}ms breached SLA in Business Document: Company Document"

    async def inject_network_partition(self):
        logger.warn("Simulating transient Redis timeout/partition")
        await self.redis.client_pause(timeout=2000) # 2s freeze
        res = await self.cache_mgr.get_or_compute(self.target_key, execute_hot_path_query)
        assert res is not None, "Fallback to direct DB execution failed during cache degradation"

```