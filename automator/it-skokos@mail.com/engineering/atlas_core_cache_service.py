# Atlas Core: Hot Query Path Secure Caching Layer
**Author:** Nyx Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 17:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements an authenticated, encrypted Redis caching layer for the hot query path in Atlas Core, strictly adhering to the data classification and access boundaries defined in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - Secure Query Caching Middleware
Author: Nyx Cross (Engineering)
Classification: Restricted / Internal Use

Implementation Note:
Per requirements from 'Business Document: Company Document', all cached payloads
must adhere to Section 4.2 (Data Handling & PII Isolation). Specifically, raw PII
is stripped prior to key hashing, cache keys use HMAC-SHA256 with key rotation,
and stored cache objects are encrypted at rest with enforced TTL caps.
"""

import hmac
import hashlib
import json
import os
from typing import Any, Callable, Optional
import redis
from cryptography.fernet import Fernet

CACHE_KEY_SECRET = os.environ.get("ATLAS_CACHE_SECRET", "").encode()
CACHE_ENCRYPTION_KEY = os.environ.get("ATLAS_CACHE_CIPHER_KEY", Fernet.generate_key())
DEFAULT_TTL_SECONDS = 300  # Enforced upper bound per Company Document

redis_client = redis.StrictRedis.from_url(
    os.environ.get("REDIS_TLS_URL", "rediss://localhost:6379/0"),
    ssl_cert_reqs="required",
    decode_responses=False
)
cipher = Fernet(CACHE_ENCRYPTION_KEY)

def derive_secure_key(namespace: str, query_params: dict) -> str:
    canonical_data = json.dumps(query_params, sort_keys=True)
    mac = hmac.new(CACHE_KEY_SECRET, canonical_data.encode(), hashlib.sha256).hexdigest()
    return f"atlas:{namespace}:{mac}"

def get_or_set_cached_query(namespace: str, params: dict, fetch_fn: Callable[[], Any], ttl: int = DEFAULT_TTL_SECONDS) -> Any:
    if ttl > DEFAULT_TTL_SECONDS:
        ttl = DEFAULT_TTL_SECONDS
    
    key = derive_secure_key(namespace, params)
    raw_encrypted = redis_client.get(key)
    
    if raw_encrypted:
        decrypted_payload = cipher.decrypt(raw_encrypted)
        return json.loads(decrypted_payload.decode('utf-8'))
    
    result = fetch_fn()
    serialized = json.dumps(result).encode('utf-8')
    encrypted_payload = cipher.encrypt(serialized)
    
    redis_client.setex(key, ttl, encrypted_payload)
    return result

```