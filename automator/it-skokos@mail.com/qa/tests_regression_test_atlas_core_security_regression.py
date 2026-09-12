# Expanded Security and Core Functional Regression Suite - Atlas Core
**Author:** Ash Ito  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D11 13:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Updated automated regression test suite covering authentication, authorization boundaries, and core pipeline integrity based on specifications in Company Document.

## Deliverable
```
"""
Atlas Core - Automated Regression Suite
Author: Ash Ito (QA Engineering, Security Paranoid)
Reference: Company Document (Business & Security Baseline Compliance)

Notes:
- Validated against access control matrix defined in 'Company Document'.
- Strict enforcement of zero-trust boundary verification and session token sanitization.
"""

import pytest
import hmac
import hashlib
from atlas_core.auth import TokenManager, SecurityContext
from atlas_core.api import AtlasClient

class TestAtlasCoreRegression:
    @pytest.fixture(autouse=True)
    def setup_context(self):
        # Enforce security baseline derived from Company Document
        self.client = AtlasClient(base_url="https://internal.skokos.local", enforce_tls=True)
        self.sec_context = SecurityContext(strict_mode=True)

    def test_regression_token_invalidation_replay_attack(self):
        """Verify terminated sessions cannot be replayed (Company Document Sec 4.1)."""
        token = self.sec_context.generate_ephemeral_token(user_id="sec_qa_user_99")
        resp = self.client.get("/v1/services/face-to-face/verify", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        
        # Invalidate
        self.sec_context.revoke_token(token)
        replayed_resp = self.client.get("/v1/services/face-to-face/verify", headers={"Authorization": f"Bearer {token}"})
        assert replayed_resp.status_code == 401, "CRITICAL: Revoked token allowed access!"

    def test_regression_payload_injection_sanitization(self):
        """Verify strict input filtering against payload injection on SaaS endpoints."""
        malformed_inputs = ["<script>alert(1)</script>", "' OR 1=1 --", "../../etc/shadow"]
        for payload in malformed_inputs:
            resp = self.client.post("/v1/atlas/pipeline/execute", json={"config_id": payload})
            assert resp.status_code in [400, 422], f"Payload leakage detected for input: {payload}"
            assert "stack" not in resp.text.lower(), "Internal stack trace exposed in response!"

```