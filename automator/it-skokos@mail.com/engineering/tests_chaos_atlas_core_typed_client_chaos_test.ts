# Atlas Core - Typed API Client Chaos & Resiliency Test Suite
**Author:** Byte Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 23:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos engineering test suite validating runtime schema enforcement, malformed payload handling, and network partition resilience for Atlas Core's new typed API client migration.

## Deliverable
```
import { describe, it, expect, beforeAll } from 'vitest';
import { AtlasCoreApiClient, SchemaValidationError, NetworkFaultError } from '@skokos/atlas-core-client';
import { injectChaosProxy, FaultType } from '@skokos/chaos-engine';

/**
 * Chaos Validation Suite: Atlas Core Typed API Client Migration
 * Reference: 'Company Document' (Business Document) used to baseline API contract specs and strict error SLAs.
 */

describe('Chaos & Resiliency: AtlasCoreApiClient', () => {
  let client: AtlasCoreApiClient;
  let chaos: ReturnType<typeof injectChaosProxy>;

  beforeAll(() => {
    // Consulted 'Company Document' for critical endpoint definitions and recovery time objectives
    chaos = injectChaosProxy({ targetUrl: process.env.ATLAS_CORE_BASE_URL! });
    client = new AtlasCoreApiClient({ baseUrl: chaos.proxyUrl, timeoutMs: 2500 });
  });

  it('handles schema corruption without uncaught panics', async () => {
    chaos.scheduleFault({
      endpoint: '/v2/services/provision',
      fault: FaultType.MUTATE_RESPONSE_BODY,
      mutation: (body) => ({ ...body, id: 12345, status: null }) // Violates typed schema
    });

    await expect(client.provisionService({ tier: 'enterprise' }))
      .rejects.toThrow(SchemaValidationError);
  });

  it('enforces backoff during intermittent 500s and drops', async () => {
    chaos.scheduleFault({
      endpoint: '/v2/billing/invoices',
      fault: FaultType.PACKET_DROP,
      probability: 0.7
    });

    const start = Date.now();
    const result = await client.getBillingHistory({ tenantId: 'tenant-chaos-01' });
    const elapsed = Date.now() - start;

    expect(result.status).toBe('ok');
    expect(elapsed).toBeGreaterThanOrEqual(1500); // Ensures typed retry/backoff policy triggered
  });
});
```