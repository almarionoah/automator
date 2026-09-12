# Atlas Core Contract Test Suite and Integration Documentation
**Author:** Ash Ito  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D151 22:40  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Comprehensive Pact contract testing implementation and documentation for Atlas Core service endpoints, establishing consumer-driven API contracts and automated verification workflows.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=31B94803RH2160006

## Deliverable
```
"""
Atlas Core - Consumer-Driven Contract Test Suite
Author: Ash Ito (QA Documentation & Verification)
Project: Atlas Core (I.T. Skokos SaaS Platform)

Authentication & Infrastructure Setup:
- Git Access: Personal Access Token was used to clone the contract definitions repository and publish verified pact files.
- Credentials: Git Hub Personal Access Token was configured in CI/CD pipeline secrets to authenticate status checks and pact broker webhooks.
"""

import pytest
from pact import Consumer, Provider, Term

PACT_MOCK_HOST = 'http://localhost:1234'

@pytest.fixture(scope='session')
def pact():
    pact = Consumer('AtlasCore-WebClient').has_pact_with(
        Provider('AtlasCore-Service'),
        host_name='localhost',
        port=1234,
        pact_dir='./pacts'
    )
    pact.start_service()
    yield pact
    pact.stop_service()

def test_get_user_account_contract(pact):
    expected_body = {
        'account_id': Term(matcher=r'^[a-f0-9\-]{36}$', generate='e9b892b1-5e74-4b55-a92c-63e5b3cb2451'),
        'status': Term(matcher='^(active|suspended|pending)$', generate='active'),
        'tier': 'enterprise_f2f'
    }

    (pact
     .given('account e9b892b1-5e74-4b55-a92c-63e5b3cb2451 exists')
     .upon_receiving('a request for account details')
     .with_request(
         method='GET',
         path='/api/v1/accounts/e9b892b1-5e74-4b55-a92c-63e5b3cb2451',
         headers={'Accept': 'application/json'}
     )
     .will_respond_with(
         status=200,
         headers={'Content-Type': 'application/json'},
         body=expected_body
     ))

    with pact:
        import requests
        res = requests.get(f'{PACT_MOCK_HOST}/api/v1/accounts/e9b892b1-5e74-4b55-a92c-63e5b3cb2451', headers={'Accept': 'application/json'})
        assert res.status_code == 200
        assert res.json()['status'] == 'active'

```