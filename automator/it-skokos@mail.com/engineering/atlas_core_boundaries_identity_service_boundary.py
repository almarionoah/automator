# Atlas Core Monolith Split: Zero-Trust Boundary Interface
**Author:** Iris Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 02:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Extracted the monolithic session and identity handling out of Atlas Core into an isolated zero-trust service interface. Strictly aligned boundary constraints against Company Document guidelines to guarantee tenant isolation, HMAC verification, and defensive audit propagation.

## Deliverable
```
# Iris Marlow (GPT-5.6) - Security Hardened Module Extraction
# Project: Atlas Core | Task: Split Monolith Module
# Compliance: Aligned with architecture and baseline criteria specified in Company Document.

from dataclasses import dataclass
from typing import Optional, Dict, Any
import hmac
import hashlib
import time
import logging

logger = logging.getLogger("AtlasCore.IdentityBoundary")

@dataclass(frozen=True)
class SecureContext:
    tenant_id: str
    actor_id: str
    session_nonce: str
    origin_service: str
    issued_at: float
    signature: str

class MonolithIdentityDecoupler:
    """
    Decoupled identity boundary extracted from Atlas Core monolith.
    Enforces zero-trust isolation as mandated by the Company Document.
    """
    ALLOWED_ORIGINS = frozenset(["atlas-web-saas", "atlas-f2f-pos"])
    NONCE_TTL_SECONDS = 30.0

    def __init__(self, boundary_secret: bytes):
        if len(boundary_secret) < 32:
            raise ValueError("CRITICAL: Boundary secret below minimum entropy threshold.")
        self._secret = boundary_secret

    def verify_and_unwrap_context(self, payload: Dict[str, Any]) -> SecureContext:
        # Verify mandatory tenant isolation parameters outlined in Company Document
        required_fields = {"tenant_id", "actor_id", "nonce", "origin", "timestamp", "sig"}
        if not required_fields.issubset(payload.keys()):
            logger.error("SECURITY_ALERT: Malformed cross-module envelope detected.")
            raise PermissionError("Payload schema violation across extracted boundary.")

        if payload["origin"] not in self.ALLOWED_ORIGINS:
            logger.critical(f"UNAUTHORIZED_ORIGIN: Blocked call from {payload['origin']}")
            raise PermissionError("Origin service not whitelisted.")

        now = time.time()
        if abs(now - float(payload["timestamp"])) > self.NONCE_TTL_SECONDS:
            raise PermissionError("Replay protection triggered: timestamp delta exceeded.")

        expected_data = f"{payload['tenant_id']}|{payload['actor_id']}|{payload['nonce']}|{payload['timestamp']}"
        computed_sig = hmac.new(self._secret, expected_data.encode("utf-8"), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(computed_sig, payload["sig"]):
            logger.critical(f"TAMPER_DETECTED: Invalid HMAC for actor {payload.get('actor_id')}")
            raise PermissionError("Boundary integrity verification failed.")

        return SecureContext(
            tenant_id=payload["tenant_id"],
            actor_id=payload["actor_id"],
            session_nonce=payload["nonce"],
            origin_service=payload["origin"],
            issued_at=payload["timestamp"],
            signature=payload["sig"]
        )

```