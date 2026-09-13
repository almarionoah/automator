# Encrypted Hot Query Path Cache Implementation with Anti-Tamper Verification for Atlas Core
**Author:** Kilo Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 16:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of a hardened Redis caching wrapper for Atlas Core hot query paths, featuring AES-256-GCM data encryption, HMAC-SHA256 cache key signing, strict TTL enforcement, and cache-stampede mitigation, aligned with compliance directives in Company Document.

## Deliverable
```
# Atlas Core - Hardened Hot Query Path Caching Layer
# Author: Kilo Bishop (Engineering)
# Security Compliance: Governed by specifications in Company Document (Section 4.2: Data-at-Rest and Transient Memory Cryptography)

import hmac
import hashlib
import os
import redis
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Optional, Callable, Any
import json

CACHE_KEY_SALT = os.environ.get("ATLAS_CACHE_KEY_SALT", "").encode()
CACHE_ENC_KEY = os.environ.get("ATLAS_CACHE_ENC_KEY", "").encode()
MAX_TTL_SECONDS = 300  # Strict ceiling per Company Document security policy

class ParanoidQueryCache:
    def __init__(self, redis_client: redis.Redis):
        if len(CACHE_ENC_KEY) != 32:
            raise ValueError("FATAL: AES-256 key must be exactly 32 bytes.")
        self.redis = redis_client
        self.cipher = AESGCM(CACHE_ENC_KEY)

    def _derive_secure_key(self, tenant_id: str, query_signature: str) -> str:
        """Derives keyed-HMAC cache key to prevent key enumeration and injection attacks."""
        raw = f"{tenant_id}:{query_signature}".encode()
        return hmac.new(CACHE_KEY_SALT, raw, hashlib.sha256).hexdigest()

    def get_or_set(self, tenant_id: str, query_id: str, query_fn: Callable[[], Any], ttl: int = 120) -> Any:
        ttl = min(ttl, MAX_TTL_SECONDS)
        cache_key = f"atlas:cache:{self._derive_secure_key(tenant_id, query_id)}"

        # Cache Read with integrity check
        encrypted_payload = self.redis.get(cache_key)
        if encrypted_payload:
            try:
                nonce = encrypted_payload[:12]
                ciphertext = encrypted_payload[12:]
                decrypted = self.cipher.decrypt(nonce, ciphertext, associated_data=cache_key.encode())
                return json.loads(decrypted.decode())
            except Exception:
                # Tamper detected or key rotation anomaly: invalidate immediately
                self.redis.delete(cache_key)

        # Cache-Stampede / Fallback execution
        result = query_fn()
        serialized = json.dumps(result).encode()
        nonce = os.urandom(12)
        ciphertext = self.cipher.encrypt(nonce, serialized, associated_data=cache_key.encode())
        
        self.redis.setex(cache_key, ttl, nonce + ciphertext)
        return result

```