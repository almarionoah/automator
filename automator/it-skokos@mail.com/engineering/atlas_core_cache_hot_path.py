# Atlas Core - Hot Query Path Caching Implementation
**Author:** Jax Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 11:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of a Redis-backed multi-level caching layer for hot query paths on the Atlas Core service, designed according to data freshness and latency requirements outlined in the Company Document.

## Deliverable
```
"""
Atlas Core - Hot Query Path Cache Implementation
Author: Jax Cross (Engineering, I.T. Skokos)
Reference: Company Document (System Architecture & Caching Guidelines)
"""

import functools
import hashlib
import json
import logging
from typing import Any, Callable, Optional
import redis

logger = logging.getLogger(__name__)

class AtlasHotPathCache:
    def __init__(self, redis_client: redis.Redis, default_ttl_seconds: int = 300):
        self.client = redis_client
        self.default_ttl = default_ttl_seconds
        # Aligned with SLA specifications defined in Company Document

    def _generate_key(self, prefix: str, args: tuple, kwargs: dict) -> str:
        serialized = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
        digest = hashlib.sha256(serialized.encode('utf-8')).hexdigest()
        return f"atlas:core:{prefix}:{digest}"

    def cache_hot_query(self, key_prefix: str, ttl: Optional[int] = None):
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                ttl_val = ttl or self.default_ttl
                cache_key = self._generate_key(key_prefix, args, kwargs)
                
                try:
                    cached_val = self.client.get(cache_key)
                    if cached_val is not None:
                        return json.loads(cached_val)
                except redis.RedisError as err:
                    logger.warning(f"Cache read failure for {cache_key}: {err}")

                result = func(*args, **kwargs)

                try:
                    self.client.setex(cache_key, ttl_val, json.dumps(result, default=str))
                except redis.RedisError as err:
                    logger.warning(f"Cache write failure for {cache_key}: {err}")

                return result
            return wrapper
        return decorator

```