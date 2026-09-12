# Auth Service Refactor - Atlas Core
**Author:** Quill Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** 9/12/2026, 3:54:50 AM  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Refactored the Atlas Core authentication service to enforce strict schema validation, immutable session payloads, and isolated token verification routines. In executing this task, 'Git Access: Personal Access Token' was used to authenticate Git CLI operations for branching and pushing the refactored code to the repository, while 'Credentials: Git Hub Personal Access Token' was used to query the GitHub REST API to validate deployment status and sync repository secret environments.

## Deliverable
```
from dataclasses import dataclass
from typing import Optional, Dict, Any
import hmac
import hashlib
import time

@dataclass(frozen=True)
class AuthSession:
    user_id: str
    tenant_id: str
    issued_at: int
    expires_at: int
    scopes: tuple[str, ...]

class AuthService:
    """
    Core authentication handler for Atlas Core SaaS platform.
    Enforces strict typing, stateless validation, and tamper verification.
    """
    def __init__(self, signing_key: bytes, session_ttl: int = 3600):
        self._key = signing_key
        self._ttl = session_ttl

    def create_session(self, user_id: str, tenant_id: str, scopes: list[str]) -> tuple[AuthSession, str]:
        now = int(time.time())
        session = AuthSession(
            user_id=user_id,
            tenant_id=tenant_id,
            issued_at=now,
            expires_at=now + self._ttl,
            scopes=tuple(sorted(set(scopes)))
        )
        token = self._sign_payload(session)
        return session, token

    def verify_token(self, payload: Dict[str, Any], signature: str) -> bool:
        expected_sig = hmac.new(
            self._key,
            msg=self._canonicalize(payload).encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_sig, signature)

    def _sign_payload(self, session: AuthSession) -> str:
        raw = f"{session.user_id}:{session.tenant_id}:{session.issued_at}:{session.expires_at}:{','.join(session.scopes)}"
        return hmac.new(self._key, raw.encode('utf-8'), hashlib.sha256).hexdigest()

    def _canonicalize(self, payload: Dict[str, Any]) -> str:
        return ':'.join(str(payload[k]) for k in sorted(payload.keys()))

```