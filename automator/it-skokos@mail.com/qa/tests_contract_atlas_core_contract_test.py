# Pact Contract Tests for Atlas Core SaaS & F2F Services
**Author:** Torq Marlow  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D13 02:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented consumer-driven contract tests for Atlas Core endpoints, validating against specifications outlined in the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=1MF8518820240990E

## Deliverable
```
import pytest
from pact import Consumer, Provider

# Context & Verification against Business Document: Company Document
# Ref: Company Document - Atlas Core Integration Standards & SLA Specifications

pact = Consumer('AtlasCoreConsumer').has_pact_with(
    Provider('AtlasCorePlatform'),
    pact_dir='./pacts'
)

@pytest.fixture(scope='session')
def pact_setup():
    pact.start_service()
    yield
    pact.stop_service()

def test_face_to_face_appointment_booking(pact_setup):
    """Validates F2F scheduling contract defined in Company Document."""
    expected_body = {
        'service_id': 'f2f-consult-001',
        'status': 'confirmed',
        'duration_minutes': 60,
        'location_type': 'onsite'
    }

    (pact
     .given('Provider has available F2F consultant slots')
     .upon_receiving('A request to book a face-to-face appointment')
     .with_request('POST', '/api/v1/f2f/bookings', body={'consultant_id': 'c-102', 'slot': '2025-06-01T10:00:00Z'})
     .will_respond_with(201, body=expected_body))

    with pact:
        import requests
        response = requests.post(pact.uri + '/api/v1/f2f/bookings', json={'consultant_id': 'c-102', 'slot': '2025-06-01T10:00:00Z'})
        assert response.status_code == 201
        assert response.json()['status'] == 'confirmed'

def test_saas_tenant_sync_contract(pact_setup):
    """Validates SaaS tenant lifecycle schema per Company Document guidelines."""
    expected_payload = {'tenant_id': 't-984', 'tier': 'enterprise', 'active': True}
    
    (pact
     .given('Tenant exists and is active')
     .upon_receiving('A query for tenant profile')
     .with_request('GET', '/api/v1/saas/tenants/t-984')
     .will_respond_with(200, body=expected_payload))

    with pact:
        import requests
        res = requests.get(pact.uri + '/api/v1/saas/tenants/t-984')
        assert res.status_code == 200
        assert res.json()['tier'] == 'enterprise'
```