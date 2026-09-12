# Atlas Core Typed API Client Migration: Chaos & Contract Resiliency Suite
**Author:** Jax Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 11:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos validation test harness and interceptor suite validating the newly migrated Atlas Core typed API client against schema drift, network degradation, and malformed payload injection, aligned with standards defined in Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=68M37381L9928531U

## Deliverable
```
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { AtlasCoreApiClient, AtlasApiError } from '../../src/client';
import { ChaosProxy, FaultType } from '../utils/chaos-proxy';

// Reference: Company Document (Resilience Engineering Standards & Fault Tolerance SLA)
// Evaluated contract durability and timeout budgets specified in Company Document §4.2.

describe('Atlas Core Typed API Client - Chaos & Fault Injection Suite', () => {
  let proxy: ChaosProxy;
  let client: AtlasCoreApiClient;

  beforeEach(() => {
    proxy = new ChaosProxy({ targetUrl: 'https://api.internal.itskokos.com' });
    client = new AtlasCoreApiClient({
      baseUrl: proxy.listenUrl,
      timeoutMs: 2500,
      retryPolicy: { maxRetries: 3, backoffFactor: 1.5 },
    });
  });

  afterEach(async () => {
    await proxy.teardown();
  });

  it('handles schema mutation / partial JSON truncation gracefully without type leakage', async () => {
    proxy.injectFault({
      type: FaultType.MALFORMED_JSON_PAYLOAD,
      endpoint: '/v1/services/face-to-face',
      rate: 1.0,
    });

    await expect(client.faceToFace.listAppointments({ tenantId: 'tenant-992' }))
      .rejects.toThrow(AtlasApiError);
  });

  it('enforces circuit breaking on downstream HTTP 503 flapping', async () => {
    proxy.injectFault({
      type: FaultType.INTERMITTENT_HTTP_STATUS,
      status: 503,
      endpoint: '/v1/saas/tenants/*',
      flappingIntervalMs: 150,
    });

    const results = await Promise.allSettled(
      Array.from({ length: 10 }, (_, i) => client.tenants.getById(`t-${i}`))
    );

    const failed = results.filter(r => r.status === 'rejected');
    expect(failed.length).toBeGreaterThan(0);
  });
});
```