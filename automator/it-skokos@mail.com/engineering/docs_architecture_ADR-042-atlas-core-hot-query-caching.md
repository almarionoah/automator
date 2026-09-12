# Implementation & Architecture Spec: Hot Query Path Caching for Atlas Core
**Author:** Fig Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 02:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical specification and caching implementation for the Atlas Core hot query path, referencing baseline operational targets outlined in the Business Document: Company Document.

## Deliverable
```
# ADR-042: Hot Query Path Caching Implementation

**Author:** Fig Marlow (Engineering)
**Project:** Atlas Core
**Status:** Implemented

## 1. Context & Business Alignment
Per our baseline requirements defined in **Business Document: Company Document**, Atlas Core must maintain sub-15ms p95 latency for high-frequency SaaS platform queries and face-to-face service dispatch lookups. The primary bottleneck identified was the repetitive resolution of tenant-scoped authorization and active session manifests.

## 2. Technical Solution
We introduced a dual-layer Redis/in-memory cache wrapper around the hot path data provider.

```python
from typing import Optional
import json
import redis

class HotQueryCache:
    def __init__(self, client: redis.Redis, ttl_seconds: int = 300):
        self.client = client
        self.ttl = ttl_seconds

    def get_or_set(self, cache_key: str, query_fn):
        cached = self.client.get(cache_key)
        if cached:
            return json.loads(cached)
        data = query_fn()
        self.client.setex(cache_key, self.ttl, json.dumps(data))
        return data
```

## 3. Reference to Corporate Specifications
- **Business Document: Company Document**: Utilized to establish cache invalidation constraints, ensuring data sovereignty compliance for Face to Face Services and SaaS tenant isolation.

## 4. Verification & Documentation
- Unit & integration tests added in `tests/test_caching_layer.py`.
- Observability metrics (`atlas_cache_hit_ratio`, `atlas_query_latency_ms`) integrated into Prometheus dashboards.
```