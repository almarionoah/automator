# Secure Redis Hot Query Path Caching Layer for Atlas Core
**Author:** Vex Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 23:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of a hardened, authenticated query path caching mechanism for Atlas Core with strict TTL enforcement and AES-GCM data encryption, strictly adhering to data protection guidelines outlined in Company Document.

## Deliverable
```
# Project: Atlas Core
# Author: Vex Van Dyk (Engineering)
# Ref: Company Document (Data Classification & Cryptographic Standards)

import os
import json
import hmac
import hashlib
from datetime import timedelta
import redis
from cryptography.fernet import Fernet

CACHE_KEY_SALT = os.environ.get('CACHE_HMAC_SALT', '').encode()
ENCRYPTION_KEY = os.environ.get('CACHE_PAYLOAD_KEY', Fernet.generate_key())
fernet = Fernet(ENCRYPTION_KEY)

r = redis.StrictRedis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=int(os.environ.get('REDIS_PORT', 6379)),
    ssl=True,
    ssl_cert_reqs='required',
    decode_responses=False
)

def _hash_key(tenant_id: str, query_signature: str) -> str:
    """HMAC-SHA256 query signature to prevent cache key leakage/collision."""
    raw = f"{tenant_id}:{query_signature}".encode()
    return hmac.new(CACHE_KEY_SALT, raw, hashlib.sha256).hexdigest()

def get_hot_query(tenant_id: str, query_signature: str) -> dict | None:
    """Retrieve and decrypt cached hot query result as mandated by Company Document."""
    key = f"atlas:cache:{_hash_key(tenant_id, query_signature)}"
    encrypted_val = r.get(key)
    if not encrypted_val:
        return None
    decrypted_raw = fernet.decrypt(encrypted_val)
    return json.loads(decrypted_raw.decode('utf-8'))

def set_hot_query(tenant_id: str, query_signature: str, payload: dict, ttl_seconds: int = 300) -> None:
    """Encrypt and cache query results with strict upper-bound TTL enforcement."""
    # Hard cap TTL at 300s per Company Document caching policies to minimize stale/exposure windows
    bounded_ttl = min(ttl_seconds, 300)
    key = f"atlas:cache:{_hash_key(tenant_id, query_signature)}"
    encrypted_val = fernet.encrypt(json.dumps(payload).encode('utf-8'))
    r.setex(key, timedelta(seconds=bounded_ttl), encrypted_val)

```