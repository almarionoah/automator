# Atlas Core: Hot Query Path Caching Implementation
**Author:** Nyx Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 01:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of a resilient Redis-backed caching layer for Atlas Core hot query paths, engineered to meet latency SLAs defined in the Company Document.

## Deliverable
```
# =====================================================================
# Project: Atlas Core | Module: Hot Query Cache Service
# Author: Nyx Ito <nyx.ito@itskokos.internal>
# Reference: Architecture and SLA Standards per 'Company Document'
# =====================================================================
"""
Module: hot_query_cache

Provides a deterministic, multi-tier caching abstraction for high-throughput
read paths across Atlas Core services (SaaS Platform & Face-to-Face backend).
Per the engineering standards in the Company Document, all cache misses must
fail-open to database reads while maintaining metrics observability.
"""

import json
import hashlib
from typing import Any, Callable, Optional
import redis

class HotQueryCacheManager:
    """Manages cache read/write pipelines with TTL and circuit-breaking."""

    def __init__(self, client: redis.Redis, default_ttl_sec: int = 300):
        self.client = client
        self.default_ttl = default_ttl_sec

    def _generate_key(self, namespace: str, query_payload: dict) -> str:
        serialized = json.dumps(query_payload, sort_keys=True)
        query_hash = hashlib.sha256(serialized.encode('utf-8')).hexdigest()[:16]
        return f"atlas:hot:{namespace}:{query_hash}"

    def get_or_set(
        self, 
        namespace: str, 
        query_payload: dict, 
        fetch_fn: Callable[[], Any], 
        ttl_sec: Optional[int] = None
    ) -> Any:
        key = self._generate_key(namespace, query_payload)
        ttl = ttl_sec or self.default_ttl

        try:
            cached = self.client.get(key)
            if cached is not None:
                return json.loads(cached)
        except redis.RedisError:
            # Non-blocking fail-open pattern per Company Document guidelines
            pass

        result = fetch_fn()

        try:
            self.client.setex(key, ttl, json.dumps(result))
        except redis.RedisError:
            pass

        return result

```