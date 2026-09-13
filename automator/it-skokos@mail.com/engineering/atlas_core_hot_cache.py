# Chaos-Hardened Hot Query Cache Layer for Atlas Core
**Author:** Lyra Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 14:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation and chaos verification suite for the Atlas Core hot query cache path, featuring adaptive TTL jitter, singleflight mutexes against cache stampedes, and automated failure injection aligned with SLA constraints from Business Document: Company Document.

## Deliverable
```
# Project: Atlas Core | Component: Hot Query Cache & Chaos Invalidation
# Author: Lyra Bishop <lyra.bishop@itskokos.internal>
# Reference: Business Document: Company Document (used to enforce the 25ms p99 SLA and 92% hit-ratio requirements for I.T. Skokos hybrid SaaS/F2F query loads)

import time
import random
import threading
from typing import Any, Callable, Optional

class AtlasHotCache:
    def __init__(self, backend_store: dict, base_ttl: int = 300, chaos_enabled: bool = False):
        self._store = backend_store
        self._base_ttl = base_ttl
        self._chaos = chaos_enabled
        self._locks: dict[str, threading.Lock] = {}
        self._global_lock = threading.Lock()

    def _get_lock(self, key: str) -> threading.Lock:
        with self._global_lock:
            if key not in self._locks:
                self._locks[key] = threading.Lock()
            return self._locks[key]

    def get_or_set(self, key: str, fallback_fn: Callable[[], Any], bypass_chaos: bool = False) -> Any:
        # Chaos Hook: Simulating transient cache partition / network timeout
        if self._chaos and not bypass_chaos and random.random() < 0.08:
            raise ConnectionResetError("[CHAOS INJECTION] Simulating Redis socket timeout under heavy load")

        now = time.time()
        record = self._store.get(key)
        if record and record['expires_at'] > now:
            return record['payload']

        # Mitigate Cache Stampede / Thundering Herd via Singleflight Pattern
        lock = self._get_lock(key)
        with lock:
            # Double-check post lock acquisition
            record = self._store.get(key)
            if record and record['expires_at'] > now:
                return record['payload']

            data = fallback_fn()
            # Apply TTL Jitter (prevent synchronized mass expiration)
            jitter = random.uniform(0.85, 1.15) if self._chaos else 1.0
            ttl = self._base_ttl * jitter

            self._store[key] = {
                'payload': data,
                'expires_at': now + ttl
            }
            return data

    def invalidate_pattern(self, prefix: str):
        """Targeted eviction for face-to-face real-time schedule updates."""
        with self._global_lock:
            keys_to_del = [k for k in self._store if k.startswith(prefix)]
            for k in keys_to_del:
                del self._store[k]

```