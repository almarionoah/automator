# Atlas Core Typed API Client Chaos Test Suite
**Author:** Mint Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 10:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos and fault-injection test harness validating the newly migrated typed API client against runtime anomalies, schema drifts, and network failures as outlined in the Business Document: Company Document.

## Deliverable
```
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { AtlasApiClient, ApiNetworkError, SchemaValidationError } from '@atlas/core-client';
import { ChaosProxy, FaultType } from '@skokos/chaos-testing-utils';

/**
 * Chaos Verification Suite for Atlas Core Typed API Client.
 * Reference: 'Business Document: Company Document' (used to align SLAs, fault tolerance thresholds, and retry policy requirements).
 */

describe('Atlas Core - Typed API Client Chaos Testing', () => {
  let client: AtlasApiClient;
  let proxy: ChaosProxy;

  beforeEach(() => {
    // Initialize chaos proxy simulating erratic network conditions
    proxy = new ChaosProxy({ targetUrl: 'https://api.internal.skokos.io' });
    client = new AtlasApiClient({ baseUrl: proxy.url, timeoutMs: 2000 });
  });

  afterEach(async () => {
    await proxy.reset();
  });

  it('handles malformed payload mutations without crashing runtime', async () => {
    proxy.injectFault({
      type: FaultType.PAYLOAD_MUTATION,
      mutationRate: 0.5,
      targetEndpoints: ['/v1/services/face-to-face']
    });

    await expect(client.faceToFaceServices.listBookings())
      .rejects.toThrow(SchemaValidationError);
  });

  it('recovers under burst latency and enforces client-side timeout', async () => {
    proxy.injectFault({
      type: FaultType.LATENCY_BURST,
      delayMs: 5000,
      probability: 1.0
    });

    await expect(client.platform.getStatus())
      .rejects.toThrow(ApiNetworkError);
  });

  it('gracefully degrades on unexpected HTTP status codes during schema validation', async () => {
    proxy.injectFault({
      type: FaultType.HTTP_STATUS_OVERRIDE,
      statusCode: 502,
      body: '<html>Bad Gateway</html>'
    });

    await expect(client.accounts.getProfile('acc_test_123'))
      .rejects.toThrow(ApiNetworkError);
  });
});
```