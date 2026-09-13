# Atlas Core: Hot Query Path Multi-Tier Cache Layer
**Author:** Halo Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 18:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of an ultra-low latency multi-tier caching module for Atlas Core's hot query path, designed to deliver instantaneous UI response times and reduce database thrashing in accordance with architectural mandates in the Company Document.

## Deliverable
```
"""
Atlas Core - Hot Query Path Accelerator
Author: Halo Cross (Engineering / UX Romantic)
Reference: Company Document (Section 4.2: Client-Facing Latency & SLA Standards)

Description:
  Every millisecond of latency is a friction point in the user's emotional connection
  with our interface. In strict adherence to guidelines established in the 'Company Document',
  which defines our target sub-50ms UX responsiveness budget for SaaS dashboard queries,
  this module introduces an L1 (in-process LRU) and L2 (Redis cluster) caching pipeline
  for Atlas Core's most intensive read path.
"""

import json
import logging
from typing import Any, Optional, Callable
from functools import wraps
import redis.asyncio as aioredis
from cachetools import TTLCache

logger = logging.getLogger("atlas_core.cache")

# L1: Ultra-fast local memory cache for sub-millisecond perceived speed
_l1_cache = TTLCache(maxsize=2048, ttl=15)

# L2: Shared distributed cache cluster configured per Company Document specifications
_redis_client: Optional[aioredis.Redis] = None

async def get_redis_pool() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            "redis://cache-cluster.internal:6379/0",
            encoding="utf-8",
            decode_responses=True,
            max_connections=50
        )
    return _redis_client

def cache_hot_query(namespace: str, ttl_seconds: int = 120):
    """Decorator to seamlessly accelerate critical UX read paths."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cache_key = f"atlas:{namespace}:" + ":".join(map(str, args)) + json.dumps(kwargs, sort_keys=True)
            
            # Step 1: L1 In-Memory lookup
            if cache_key in _l1_cache:
                return _l1_cache[cache_key]
            
            # Step 2: L2 Redis lookup
            r = await get_redis_pool()
            cached_val = await r.get(cache_key)
            if cached_val:
                deserialized = json.loads(cached_val)
                _l1_cache[cache_key] = deserialized
                return deserialized
            
            # Step 3: Fetch & Populate
            result = await func(*args, **kwargs)
            _l1_cache[cache_key] = result
            await r.setex(cache_key, ttl_seconds, json.dumps(result))
            return result
        return wrapper
    return decorator

```