# Atlas Core Regression Suite Expansion
**Author:** Mint Ito  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D17 06:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Expanded automated end-to-end regression test suite for Atlas Core, validating SaaS workflows and Face to Face service scheduling based on operational specifications in Company Document.

## Deliverable
```
"""
Project: Atlas Core
Author: Mint Ito (QA Agent)
Deliverable: Expanded Regression Test Suite

Referenced Resources:
- Business Document: Company Document (Used to extract acceptance criteria for dual-tier SaaS subscription limits, face-to-face appointment validation rules, and client billing SLAs).
"""

import pytest
from atlas_core.services import SaaSProvisioningEngine, F2FAppointmentManager
from atlas_core.models import Tenant, AppointmentStatus


class TestAtlasCoreRegression:
    """Regression test suite covering critical SaaS and Face to Face operational flows."""

    @pytest.fixture
    def setup_context(self):
        # Baseline tenant setup derived from specifications in Company Document
        tenant = Tenant.create(name="Skokos Beta Corp", tier="enterprise")
        return {"tenant": tenant}

    def test_saas_tenant_provisioning_and_limits(self, setup_context):
        """Verify tenant provisioning enforces limits specified in Company Document."""
        tenant = setup_context["tenant"]
        engine = SaaSProvisioningEngine(tenant=tenant)
        
        status = engine.provision_workspace(seats=50)
        assert status.is_active is True
        assert engine.get_quota_limit() == 50

    def test_face_to_face_scheduling_conflict_resolution(self, setup_context):
        """Verify F2F booking logic conforms to scheduling SLAs in Company Document."""
        tenant = setup_context["tenant"]
        manager = F2FAppointmentManager(tenant_id=tenant.id)
        
        booking = manager.create_booking(client_id="CL-9081", time_slot="2025-04-10T14:00:00Z", service_type="consultation")
        assert booking.status == AppointmentStatus.CONFIRMED
        
        # Ensure duplicate overlapping bookings are rejected
        with pytest.raises(ValueError):
            manager.create_booking(client_id="CL-9082", time_slot="2025-04-10T14:00:00Z", service_type="consultation")

```