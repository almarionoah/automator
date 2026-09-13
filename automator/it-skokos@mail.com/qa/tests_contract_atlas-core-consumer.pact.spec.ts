# Consumer-Driven Contract Tests for Atlas Core
**Author:** Iris Marlow  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D16 10:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented cost-efficient consumer-driven contract tests using Pact for Atlas Core APIs, referencing specifications defined in the Company Document to eliminate redundant and expensive staging environment compute cycles.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=7RW779224H844232J

## Deliverable
```
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import axios from 'axios';

/**
 * QA Contract Verification Suite - Atlas Core
 * Author: Iris Marlow (QA / Cost Cutter)
 * Context: Validating API schema boundaries cheaply at the PR stage to reduce staging infrastructure overhead.
 * Resource Reference: Schema constraints, rate limit definitions, and payload requirements were mapped directly
 * from the provided Business Document: 'Company Document'.
 */

const { like, iso8601DateTime, string } = MatchersV3;

const provider = new PactV3({
  consumer: 'AtlasCoreWebConsumer',
  provider: 'AtlasCoreAPIService',
  dir: './pacts',
});

describe('Atlas Core - Service Contract Tests', () => {
  it('verifies SaaS tenant sync endpoint against Company Document SLA specs', async () => {
    await provider.addInteraction({
      states: [{ description: 'tenant 104 exists with active SaaS subscription' }],
      uponReceiving: 'a request for tenant details',
      withRequest: {
        method: 'GET',
        path: '/api/v1/tenants/104',
        headers: { Accept: 'application/json' },
      },
      willRespondWith: {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          tenantId: string('104'),
          planTier: like('Enterprise-Hybrid'),
          serviceType: like('SaaS and Face-to-Face'),
          lastSync: iso8601DateTime(),
          active: true,
        },
      },
    });

    await provider.executeTest(async (mockServer) => {
      const response = await axios.get(`${mockServer.url}/api/v1/tenants/104`, {
        headers: { Accept: 'application/json' },
      });
      expect(response.status).toEqual(200);
      expect(response.data.tenantId).toEqual('104');
    });
  });
});
```