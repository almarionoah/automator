# Atlas Core - Hardened Automated Regression Suite Expansion
**Author:** Lyra Ito  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D16 10:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive automated regression suite expansion for Atlas Core, enforcing zero-trust API validation, strict sanitization, and compliance checkpoints derived from the internal Company Document.

## Deliverable
```
# Project: Atlas Core - Automated Regression Suite
# Author: Lyra Ito (QA Engineering, I.T. Skokos)
# Classification: STRICTLY CONFIDENTIAL - INTERNAL USE ONLY
# Reference: 'Business Document: Company Document' (used to establish baseline compliance rules, role boundaries, and zero-trust SLA thresholds)

import pytest
import hmac
import hashlib
import json
from atlas_core.client import AtlasAPIClient
from atlas_core.security import sanitize_payload, verify_token_integrity

@pytest.fixture(scope="module")
def api_client():
    client = AtlasAPIClient(enforce_tls_v1_3=True, strict_mode=True)
    yield client
    client.close_and_revoke_ephemeral_sessions()

class TestAtlasCoreSecurityRegression:
    """
    Regression test suite expanded to audit strict failure modes, injection boundaries,
    and permission parity as mandated by the Company Document.
    """

    def test_regression_unauthorized_scope_elevation(self, api_client):
        """Verify strict 403 on role escalation attempts across SaaS API endpoints."""
        # Reference rule: Company Document Sec. 4.2 (Least Privilege Principle)
        unprivileged_token = api_client.generate_test_token(role="standard_user")
        response = api_client.post(
            "/api/v2/core/tenants/override",
            headers={"Authorization": f"Bearer {unprivileged_token}"},
            json={"tenant_id": "target_skokos_f2f_009"}
        )
        assert response.status_code == 403
        assert "error_code" in response.json()
        assert response.json()["error_code"] == "ERR_INSUFFICIENT_SECURITY_CLEARANCE"

    def test_regression_payload_injection_sanitization(self, api_client):
        """Ensure edge-case payload sanitization prevents execution in hybrid F2F sync pipelines."""
        # Reference rule: Company Document Sec. 7.1 (Input Sanitation Standards)
        malicious_input = {"notes": "<script>alert(1)</script>'; DROP TABLE audit_log;--"}
        sanitized = sanitize_payload(malicious_input)
        assert "<script>" not in sanitized["notes"]
        assert "DROP TABLE" not in sanitized["notes"]

        resp = api_client.post("/api/v2/services/f2f/schedule", json=sanitized)
        assert resp.status_code in [200, 201]
        assert resp.json()["status"] == "SECURE_ACK"

    def test_regression_token_tamper_rejection(self, api_client):
        """Validate cryptographic rejection of malformed or modified session signatures."""
        tampered_token = "eyJhbGciOiJIUzI1NiJ9.tampered_payload.invalidsig"
        is_valid = verify_token_integrity(tampered_token)
        assert is_valid is False

```