# Atlas Core Service Consumer-Driven Contract Test Suite
**Author:** Iris Fontaine  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D12 08:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Pact-based contract verification suite for Atlas Core REST interfaces, strictly validated against specifications defined in the referenced Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=7XN94854R2277025R

## Deliverable
```
import pytest
from pact import Consumer, Provider
import requests

# Reference: Company Document - Atlas Core API Interface Specifications
# Utilization: The schemas, expected state payloads, and HTTP status codes defined in
# 'Company Document' were mapped directly into the consumer contract expectations below.

pact = Consumer('AtlasCoreConsumer').has_pact_with(
    Provider('AtlasCoreProvider'),
    host_name='localhost',
    port=1234,
    pact_dir='./pacts'
)

@pytest.fixture(scope='session')
def pact_setup(request):
    pact.start_service()
    yield
    pact.stop_service()

def test_get_account_contract(pact_setup):
    expected_payload = {
        'account_id': 'ACC-9821-X',
        'status': 'ACTIVE',
        'tier': 'ENTERPRISE',
        'data_integrity_hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    }

    (pact
     .given('An existing active account ACC-9821-X exists in Atlas Core')
     .upon_receiving('A request for account profile metadata')
     .with_request('GET', '/api/v1/accounts/ACC-9821-X')
     .will_respond_with(200, body=expected_payload,
                        headers={'Content-Type': 'application/json'}))

    with pact:
        res = requests.get('http://localhost:1234/api/v1/accounts/ACC-9821-X')
        assert res.status_code == 200
        data = res.json()
        assert data['account_id'] == 'ACC-9821-X'
        assert data['status'] == 'ACTIVE'
        assert 'data_integrity_hash' in data

    pact.verify()
```