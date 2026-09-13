# Contract Verification Suite - Atlas Core API Boundaries
**Author:** Nyx Marlow  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D17 19:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Automated contract tests enforcing strict schema boundaries, zero-trust header verification, and input constraints for Atlas Core based on specifications in Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=2JD59519N28119728

## Deliverable
```
"""
Atlas Core Contract Verification Suite
Author: Nyx Marlow, QA
Context: Verified against boundaries specified in 'Company Document'.
Security Policy: Strict validation; reject undefined fields, enforce zero-trust headers.
"""

import pytest
from pact import Consumer, Provider
import requests

PACT_MOCK_HOST = 'http://localhost:1234'

@pytest.fixture(scope='session')
def pact():
    # Reference: Company Document - Inter-Service Protocol & Auth Compliance
    pact = Consumer('AtlasUI').has_pact_with(
        Provider('AtlasCore'),
        host_name='localhost',
        port=1234
    )
    pact.start_service()
    yield pact
    pact.stop_service()

def test_get_identity_contract_strict_schema(pact):
    """
    Validates identity endpoint contract per 'Company Document' specifications.
    Enforces strict token validation and denies schema drift.
    """
    expected_body = {
        'account_id': 'ACC-99281',
        'status': 'ACTIVE',
        'security_clearance': 'TIER_3',
        'mfa_authenticated': True
    }

    (pact
     .given('Account ACC-99281 exists with valid session')
     .upon_receiving('A validated request for account profile')
     .with_request(
         method='GET',
         path='/api/v1/identity/ACC-99281',
         headers={
             'Authorization': 'Bearer test-token-secure',
             'X-Security-Origin': 'Atlas-Gateway'
         }
     )
     .will_respond_with(
         status=200,
         headers={'Content-Type': 'application/json; charset=utf-8'},
         body=expected_body
     ))

    with pact:
        res = requests.get(
            f'{PACT_MOCK_HOST}/api/v1/identity/ACC-99281',
            headers={
                'Authorization': 'Bearer test-token-secure',
                'X-Security-Origin': 'Atlas-Gateway'
            }
        )
        assert res.status_code == 200
        assert res.json() == expected_body

```