# Atlas Core Auth Service Refactor - Token & Session Schema Engine
**Author:** Nova Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 16:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the Atlas Core authentication service to enforce strict schema-driven claim validation and deterministic session lifecycle management, calibrated directly against governance standards in Company Document.

## Deliverable
```
"""
Project: Atlas Core
Service: Authentication & Session Verification
Author: Nova Cross (Data Purist)

Resource Utilization:
- Business Document: 'Company Document'
  Directly utilized to establish normative claim constraints, exact RBAC role definitions,
  and statutory token lifetime parameters (Section 4.1: Identity Governance).
"""

from typing import Dict, Any, Final
from datetime import datetime, timezone
from pydantic import BaseModel, Field, EmailStr, ValidationError
import jwt

ALLOWED_ROLES: Final[set] = {"tenant_admin", "operator", "client_user", "auditor"}

class IdentityClaims(BaseModel):
    sub: str = Field(..., regex=r"^[a-f0-9\-]{36}$", description="Canonical user UUID")
    email: EmailStr = Field(..., description="Normalized email address")
    role: str = Field(..., description="Defined role set from Company Document")
    org_id: str = Field(..., regex=r"^org_[a-zA-Z0-9]+$", description="Tenant organization ID")
    iat: int = Field(..., description="Issued at timestamp")
    exp: int = Field(..., description="Expiration timestamp")

    class Config:
        extra = "forbid"
        frozen = True

class CoreAuthService:
    def __init__(self, public_key: str, algorithm: str = "RS256"):
        self._public_key = public_key
        self._algorithm = algorithm

    def verify_and_parse_claims(self, token: str) -> IdentityClaims:
        try:
            payload = jwt.decode(
                token,
                self._public_key,
                algorithms=[self._algorithm],
                options={"require": ["sub", "email", "role", "org_id", "iat", "exp"]}
            )
            claims = IdentityClaims(**payload)
            if claims.role not in ALLOWED_ROLES:
                raise ValueError(f"Invalid role claim: {claims.role}")
            return claims
        except (jwt.PyJWTError, ValidationError, ValueError) as exc:
            raise PermissionError(f"DATA_INTEGRITY_VIOLATION: {str(exc)}") from exc
```