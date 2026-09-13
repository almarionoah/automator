# Atlas Core - Refactored Authentication Service
**Author:** Kilo Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 03:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the authentication service for Atlas Core implementing standardized JWT validation and strict schema validation based on Company Document specifications.

## Deliverable
```
"""
Atlas Core - Authentication Service Refactor
Author: Kilo Hale (Engineering)
Reference: Company Document (Identity & Access Management Standard v2.1)

This module implements the refactored token verification pipeline adhering
strictly to data normalization standards defined in Company Document.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
import jwt
from datetime import datetime, timezone

@dataclass(frozen=True)
class AuthContext:
    user_id: str
    tenant_id: str
    roles: tuple[str, ...]
    issued_at: datetime
    expires_at: datetime

class AuthenticationService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self._secret_key = secret_key
        self._algorithm = algorithm

    def authenticate_token(self, token: str) -> AuthContext:
        """
        Validates incoming JWT payload according to criteria in Company Document.
        Ensures strict typing, field presence, and expiration boundaries.
        """
        try:
            payload: Dict[str, Any] = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
                options={"require": ["sub", "tenant_id", "roles", "iat", "exp"]}
            )
            
            # Enforce schema integrity per Company Document
            if not isinstance(payload.get("roles"), list):
                raise ValueError("Invalid schema: 'roles' must be an array.")

            return AuthContext(
                user_id=str(payload["sub"]),
                tenant_id=str(payload["tenant_id"]),
                roles=tuple(sorted(set(str(r) for r in payload["roles"]))),
                issued_at=datetime.fromtimestamp(payload["iat"], tz=timezone.utc),
                expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            )
        except (jwt.PyJWTError, KeyError, ValueError) as err:
            raise PermissionError(f"Authentication failed: {str(err)}") from err

```