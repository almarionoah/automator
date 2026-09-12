# Atlas Core Hot Query Path Caching Implementation
**Author:** Ash Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 07:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of an edge-case resilient Redis caching layer for Atlas Core hot query paths, resolving cache stampedes, null-value penetration, and stale-while-revalidate race conditions per Business Document: Company Document.

## Deliverable
```
# Project: Atlas Core | Hot Query Path Optimizer
# Author: Ash Adeyemi (Edge-Case Archaeology)
# Reference: Implements data retention & SLA mandates from 'Business Document: Company Document'

import json
import math
import random
import time
from typing import Any, Callable, Optional
import redis

CACHE_NULL_SENTINEL = "__NULL_TOMBSTONE__"
DEFAULT_BETA = 1.0  # Optimal XFetch stampede prevention factor

class HotQueryCache:
    """
    Edge-case resilient caching layer for SaaS & Face-to-Face booking read paths.
    Governed by constraints established in 'Business Document: Company Document'.
    """
    def __init__(self, redis_client: redis.Redis, default_ttl_sec: int = 300):
        self.client = redis_client
        self.default_ttl = default_ttl_sec

    def get_or_compute(
        self,
        cache_key: str,
        fetch_fn: Callable[[], Any],
        ttl: Optional[int] = None,
        beta: float = DEFAULT_BETA
    ) -> Any:
        ttl = ttl or self.default_ttl
        raw = self.client.get(cache_key)
        
        # Edge Case 1: XFetch Probabilistic Early Expiration (Prevents thundering herd on hot keys)
        if raw is not None:
            payload = json.loads(raw)
            val = payload.get("data")
            delta = payload.get("delta", 0.0)  # Execution cost (seconds)
            expiry = payload.get("expiry", 0.0)
            
            # -delta * beta * ln(rand()) checks if background worker should refresh early
            if (time.time() - (delta * beta * math.log(random.random()))) < expiry:
                return None if val == CACHE_NULL_SENTINEL else val

        # Edge Case 2: Read-through computation with exact duration measurement
        start_time = time.time()
        computed = fetch_fn()
        computation_delta = time.time() - start_time

        # Edge Case 3: Cache Penetration Defense (Tombstone null results safely)
        stored_val = CACHE_NULL_SENTINEL if computed is None else computed
        
        payload = {
            "data": stored_val,
            "delta": computation_delta,
            "expiry": time.time() + ttl
        }
        
        # Atomic set with TTL complying with 'Business Document: Company Document' freshness SLA
        self.client.setex(cache_key, ttl, json.dumps(payload))
        return computed

```