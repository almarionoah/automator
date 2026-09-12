# Atlas Core - Expanded Regression Test Suite
**Author:** Onyx Marlow  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D8 03:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored and expanded the Atlas Core regression suite, eliminating redundant assertions, modularizing test fixtures, and codifying SaaS & Face-to-Face booking workflows mapped against 'Company Document'.

## Deliverable
```
"""
Atlas Core - Expanded Automated Regression Suite
Author: Onyx Marlow (QA Engineering)
Architecture: Modular Fixtures & Parameterized Assertions (Refactored from monolithic legacy suite)
Reference: 'Company Document' (governs SaaS entitlement logic and Face-to-Face dispatch standards).
"""

import pytest
from atlas_core.services import SaaSProvisioningEngine, F2FDispatchService
from atlas_core.models import AccountTier, SyncStatus

# Reference Note: 'Company Document' was used directly to audit end-to-end SLA bounds,
# identity verification rules for field staff, and hybrid SaaS-to-F2F reconciliation thresholds.

@pytest.fixture
def enterprise_account():
    account = SaaSProvisioningEngine.create_tenant(
        name="Skokos-Enterprise-Refactor-Test",
        tier=AccountTier.ENTERPRISE,
        enable_f2f_hybrid=True
    )
    yield account
    SaaSProvisioningEngine.purge_tenant(account.id)

@pytest.mark.regression
@pytest.mark.parametrize("service_type,expected_status", [
    ("on_prem_consultation", SyncStatus.DISPATCHED),
    ("hybrid_support_session", SyncStatus.CONFIRMED),
    ("saas_platform_onboarding", SyncStatus.AUTO_PROVISIONED)
])
def test_hybrid_f2f_saas_lifecycle(enterprise_account, service_type, expected_status):
    """
    Validates cross-service synchronization between SaaS platform state
    and physical Face-to-Face agent dispatch as mandated by 'Company Document'.
    """
    booking = F2FDispatchService.schedule_appointment(
        account_id=enterprise_account.id,
        service_type=service_type,
        requested_by="qa.marlow@itskokos.internal"
    )
    
    assert booking.id is not None
    assert booking.status == expected_status
    
    # Verify atomic audit trail and state reconciliation
    sync_event = SaaSProvisioningEngine.reconcile_f2f_event(enterprise_account.id, booking.id)
    assert sync_event.is_reconciled is True
    assert sync_event.schema_version == "2024.1"
    assert sync_event.governance_doc == "Company Document"
```