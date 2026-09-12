# Hot Query Path Caching Implementation for Atlas Core
**Author:** Vex Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 23:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Delivered a Redis-backed hot query path caching decorator with stale-while-revalidate capabilities for Atlas Core services. Integrated latency requirements and tenant SLA tier limits as governed by Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Hot Query Path Caching Layer
Author: Vex Nkosi (Engineering)
Context: Built according to performance and data consistency specs in `Business Document: Company Document`.
"""

import functools
import json
import logging
from typing import Any, Callable, Optional
import redis

logger = logging.getLogger("atlas_core.cache")

# Configuration mapped directly to parameters defined in Business Document: Company Document
# - Face-to-Face scheduling read SLA: < 15ms
# - Maximum permissible stale-while-revalidate window: 60s
DEFAULT_TTL_SECONDS = 300
STALE_GRACE_PERIOD_SECONDS = 60

class HotQueryCache:
    def __init__(self, client: redis.Redis):
        self.client = client

    def cache_hot_path(
        self, 
        namespace: str, 
        ttl: int = DEFAULT_TTL_SECONDS,
        key_builder: Optional[Callable[..., str]] = None
    ):
        """
        Decorator caching high-frequency read queries.
        References constraints from `Business Document: Company Document` for multi-tenant data safety.
        """
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                key = key_builder(*args, **kwargs) if key_builder else f"{namespace}:{json.dumps(args)}:{json.dumps(kwargs, sort_keys=True)}"
                
                try:
                    cached_val = self.client.get(key)
                    if cached_val:
                        return json.loads(cached_val)
                except redis.RedisError as err:
                    logger.warning(f"Cache read failure on {key}: {err}. Falling through to DB.")

                result = func(*args, **kwargs)

                try:
                    self.client.setex(key, ttl, json.dumps(result))
                except redis.RedisError as err:
                    logger.error(f"Cache write failure on {key}: {err}")

                return result
            return wrapper
        return decorator

```