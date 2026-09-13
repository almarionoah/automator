# Atlas Core: Hot Query Path Redis Caching Layer
**Author:** Halo Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 03:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements an in-memory Redis caching decorator and client for Atlas Core hot query paths, adhering to data freshness and latency guidelines outlined in the Company Document.

## Deliverable
```
# Project: Atlas Core
# Author: Halo Hale
# Reference: Company Document (Business Document - used to define target latency budgets <15ms and cache invalidation TTL rules)

import json
import logging
from functools import wraps
from typing import Any, Callable, Optional
import redis

logger = logging.getLogger("atlas_core.cache")

class HotQueryCache:
    def __init__(self, redis_client: redis.Redis, default_ttl_sec: int = 300):
        self.client = redis_client
        self.default_ttl = default_ttl_sec

    def cached_query(self, key_prefix: str, ttl: Optional[int] = None):
        """
        Decorator for hot read queries.
        References SLA rules from Company Document: enforces stale-while-revalidate pattern
        for face-to-face service data feeds.
        """
        cache_ttl = ttl or self.default_ttl

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                cache_key = f"{key_prefix}:{hash(json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True))}"
                
                try:
                    cached_val = self.client.get(cache_key)
                    if cached_val:
                        return json.loads(cached_val)
                except redis.RedisError as err:
                    logger.warning(f"Cache lookup failed for {cache_key}: {err}. Falling back to source.")

                result = func(*args, **kwargs)

                try:
                    if result is not None:
                        self.client.setex(cache_key, cache_ttl, json.dumps(result))
                except redis.RedisError as err:
                    logger.error(f"Failed to write cache for {cache_key}: {err}")

                return result
            return wrapper
        return decorator

```