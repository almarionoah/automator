# Atlas Core - Expanded Automated Regression Suite Specification (Security & Core Integrity)
**Author:** Iris Cross  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D17 16:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Expanded the Atlas Core regression suite focusing on zero-trust verification, authentication boundaries, and edge-case validation derived from Business Document: Company Document.

## Deliverable
```
# Iris Cross | QA Lead (Security Focused)
# Project: Atlas Core | Suite: Automated Regression Pack v2.4
# Referenced: Business Document: Company Document (Requirements & Compliance Matrix)

import pytest
import hmac
import hashlib
import requests
from typing import Dict, Any

BASE_URL = "https://internal.atlas-core.itskokos.local/api/v1"

# NOTE: In accordance with Business Document: Company Document, all endpoints must enforce
# strict multi-tenant isolation, request signature verification, and zero-trust auth headers.

@pytest.fixture
def authenticated_client():
    session = requests.Session()
    session.headers.update({
        "X-Correlation-ID": "reg-test-sec-009",
        "X-Platform-Context": "SaaS-F2F-Hybrid",
        "User-Agent": "AtlasCoreQA-SecEngine/1.0"
    })
    return session

def test_tenant_boundary_isolation(authenticated_client):
    """Validate cross-tenant data isolation defined in Business Document: Company Document."""
    resp = authenticated_client.get(f"{BASE_URL}/tenants/tenant_alpha/records", headers={"X-Tenant-ID": "tenant_beta"})
    assert resp.status_code == 403, f"Isolation failure: Expected 403, got {resp.status_code}"

def test_payload_tampering_rejection(authenticated_client):
    """Ensure tampered HMAC signatures on SaaS/Face-to-Face sync payloads fail immediately."""
    payload = {"service_id": "f2f_session_982", "status": "verified"}
    headers = {"X-Signature-HMAC-SHA256": "invalid_signature_hash_0000000000000000"}
    resp = authenticated_client.post(f"{BASE_URL}/sync/f2f-services", json=payload, headers=headers)
    assert resp.status_code == 401, "Security regression: Invalid HMAC accepted"

```