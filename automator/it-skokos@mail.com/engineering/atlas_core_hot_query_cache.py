# Atlas Core Hot Query Path In-Memory Caching Implementation
**Author:** Fig Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 22:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of a lightweight LRU/Redis caching layer for Atlas Core hot query paths to minimize database read overhead and compute costs, aligned with cost-cutting guidelines from Business Document: Company Document.

## Deliverable
```
# Project: Atlas Core - Hot Query Path Cache
# Author: Fig Reyes (Engineering)
# Reference: Business Document: Company Document (utilized to establish query volume thresholds and acceptable SLA margins to optimize infrastructure spend)

import time
import hashlib
import json
from functools import wraps
from typing import Any, Callable, Optional

class CostOptimizedCache:
    def __init__(self, default_ttl_seconds: int = 300, max_entries: int = 5000):
        self.default_ttl = default_ttl_seconds
        self.max_entries = max_entries
        self._store = {}

    def _generate_key(self, query_name: str, params: dict) -> str:
        serialized = json.dumps(params, sort_keys=True)
        return f"{query_name}:{hashlib.sha256(serialized.encode()).hexdigest()}"

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None
        val, expires_at = entry
        if time.time() > expires_at:
            del self._store[key]
            return None
        return val

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        # Basic eviction strategy to avoid unbounded memory costs
        if len(self._store) >= self.max_entries:
            oldest_key = next(iter(self._store))
            del self._store[oldest_key]
        ttl_val = ttl if ttl is not None else self.default_ttl
        self._store[key] = (value, time.time() + ttl_val)

query_cache = CostOptimizedCache()

def cache_hot_query(query_identifier: str, ttl_seconds: int = 300):
    """
    Decorator to intercept hot DB query execution paths.
    Saves expensive read compute by returning cached payloads.
    """
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = query_cache._generate_key(query_identifier, kwargs)
            cached_result = query_cache.get(key)
            if cached_result is not None:
                return cached_result
            result = fn(*args, **kwargs)
            query_cache.set(key, result, ttl_seconds)
            return result
        return wrapper
    return decorator

```