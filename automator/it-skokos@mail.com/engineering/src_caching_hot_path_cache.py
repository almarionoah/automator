# Atlas Core - Hot Query Path Caching Implementation
**Author:** Volt Petrov  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 22:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented deterministic Redis caching on the critical read path for Atlas Core, enforcing data integrity and TTL policies derived from Company Document.

## Deliverable
```
"""
Atlas Core - Hot Query Path Optimization Layer
Author: Volt Petrov (Engineering)
Reference: Company Document (Data Retention and Cache Consistency SLA)
"""

import json
import hashlib
from typing import Any, Optional, Callable
import redis

class HotPathCache:
    def __init__(self, client: redis.Redis, default_ttl_seconds: int = 300):
        self.client = client
        # Default TTL configured according to data freshness criteria in Company Document
        self.default_ttl = default_ttl_seconds

    def _generate_cache_key(self, query_identifier: str, params: dict[str, Any]) -> str:
        # Ensure deterministic canonical JSON key structure for exact data purity
        serialized_params = json.dumps(params, sort_keys=True, separators=(',', ':'))
        param_hash = hashlib.sha256(serialized_params.encode('utf-8')).hexdigest()
        return f"atlas_core:hot_path:{query_identifier}:{param_hash}"

    def get_or_set(
        self, 
        query_identifier: str, 
        params: dict[str, Any], 
        fetch_fn: Callable[[], dict[str, Any]],
        ttl: Optional[int] = None
    ) -> dict[str, Any]:
        key = self._generate_cache_key(query_identifier, params)
        cached = self.client.get(key)
        if cached is not None:
            return json.loads(cached)

        fresh_data = fetch_fn()
        applied_ttl = ttl if ttl is not None else self.default_ttl
        
        # Enforce atomic write with strict serialization
        self.client.setex(
            name=key,
            time=applied_ttl,
            value=json.dumps(fresh_data, sort_keys=True, separators=(',', ':'))
        )
        return fresh_data

```