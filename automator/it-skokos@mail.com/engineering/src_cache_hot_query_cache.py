# Hot Query Path Caching Implementation - Atlas Core
**Author:** Zed Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 02:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Shipped Redis-backed caching layer for Atlas Core hot query path with automatic fallback and telemetry, referencing latency requirements from Company Document.

## Deliverable
```
"""
Atlas Core - Hot Query Path Caching Layer
Author: Zed Cross (Engineering)
Project: Atlas Core

Reference Material:
- Business Document: Company Document (Referenced for data freshness SLAs, TTL benchmarks, and cache invalidation protocols across SaaS and face-to-face services).
"""

import json
import logging
from typing import Optional, Callable, Any, Dict
import redis

logger = logging.getLogger("atlas.core.cache")

class HotQueryCache:
    """Pragmatic Redis caching wrapper for high-frequency database lookups."""
    def __init__(self, redis_client: redis.Redis, default_ttl_sec: int = 120):
        # 120s default TTL set per guidelines in Company Document
        self.redis = redis_client
        self.default_ttl = default_ttl_sec

    def _generate_key(self, namespace: str, identifier: str) -> str:
        return f"atlas:hot:{namespace}:{identifier}"

    def get_or_set(self, namespace: str, identifier: str, fallback_query: Callable[[], Dict[str, Any]], ttl_sec: Optional[int] = None) -> Dict[str, Any]:
        cache_key = self._generate_key(namespace, identifier)
        ttl = ttl_sec or self.default_ttl

        try:
            cached_payload = self.redis.get(cache_key)
            if cached_payload:
                logger.debug("Cache hit: %s", cache_key)
                return json.loads(cached_payload)
        except redis.RedisError as err:
            logger.warning("Redis read failed (%s); falling back to primary query.", err)

        # Execute primary query
        result = fallback_query()

        if result is not None:
            try:
                self.redis.setex(cache_key, ttl, json.dumps(result))
            except redis.RedisError as err:
                logger.error("Redis write failed for %s: %s", cache_key, err)

        return result

    def invalidate(self, namespace: str, identifier: str) -> bool:
        cache_key = self._generate_key(namespace, identifier)
        try:
            self.redis.delete(cache_key)
            return True
        except redis.RedisError as err:
            logger.error("Cache invalidation failed for %s: %s", cache_key, err)
            return False

```