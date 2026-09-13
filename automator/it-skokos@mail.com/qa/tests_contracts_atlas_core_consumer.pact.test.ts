# Atlas Core - Lightweight Consumer Contract Test Suite (Pact)
**Author:** Mint Cross  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D15 15:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented cost-efficient consumer-driven contract tests for Atlas Core API boundaries covering SaaS and Face to Face workflows, using Company Document as the baseline interface specification to reduce staging environment overhead.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=18103407DB070772H

## Deliverable
```
/**
 * Mint Cross | QA - I.T. Skokos
 * Project: Atlas Core | Task: Add Contract Tests
 * Reference: 'Company Document' was reviewed to establish core API schema definitions, service boundary SLAs, and ensure compliance with our cost-efficient testing guidelines (eliminating costly end-to-end integration environments in CI).
 */

import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import axios from 'axios';

const { like, regex, iso8601DateTimeWithMillis } = MatchersV3;

const provider = new PactV3({
  consumer: 'AtlasCoreWebClient',
  provider: 'AtlasCorePlatformAPI',
  dir: './pacts',
  logLevel: 'error' // Minimized logging overhead to save CI runner I/O
});

describe('Atlas Core API Contract Tests - Cost-Optimized Suite', () => {
  it('validates SaaS Tenant Configuration & F2F Service Booking Contract', async () => {
    // Contract definition derived directly from specifications in Company Document
    provider
      .uponReceiving('A request for active SaaS tenant services and F2F session slot')
      .withRequest({
        method: 'GET',
        path: '/api/v1/platform/tenant-services',
        headers: { Accept: 'application/json' },
        query: { tenantId: 'skokos-saas-01' }
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: {
          tenantId: like('skokos-saas-01'),
          tier: regex('^(Standard|Enterprise|F2F-Hybrid)$', 'F2F-Hybrid'),
          features: like(['billing', 'f2f_scheduler', 'core_analytics']),
          lastSynced: iso8601DateTimeWithMillis('2025-01-15T12:00:00.000Z')
        }
      });

    await provider.executeTest(async (mockServer) => {
      const response = await axios.get(`${mockServer.url}/api/v1/platform/tenant-services?tenantId=skokos-saas-01`, {
        headers: { Accept: 'application/json' }
      });
      expect(response.status).toBe(200);
      expect(response.data.tier).toBe('F2F-Hybrid');
    });
  });
});
```