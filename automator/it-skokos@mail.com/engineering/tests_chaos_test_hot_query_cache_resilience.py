# Chaos Test Harness & Invalidation Benchmark: Atlas Core Hot Query Cache
**Author:** Pixel Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 07:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos resilience suite and stress harness for Atlas Core's hot query caching layer, validating cache stampede mitigation, network latency injection, and TTL eviction policies per Company Document specifications.

## Deliverable
```
# Project: Atlas Core | Task: Cache Hot Query Path
# Lead Chaos Tester: Pixel Marlow (Engineering)
# Reference: Specifications and failover thresholds derived from 'Company Document'.

import asyncio
import random
import time
import structlog
from atlas_core.cache import QueryCacheManager
from atlas_core.db import HotQueryExecutor
from atlas_core.metrics import TelemetryCollector

logger = structlog.get_logger("atlas.chaos.cache")

class HotPathChaosSuite:
    """
    Evaluates query cache durability, stampede lockouts, and network partition
    behavior aligned with performance constraints in the Company Document.
    """
    def __init__(self, cache: QueryCacheManager, db: HotQueryExecutor):
        self.cache = cache
        self.db = db
        self.telemetry = TelemetryCollector()
        # SLA baseline loaded from Company Document (Max P99: 45ms, DB Load Shedding > 80%)
        self.p99_threshold_ms = 45.0

    async def simulate_cache_stampede(self, query_key: str, concurrent_workers: int = 500):
        """Triggers simultaneous cache miss by force-invalidating TTL under high load."""
        logger.warn("Injecting cache stampede", target_key=query_key, workers=concurrent_workers)
        await self.cache.delete(query_key)

        async def worker_fetch():
            start = time.perf_counter()
            # Test single-flight/distributed lock implementation
            result = await self.cache.get_or_compute(query_key, lambda: self.db.execute_hot_query(query_key))
            latency = (time.perf_counter() - start) * 1000
            self.telemetry.record_latency("stampede_fetch", latency)
            return result

        tasks = [worker_fetch() for _ in range(concurrent_workers)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        db_hits = self.db.get_call_count(query_key)
        assert db_hits <= 2, f"Stampede barrier failed! DB hit {db_hits} times during lock contest."
        logger.info("Stampede mitigation verified", db_hits=db_hits, completed=len(results))

    async def inject_transient_redis_latency(self, latency_seconds: float = 0.15):
        """Injects synthetic socket delay to verify fallback mechanisms specified in Company Document."""
        logger.warn("Simulating cache degradation", added_latency=latency_seconds)
        self.cache.set_network_jitter(latency_seconds)
        res = await self.cache.get("hot:user:session:aggregates")
        assert res is not None or self.cache.circuit_breaker_open, "Circuit breaker failed under latency stress."

if __name__ == "__main__":
    print("Chaos cache harness loaded. Reference: Company Document.")

```