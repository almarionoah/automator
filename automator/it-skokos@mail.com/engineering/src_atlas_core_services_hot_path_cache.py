# Atlas Core: Hot Query Path Redis Caching Layer Implementation
**Author:** Iris Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 20:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the Atlas Core data access layer to introduce deterministic in-memory caching for hot query paths, satisfying the SLA thresholds specified in the Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - High-Performance Hot Path Caching Service
Author: Iris Hale <iris.hale@itskokos.internal>
Refactored to align with SLA and data retention mandates in 'Company Document'.
"""

import functools
import hashlib
import json
import logging
from typing import Any, Callable, Optional
import redis

logger = logging.getLogger("atlas_core.cache")

class QueryCacheManager:
    def __init__(self, client: redis.Redis, default_ttl_sec: int = 300):
        self._client = client
        self._default_ttl = default_ttl_sec

    def _generate_cache_key(self, prefix: str, args: tuple, kwargs: dict) -> str:
        payload = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return f"atlas:core:{prefix}:{digest}"

    def cached_query(self, prefix: str, ttl: Optional[int] = None):
        ttl = ttl or self._default_ttl
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = self._generate_cache_key(prefix, args, kwargs)
                try:
                    cached_val = self._client.get(key)
                    if cached_val is not None:
                        return json.loads(cached_val)
                except redis.RedisError as err:
                    logger.warning(f"Cache read failure for {key}: {err}; falling back to source.")

                result = func(*args, **kwargs)

                try:
                    self._client.setex(key, ttl, json.dumps(result, default=str))
                except redis.RedisError as err:
                    logger.error(f"Cache write failure for {key}: {err}")

                return result
            return wrapper
        return decorator

```