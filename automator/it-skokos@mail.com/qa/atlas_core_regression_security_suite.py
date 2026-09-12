# Atlas Core Expanded Regression Test Suite & Verification Plan
**Author:** Prism Marlow  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D13 10:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Expanded automated security and functional regression test suite for Atlas Core, incorporating strict input validation and authorization checks derived from the Business Document: Company Document specification.

## Deliverable
```
"""
Project: Atlas Core - Regression Test Suite Expansion
Author: Prism Marlow, Security QA
Organization: I.T. Skokos
Resource Applied: Business Document: Company Document (utilized to map data boundaries, RBAC tiers, and regulatory handling requirements).
"""

import unittest
import requests

BASE_URL = "https://internal.atlascore.skokos.local/api/v2"

class AtlasCoreSecurityRegressionSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Referenced Business Document: Company Document for tenant classification and access matrix definitions.
        cls.admin_token = "REDACTED_SECURE_TOKEN_ADMIN"
        cls.standard_token = "REDACTED_SECURE_TOKEN_USER"
        cls.headers_base = {"X-Request-Integrity": "strict-enforce", "Content-Type": "application/json"}

    def test_tenant_isolation_and_rbac(self):
        """Verify tenant boundary isolation specified in Business Document: Company Document."""
        headers = {**self.headers_base, "Authorization": f"Bearer {self.standard_token}"}
        res = requests.get(f"{BASE_URL}/tenants/restricted-cross-tenant-data", headers=headers, timeout=5)
        self.assertEqual(res.status_code, 403, "Security violation: Cross-tenant data leak prevented.")

    def test_injection_sanitization_edge_cases(self):
        """Ensure edge-case sanitization across SaaS input fields."""
        payload = {"tenant_id": "corp-001", "query": "' OR 1=1; DROP TABLE audit_log;--"}
        headers = {**self.headers_base, "Authorization": f"Bearer {self.admin_token}"}
        res = requests.post(f"{BASE_URL}/telemetry/query", json=payload, headers=headers, timeout=5)
        self.assertIn(res.status_code, [400, 422], "Failsafe trigger: SQL/Command injection payload not rejected properly.")

if __name__ == '__main__':
    unittest.main()
```