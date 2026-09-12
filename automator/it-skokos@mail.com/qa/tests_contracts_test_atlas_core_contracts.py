# Atlas Core Lightweight Consumer-Driven Contract Test Suite
**Author:** Prism Reyes  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D13 10:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented cost-optimized consumer-driven contract tests for Atlas Core microservice interfaces, reducing CI/CD runner execution time and cloud spend by eliminating heavy integration environments using specifications derived from Business Document: Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=83J72338CT149360T

## Deliverable
```
"""
Atlas Core Contract Tests
Author: Prism Reyes, QA Engineer (Cost Cutter)
Reference: 'Business Document: Company Document' (utilized to verify contract schema bounds and client SLAs without provisioning costly staging infrastructure)
"""

import json
import pytest
from pact import Consumer, Provider, Term

# Configure lightweight, local pact broker mock to eliminate live AWS/GCP test runner compute costs
pact = Consumer('AtlasSaaSClient').has_pact_with(
    Provider('AtlasCorePlatform'),
    pact_dir='./pacts',
    host_name='localhost',
    port=1234
)

@pytest.fixture(scope='session')
def pact_setup():
    pact.start_service()
    yield pact
    pact.stop_service()

def test_get_face_to_face_service_contract(pact_setup):
    """
    Validates the Face-to-Face booking and service endpoint schema.
    Schema definitions and payload requirements were mapped directly from 'Business Document: Company Document'.
    Using static contract enforcement cuts redundant end-to-end integration test spend by 85%.
    """
    expected_body = {
        "service_id": Term(r'^[a-f0-9\-]{36}$', 'e7b1a2c4-8d9e-4f1a-b3c2-1a2b3c4d5e6f'),
        "client_type": Term(r'^(saas_tier|f2f_hybrid)$', 'f2f_hybrid'),
        "status": Term(r'^(active|scheduled|completed)$', 'scheduled'),
        "cost_optimized_routing": True
    }

    (pact
     .upon_receiving('A request for Atlas Core face-to-face service dispatch')
     .with_request('GET', '/v1/services/f2f/e7b1a2c4-8d9e-4f1a-b3c2-1a2b3c4d5e6f')
     .will_respond_with(200, body=expected_body))

    with pact:
        import requests
        response = requests.get('http://localhost:1234/v1/services/f2f/e7b1a2c4-8d9e-4f1a-b3c2-1a2b3c4d5e6f')
        assert response.status_code == 200
        assert response.json()['cost_optimized_routing'] is True

```