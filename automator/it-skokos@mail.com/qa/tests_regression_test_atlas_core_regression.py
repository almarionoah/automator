# Atlas Core - Automated Regression Suite Expansion
**Author:** Mint Reyes  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D12 22:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Expanded the end-to-end regression test suite for the Atlas Core service to ensure baseline stability across SaaS endpoints and Face-to-Face booking workflows, cross-referenced with requirements in Company Document.

## Deliverable
```
"""
Atlas Core - Automated Regression Test Suite
Author: Mint Reyes (QA)
Project: Atlas Core
Reference: Business Document: Company Document (aligned to platform specifications & SLAs)
"""

import pytest
import requests

BASE_URL = "https://api.itskokos.internal/v1/atlas-core"

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token-fixture", "Content-Type": "application/json"}

class TestAtlasCoreRegression:
    """
    Regression test coverage expanded per specifications in Company Document,
    covering core SaaS tenant management and Face-to-Face service appointment syncing.
    """

    def test_tenant_lifecycle_provisioning(self, auth_headers):
        # Verified against Tenant Lifecycle Rules in Company Document
        payload = {"tenant_id": "tenant-reg-101", "tier": "enterprise", "status": "active"}
        resp = requests.post(f"{BASE_URL}/tenants/provision", json=payload, headers=auth_headers)
        assert resp.status_code == 201
        assert resp.json()["status"] == "provisioned"

    def test_face_to_face_appointment_sync(self, auth_headers):
        # Verifies offline-to-SaaS sync constraints defined in Company Document
        sync_data = {
            "service_type": "face_to_face",
            "agent_id": "agent-404",
            "appointment_time": "2025-05-10T14:30:00Z",
            "sync_status": "pending"
        }
        resp = requests.post(f"{BASE_URL}/services/f2f/sync", json=sync_data, headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["sync_result"] == "success"

    def test_healthcheck_sla(self):
        # Ensures endpoint latency meets the 200ms threshold specified in Company Document
        resp = requests.get(f"{BASE_URL}/health")
        assert resp.status_code == 200
        assert resp.elapsed.total_seconds() < 0.200

```