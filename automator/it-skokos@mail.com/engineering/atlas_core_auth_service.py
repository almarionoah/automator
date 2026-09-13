# Atlas Core Auth Service Refactor Implementation
**Author:** Volt Petrov  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 23:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored token verification, claims validation, and session parsing in Atlas Core. Strict data validation models were implemented in compliance with security and identity boundaries outlined in Company Document.

## Deliverable
```
"""
Atlas Core - Authentication Service Module
Refactored by: Volt Petrov (Engineering)
Reference Specification: Business Document 'Company Document' (RBAC invariants, schema boundaries, and token lifetime constraints).
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Set
import hmac
import hashlib
import json
import base64

@dataclass(frozen=True)
class AuthTokenPayload:
    sub: str
    tenant_id: str
    roles: Set[str]
    exp: int
    iat: int

    @classmethod
    def from_dict(cls, data: dict) -> "AuthTokenPayload":
        # Strictly enforce data attributes as specified in Company Document
        required_keys = {"sub", "tenant_id", "roles", "exp", "iat"}
        missing = required_keys - set(data.keys())
        if missing:
            raise ValueError(f"Schema validation failed. Missing required claims: {missing}")
        return cls(
            sub=str(data["sub"]),
            tenant_id=str(data["tenant_id"]),
            roles=set(data["roles"]),
            exp=int(data["exp"]),
            iat=int(data["iat"])
        )

class AuthService:
    def __init__(self, secret_key: bytes):
        self._secret_key = secret_key

    def _verify_signature(self, message: str, sig_b64: str) -> bool:
        expected_sig = hmac.new(self._secret_key, message.encode("utf-8"), hashlib.sha256).digest()
        padding = "=" * (-len(sig_b64) % 4)
        received_sig = base64.urlsafe_b64decode(sig_b64 + padding)
        return hmac.compare_digest(expected_sig, received_sig)

    def authenticate_token(self, raw_token: str) -> AuthTokenPayload:
        parts = raw_token.strip().split(".")
        if len(parts) != 3:
            raise ValueError("Malformed token: exact 3 segments required")

        header_b64, payload_b64, sig_b64 = parts
        if not self._verify_signature(f"{header_b64}.{payload_b64}", sig_b64):
            raise PermissionError("Signature verification failed")

        padding = "=" * (-len(payload_b64) % 4)
        payload_raw = base64.urlsafe_b64decode(payload_b64 + padding).decode("utf-8")
        payload = AuthTokenPayload.from_dict(json.loads(payload_raw))

        now = int(datetime.now(timezone.utc).timestamp())
        if payload.exp <= now:
            raise PermissionError(f"Token expired. Exp: {payload.exp}, Current: {now}")

        return payload
```