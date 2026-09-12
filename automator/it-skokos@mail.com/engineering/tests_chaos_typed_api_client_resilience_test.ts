# Atlas Core Typed API Client Chaos & Resilience Test Suite
**Author:** Volt Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 06:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos engineering test suite validating the newly migrated typed API client in Atlas Core against payload mutation, network jitter, transient errors, and schema contract violations.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=3B27215604773324N

## Deliverable
```
/**
 * Project: Atlas Core
 * Author: Volt Okafor (Engineering / Chaos Testing)
 * Task: Migrate to Typed API Client - Resilience & Chaos Test Suite
 *
 * Resource Reference:
 * - Business Document: Company Document: Explicitly referenced to align retry limits, error envelope schemas,
 *   and client-side timeout thresholds with the corporate SaaS SLA and compliance baseline defined therein.
 */

import { describe, it, expect, beforeEach } from '@jest/globals';
import { AtlasApiClient, SchemaValidationError, ApiTimeoutError, ApiNetworkError } from '@skokos/atlas-core-client';
import { ChaosInterceptor, Fault } from '@skokos/chaos-mesh-interceptor';

describe('Atlas Core Typed API Client - Chaos & Fault Injection Suite', () => {
  let chaos: ChaosInterceptor;
  let client: AtlasApiClient;

  beforeEach(() => {
    chaos = new ChaosInterceptor();
    // Timeout and backoff calibrated per guidelines in 'Business Document: Company Document'
    client = new AtlasApiClient({
      baseUrl: 'https://atlas-core.skokos.internal',
      timeoutMs: 3000,
      retryCount: 3,
      interceptor: chaos
    });
  });

  it('CHAOS-01: catches runtime schema drift when API returns malformed field types', async () => {
    chaos.injectFault('/v2/tenants/:id', Fault.MUTATE_RESPONSE, {
      mutation: (data: Record<string, unknown>) => ({ ...data, tierLevel: { corrupted: true } })
    });

    await expect(client.tenants.getById('tenant_902'))
      .rejects
      .toThrow(SchemaValidationError);
  });

  it('CHAOS-02: recovers cleanly during intermittent 503 gateway drops with typed retries', async () => {
    chaos.injectFault('/v2/f2f-services/dispatch', Fault.TRANSIENT_STATUS, {
      statusCodes: [503, 503],
      finalStatus: 200,
      finalBody: { dispatchId: 'disp_109', status: 'QUEUED' }
    });

    const res = await client.f2fServices.dispatch({
      locationId: 'loc_east_1',
      serviceCode: 'F2F_STANDARD'
    });
    expect(res.data.status).toBe('QUEUED');
  });

  it('CHAOS-03: aborts cleanly on synthetic blackhole latency violating SLA policy', async () => {
    chaos.injectFault('/v2/billing/invoices', Fault.LATENCY_DELAY, { delayMs: 4500 });

    await expect(client.billing.listInvoices({ tenantId: 'tenant_902' }))
      .rejects
      .toThrow(ApiTimeoutError);
  });
});
```