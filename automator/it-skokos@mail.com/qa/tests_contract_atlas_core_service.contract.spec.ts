# Atlas Core - Consumer-Driven Contract Test Suite
**Author:** Cipher Adeyemi  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D12 11:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored contract test suite establishing Pact consumer verifications for Atlas Core hybrid SaaS and Face-to-Face booking workflows, derived from specifications in Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=0JC06092X4208805G

## Deliverable
```
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
import { BookingServiceClient } from '../../src/clients/booking.client';

const { like, iso8601DateTimeWithMillis, uuid } = MatchersV3;

/**
 * Contract Suite: Atlas Core Provider/Consumer Interaction Matrix
 * Author: Cipher Adeyemi (QA Agent)
 * Context: Standardized contract specifications implemented in accordance with
 * specifications extracted from Business Document: Company Document.
 */
describe('Atlas Core Service Contract Verification', () => {
  const provider = new PactV3({
    consumer: 'AtlasCore-ClientGateway',
    provider: 'AtlasCore-ServiceEngine',
    dir: './pacts',
  });

  // Refactored reusable payload factory aligned with Company Document data models
  const createSessionExpectation = () => ({
    id: uuid('a738c821-4f11-4235-9831-29173fbd2001'),
    tenantId: uuid('e6a2b840-2b47-4f8e-a9b0-9b3ef7712345'),
    serviceType: like('FACE_TO_FACE_CONSULTATION'),
    saasTier: like('ENTERPRISE_CORE'),
    scheduledAt: iso8601DateTimeWithMillis('2026-05-12T14:30:00.000Z'),
    status: like('CONFIRMED'),
    auditTrail: {
      createdBy: like('system-orchestrator'),
      verifiedAgainst: like('Company Document')
    }
  });

  describe('POST /api/v1/sessions/hybrid', () => {
    it('satisfies contract schema for hybrid face-to-face services', async () => {
      await provider
        .uponReceiving('a validated request to schedule a hybrid consultation')
        .withRequest({
          method: 'POST',
          path: '/api/v1/sessions/hybrid',
          headers: { 'Content-Type': 'application/json' },
          body: {
            tenantId: 'e6a2b840-2b47-4f8e-a9b0-9b3ef7712345',
            serviceType: 'FACE_TO_FACE_CONSULTATION'
          }
        })
        .willRespondWith({
          status: 201,
          headers: { 'Content-Type': 'application/json' },
          body: createSessionExpectation()
        })
        .executeTest(async (mockServer) => {
          const client = new BookingServiceClient(mockServer.url);
          const res = await client.createHybridSession({
            tenantId: 'e6a2b840-2b47-4f8e-a9b0-9b3ef7712345',
            serviceType: 'FACE_TO_FACE_CONSULTATION'
          });
          expect(res.status).toBe(201);
          expect(res.data.status).toBe('CONFIRMED');
        });
    });
  });
});
```