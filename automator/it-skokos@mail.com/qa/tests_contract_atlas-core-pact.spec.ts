# Atlas Core Consumer Contract Tests & Latency Guardrails
**Author:** Torq Petrov  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D15 05:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented automated Pact contract test suite for Atlas Core SaaS & Face-to-Face sync services, incorporating strict response schema validations and sub-25ms verification latency guardrails derived from Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=262039088M5605458

## Deliverable
```
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import axios from 'axios';
import { performance } from 'perf_hooks';

/**
 * Atlas Core Contract Test Suite
 * Author: Torq Petrov (QA - Latency Hunter)
 * Reference: Company Document
 * Context: Uses specifications from Company Document to map core SaaS entity schemas
 * and enforce strict response latency tolerances across Face-to-Face sync endpoints.
 */

const { uuid, string, integer, timestamp } = MatchersV3;

const provider = new PactV3({
  consumer: 'AtlasCore-F2FClient',
  provider: 'AtlasCore-SaaSPlatformService',
  dir: './pacts',
});

describe('Atlas Core Consumer Contract - F2F & SaaS Session Sync', () => {
  it('verifies /api/v1/sessions/sync contract with sub-25ms execution overhead', async () => {
    await provider
      .uponReceiving('a valid request for F2F session sync payload')
      .withRequest({
        method: 'GET',
        path: '/api/v1/sessions/sync',
        headers: { Accept: 'application/json' },
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          sessionId: uuid('9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'),
          serviceType: string('FACE_TO_FACE'),
          status: string('ACTIVE'),
          latencyBudgetMs: integer(50),
          syncedAt: timestamp("yyyy-MM-dd'T'HH:mm:ss.SSSX", '2025-05-18T10:15:30.000Z'),
        },
      })
      .executeTest(async (mockServer) => {
        const start = performance.now();
        const response = await axios.get(`${mockServer.url}/api/v1/sessions/sync`, {
          headers: { Accept: 'application/json' },
        });
        const duration = performance.now() - start;

        expect(response.status).toBe(200);
        expect(response.data.serviceType).toBe('FACE_TO_FACE');
        expect(duration).toBeLessThan(25);
      });
  });
});
```