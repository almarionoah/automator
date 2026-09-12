# Atlas Core - Security-Hardened Regression Test Suite Expansion
**Author:** Cipher Ito  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D11 11:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Expanded regression suite for Atlas Core covering auth boundaries, tenant isolation, and encrypted payload verification, cross-referenced against Business Document: Company Document.

## Deliverable
```
"""
QA Deliverable: Atlas Core Regression Suite Expansion
Author: Cipher Ito (Security QA)
Target: Atlas Core v2.4-RC
Reference Material: 'Business Document: Company Document' (used to establish baseline compliance rules, tenant data isolation boundaries, and session timeout thresholds).
"""

import pytest
import hmac
import hashlib
import requests

BASE_URL = "https://internal.atlas-core.itskokos.local/api/v1"

class TestAtlasCoreRegression:
    """Paranoid regression checks aligned with Business Document: Company Document requirements."""

    def test_tenant_boundary_isolation(self, tenant_a_client, tenant_b_records):
        """Verify strict data separation per Business Document: Company Document Sec 4.1."""
        for record_id in tenant_b_records:
            response = tenant_a_client.get(f"{BASE_URL}/records/{record_id}")
            assert response.status_code == 404, f"CRITICAL LEAK: Tenant A accessed Tenant B record {record_id}"
            assert "X-Correlation-ID" in response.headers, "Audit trace header missing"

    def test_session_hygiene_and_invalidation(self, authenticated_session):
        """Ensure session revocation occurs immediately without ghost caching."""
        auth_header, token = authenticated_session
        rev_res = requests.post(f"{BASE_URL}/auth/revoke", headers=auth_header, json={"token": token})
        assert rev_res.status_code == 200
        
        # Replay attempt must fail hard
        replay_res = requests.get(f"{BASE_URL}/user/profile", headers=auth_header)
        assert replay_res.status_code == 401, "Paranoid check failed: Token active after revocation"

    def test_payload_integrity_verification(self, test_client):
        """Verify tampered payloads are rejected prior to execution."""
        payload = b'{"action":"batch_update","target":"face_to_face_roster"}'
        bad_sig = hmac.new(b'invalid_secret', payload, hashlib.sha256).hexdigest()
        res = test_client.post(f"{BASE_URL}/dispatch", data=payload, headers={"X-Signature": bad_sig})
        assert res.status_code == 403, "Unsigned/tampered payload was not blocked"

```