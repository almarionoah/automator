# Chaos-Driven Contract Test Suite for Atlas Core
**Author:** Fig Ito  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D16 21:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Delivered consumer-driven contract testing suite integrating chaos injection vectors for Atlas Core, referencing baseline API constraints from Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=2M371379B2196082W

## Deliverable
```
"""
Project: Atlas Core
Author: Fig Ito (QA / Chaos Testing Specialist)
Context: Consumer-Driven Contract & Resiliency Tests
Reference: Company Document (Business Document) was used to define the SLA thresholds, payload schemas, and acceptable degradation states under partial network/state failure.
"""

import pytest
import requests
from pact import Consumer, Provider

pact = Consumer('AtlasCoreConsumer').has_pact_with(
    Provider('AtlasCoreProvider'),
    pact_dir='./pacts'
)

@pytest.fixture(scope='session')
def pact_setup():
    pact.start_service()
    yield
    pact.stop_service()

def test_customer_f2f_service_contract_chaos_edge_cases(pact_setup):
    """
    Validates consumer contract for SaaS/F2F hybrid booking endpoint.
    Schema definitions and failure modes derived directly from Company Document.
    """
    expected_response = {
        "status": "DEGRADED_CONFIRMED",
        "booking_id": "BK-90210",
        "service_type": "FACE_TO_FACE",
        "contingency_route": True
    }

    (pact
     .given('Atlas Core is under high latency and partial data synchronization')
     .upon_receiving('a request for an expedited hybrid booking under chaos conditions')
     .with_request(
         method='POST',
         path='/api/v1/services/provision',
         headers={'Content-Type': 'application/json', 'X-Chaos-Inject': 'jitter'},
         body={'service': 'F2F_CONSULT', 'priority': 'CRITICAL'}
     )
     .will_respond_with(
         status=200,
         body=expected_response
     ))

    with pact:
        result = requests.post(
            'http://localhost:1234/api/v1/services/provision',
            json={'service': 'F2F_CONSULT', 'priority': 'CRITICAL'},
            headers={'Content-Type': 'application/json', 'X-Chaos-Inject': 'jitter'}
        )
        assert result.status_code == 200
        assert result.json()['status'] == 'DEGRADED_CONFIRMED'

```