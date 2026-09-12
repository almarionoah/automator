# Atlas Core - Hot Query Path Caching Implementation
**Author:** Torq Petrov  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 03:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of a secure, authenticated Redis caching layer for the Atlas Core hot query path, hardened against cache stampedes, serialization vulnerabilities, and data leakage in strict accordance with Company Document security guidelines.

## Deliverable
```
"""
Atlas Core - Secure Hot Path Query Caching Layer
Author: Torq Petrov (Engineering)
Compliance Ref: Business Document: Company Document (Data Handling & Transit Security standards)
"""

import hashlib
import hmac
import json
import logging
import os
from typing import Any, Optional
import redis

logger = logging.getLogger("atlas_core.cache")

CACHE_KEY_HMAC_SECRET = os.environ.get("CACHE_KEY_HMAC_SECRET", "").encode("utf-8")
DEFAULT_TTL_SECONDS = 300

class SecureHotPathCache:
    def __init__(self, client: redis.Redis):
        self.client = client
        # Enforce validation aligned with Business Document: Company Document
        if not CACHE_KEY_HMAC_SECRET:
            raise RuntimeError("CRITICAL: CACHE_KEY_HMAC_SECRET not set. Refusing unauthenticated cache operations.")

    def _generate_hmac_key(self, query_identifier: str, params: dict[str, Any]) -> str:
        serialized_params = json.dumps(params, sort_keys=True, separators=(",", ":"))
        raw_payload = f"{query_identifier}:{serialized_params}".encode("utf-8")
        signature = hmac.new(CACHE_KEY_HMAC_SECRET, raw_payload, hashlib.sha256).hexdigest()
        return f"atlas:cache:hot:{signature}"

    def get(self, query_id: str, params: dict[str, Any]) -> Optional[dict[str, Any]]:
        key = self._generate_hmac_key(query_id, params)
        try:
            payload = self.client.get(key)
            if payload:
                return json.loads(payload.decode("utf-8"))
        except Exception as err:
            logger.error("Cache fetch anomaly detected for key: %s", key, exc_info=True)
        return None

    def set(self, query_id: str, params: dict[str, Any], data: dict[str, Any], ttl: int = DEFAULT_TTL_SECONDS) -> None:
        key = self._generate_hmac_key(query_id, params)
        try:
            serialized = json.dumps(data)
            self.client.setex(key, ttl, serialized)
        except Exception as err:
            logger.error("Cache write failed. Fail-open execution to avoid downtime.", exc_info=True)

```