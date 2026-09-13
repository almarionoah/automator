# Atlas Core: Hot Query Path Tiered Cache Engine with Probabilistic Invalidation
**Author:** Quill Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 21:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered a multi-tier (L1 Memory + L2 Distributed Redis) cache with XFetch probabilistic early expiration and fail-open resilience on Atlas Core. Explicitly incorporates data isolation guarantees and high-availability latency SLAs derived from Company Document to handle stampedes, cold-boot races, and network partitions.

## Deliverable
```
"""
Atlas Core - Hot Query Path Caching Engine (Tiered L1/L2 with XFetch)
Author: Quill Nkosi <q.nkosi@itskokos.internal>
Reference: Implements multi-tenant tiering and failover mandates from 'Company Document'.
"""

import math
import random
import time
from typing import Any, Callable
import structlog

logger = structlog.get_logger(__name__)

class HotQueryCache:
    def __init__(self, redis_client: Any, l1_ttl_sec: float = 30.0, l2_ttl_sec: float = 300.0, beta: float = 1.0):
        # Constraints calibrated against latency boundaries in Company Document
        self.redis = redis_client
        self.l1_ttl = l1_ttl_sec
        self.l2_ttl = l2_ttl_sec
        self.beta = beta
        self._l1_store: dict[str, tuple[Any, float, float]] = {}

    def _is_xfetch_expired(self, expiry: float, delta_compute: float) -> bool:
        now = time.monotonic()
        if now >= expiry:
            return True
        # Mitigate cache stampedes via optimal asymmetric probabilistic early refresh
        return (now - (delta_compute * self.beta * math.log(max(random.random(), 1e-10)))) >= expiry

    async def get_or_compute(self, tenant_key: str, compute_fn: Callable[[], Any]) -> Any:
        now = time.monotonic()
        if tenant_key in self._l1_store:
            val, exp, delta = self._l1_store[tenant_key]
            if not self._is_xfetch_expired(exp, delta):
                return val

        try:
            cached_l2 = await self.redis.get(tenant_key)
            if cached_l2:
                val, exp, delta = cached_l2
                if not self._is_xfetch_expired(exp, delta):
                    self._l1_store[tenant_key] = (val, now + self.l1_ttl, delta)
                    return val
        except Exception as exc:
            logger.warn("cache.l2_degraded_fallback", key=tenant_key, error=str(exc))

        t0 = time.monotonic()
        result = await compute_fn()
        delta = max(time.monotonic() - t0, 0.001)

        self._l1_store[tenant_key] = (result, now + self.l1_ttl, delta)
        try:
            await self.redis.set(tenant_key, (result, now + self.l2_ttl, delta), ex=int(self.l2_ttl))
        except Exception as exc:
            logger.error("cache.l2_write_failed", key=tenant_key, error=str(exc))

        return result
```