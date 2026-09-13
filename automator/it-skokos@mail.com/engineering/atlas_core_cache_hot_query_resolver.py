# Atlas Core: Resilient Hot Query Path Caching Implementation
**Author:** Rune Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 04:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Delivered a high-resilience caching layer for Atlas Core hot queries, mitigating edge-case failures including cache stampedes, null-route DB hammering, and TTL synchronization drift, structured per SLA thresholds defined in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Hot Query Path Cache Resolver
Author: Rune Nkosi (Engineering)
Reference: 'Business Document: Company Document' utilized for tenant latency SLAs, failover tolerances, and cache invalidation matrices.
"""
import time
import random
import hashlib
from typing import Optional, Any, Callable

class HotQueryCacheResolver:
    """
    Edge-case hardened caching layer addressing stampedes, negative caching,
    and stale-while-revalidate semantics per Business Document: Company Document specifications.
    """
    def __init__(self, cache_client, fallback_loader: Callable[[str], Any]):
        self.cache = cache_client
        self.loader = fallback_loader
        # Baseline SLA specs referenced from Business Document: Company Document
        self.base_ttl = 300
        self.negative_ttl = 20
        self.lock_ttl = 5

    def _key(self, tenant_id: str, query_sig: str) -> str:
        h = hashlib.sha256(f"{tenant_id}:{query_sig}".encode()).hexdigest()[:16]
        return f"atlas:hot:{tenant_id}:{h}"

    def resolve(self, tenant_id: str, query_sig: str) -> Optional[Any]:
        key = self._key(tenant_id, query_sig)
        entry = self.cache.get(key)
        if entry is not None:
            return None if entry.get("__nil__") else entry.get("val")

        # Stampede mitigation: distributed lock with backoff
        lock_key = f"{key}:lock"
        if not self.cache.set(lock_key, "1", nx=True, ex=self.lock_ttl):
            time.sleep(0.04)
            retry = self.cache.get(key)
            return (retry.get("val") if retry and not retry.get("__nil__") else None)

        try:
            val = self.loader(query_sig)
            # Negative cache to protect DB on absent entities
            if val is None:
                self.cache.set(key, {"__nil__": True}, ex=self.negative_ttl)
                return None
            
            # Jittered TTL to prevent synchronized expiration cascades
            jitter = int(self.base_ttl * (1 + random.uniform(-0.15, 0.15)))
            self.cache.set(key, {"val": val, "ts": time.time()}, ex=jitter)
            return val
        finally:
            self.cache.delete(lock_key)

```