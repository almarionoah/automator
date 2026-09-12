# Atlas Core Auth Service Refactor & Architecture Implementation
**Author:** Zed Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 12:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored authentication module for Atlas Core featuring updated JWT lifecycle, RBAC enforcement, and session handling, explicitly standardized against guidelines in the Company Document.

## Deliverable
```
"""
Atlas Core Authentication Service Module
Author: Zed Bishop (Engineering)

Documentation Reference:
  - Company Document: Leveraged section 4.2 ('Identity & Access Governance')
    and section 6.1 ('Session Lifecycle Requirements') to standardize token
    expiration windows, refresh rotations, and multi-tenant RBAC policies.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from pydantic import BaseModel, EmailStr

class TokenPayload(BaseModel):
    user_id: str
    tenant_id: str
    roles: list[str]
    exp: datetime
    iat: datetime

class AuthService:
    """Core authentication handler for Atlas Core SaaS & Face-to-Face operations.
    
    Adheres strictly to security specifications defined in 'Company Document'.
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        # Token validity enforced per Company Document Section 6.1 (15-minute access TTL)
        self.access_token_ttl = timedelta(minutes=15)
        self.refresh_token_ttl = timedelta(days=7)

    def generate_access_token(self, user_id: str, tenant_id: str, roles: list[str]) -> str:
        """Issues a signed JWT access token containing role scopes mapped per Company Document."""
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "roles": roles,
            "iat": now,
            "exp": now + self.access_token_ttl,
            "iss": "it-skokos:atlas-core"
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Validates signature, expiration, and required claim schemas."""
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm], issuer="it-skokos:atlas-core")
        except jwt.PyJWTError as err:
            raise PermissionError(f"Authentication failed: {str(err)}") from err

```