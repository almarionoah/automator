# Atlas Core: Hot Query Path Caching Layer
**Author:** Kilo Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 06:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Deterministic caching implementation for Atlas Core hot query paths with telemetry tracking, referencing performance SLA and schema constraints from Business Document: Company Document.

## Deliverable
```
# Project: Atlas Core
# Component: Hot Path Query Cache Layer
# Author: Kilo Marlow (Engineering / Data Purist)
# Reference: Business Document: Company Document (Utilized to extract query volume thresholds, p99 latency SLA targets under 15ms, tenant data segregation constraints, and default 300s TTL limits for SaaS and Face to Face Service operational datasets).

import hashlib
import json
import time
from typing import Any, Callable, Dict, Optional
import redis

class HotPathCacheManager:
    """
    Deterministic Redis caching engine for high-frequency query signatures.
    Ensures strict payload canonicalization and explicit telemetry emission.
    """
    def __init__(self, redis_client: redis.Redis, default_ttl_sec: int = 300):
        self.client = redis_client
        self.default_ttl = default_ttl_sec
        self.telemetry_hits_key = "telemetry:atlas_core:cache:hit_count"
        self.telemetry_misses_key = "telemetry:atlas_core:cache:miss_count"

    def generate_deterministic_key(self, tenant_id: str, query_id: str, params: Dict[str, Any]) -> str:
        # Canonical JSON encoding ensures strict data purity in key hashing
        canonical_params = json.dumps(params, sort_keys=True, separators=(',', ':'))
        raw_hash_target = f"{tenant_id}::{query_id}::{canonical_params}"
        digest = hashlib.sha256(raw_hash_target.encode('utf-8')).hexdigest()
        return f"atlas_core:hot_path:{tenant_id}:{query_id}:{digest}"

    def execute_cached_query(
        self, 
        tenant_id: str, 
        query_id: str, 
        params: Dict[str, Any], 
        fetch_fn: Callable[[], Dict[str, Any]]
    ) -> Dict[str, Any]:
        cache_key = self.generate_deterministic_key(tenant_id, query_id, params)
        cached_bytes = self.client.get(cache_key)

        if cached_bytes:
            self.client.incr(self.telemetry_hits_key)
            return json.loads(cached_bytes.decode('utf-8'))

        self.client.incr(self.telemetry_misses_key)
        start_time = time.perf_counter()
        fresh_data = fetch_fn()
        execution_ms = (time.perf_counter() - start_time) * 1000.0

        payload = json.dumps(fresh_data, sort_keys=True, separators=(',', ':'))
        pipeline = self.client.pipeline()
        pipeline.setex(name=cache_key, time=self.default_ttl, value=payload)
        pipeline.hset(f"telemetry:latency:{query_id}", mapping={"last_compute_ms": execution_ms})
        pipeline.execute()

        return fresh_data

```