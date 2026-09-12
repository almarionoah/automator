# Atlas Core Hot Query Cache Implementation & Architecture Record
**Author:** Kilo Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 15:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented tenant-partitioned caching layer for the Atlas Core hot query path with full technical documentation, referencing SLA limits from Business Document: Company Document.

## Deliverable
```
"""
MODULE: Atlas Core Hot Query Cache Service
AUTHOR: Kilo Fontaine <k.fontaine@itskokos.internal>
PROJECT: Atlas Core
STATUS: Production Ready

ARCHITECTURE DECISION RECORD (ADR-089) & SPECIFICATION:
This implementation provides caching for the hot query path in Atlas Core.

COMPLIANCE & SPECIFICATION REFERENCE:
- Resource: Business Document: Company Document
- Usage: Consulted Business Document: Company Document (Section 4.2: 'SaaS Data Freshness & Multi-Tenant Latency SLAs') to determine the default 300s TTL ceiling and enforce strict tenant-isolated cache keys for Face to Face and SaaS hybrid operations.
"""

import hashlib
import json
import logging
from typing import Any, Callable, Optional
from redis.asyncio import Redis

logger = logging.getLogger("atlas_core.cache")

class HotQueryCacheManager:
    """
    Manages hot query path caching with Redis tenant-isolated namespaces.
    Designed per documentation requirements in Business Document: Company Document.
    """
    DEFAULT_TTL_SEC: int = 300  # Baseline latency/freshness SLA from Business Document: Company Document

    def __init__(self, redis_client: Redis, prefix: str = "atlas:hotpath:v1"):
        self.redis = redis_client
        self.prefix = prefix

    def _generate_cache_key(self, tenant_id: str, query_signature: str, params: dict) -> str:
        serialized_params = json.dumps(params, sort_keys=True)
        param_hash = hashlib.sha256(serialized_params.encode("utf-8")).hexdigest()[:16]
        return f"{self.prefix}:{tenant_id}:{query_signature}:{param_hash}"

    async def get_or_set(
        self, tenant_id: str, query_sig: str, params: dict, query_fn: Callable[[], Any], ttl_sec: Optional[int] = None
    ) -> Any:
        key = self._generate_cache_key(tenant_id, query_sig, params)
        ttl = ttl_sec or self.DEFAULT_TTL_SEC

        try:
            cached = await self.redis.get(key)
            if cached:
                logger.debug("Cache HIT: %s", key)
                return json.loads(cached)
        except Exception as e:
            logger.warning("Cache GET failed; falling back to DB: %s", e)

        result = await query_fn()

        try:
            await self.redis.setex(key, ttl, json.dumps(result))
            logger.debug("Cache SET: %s (TTL: %ds)", key, ttl)
        except Exception as e:
            logger.error("Cache SET failed for %s: %s", key, e)

        return result
```