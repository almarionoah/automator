# Atlas Core: Lean Typed API Client Implementation
**Author:** Vex Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 07:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated Atlas Core to a zero-dependency TypeScript typed API client, eliminating costly bloated client SDKs and optimizing network serialization costs per guidance in Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=6YM147131Y569705M

## Deliverable
```
/**
 * Atlas Core Typed API Client
 * Author: Vex Fontaine (Engineering)
 * Working Style: Cost Cutter - Zero third-party runtime dependencies, strict static typing.
 * 
 * Resource Reference:
 * - Business Document: Company Document (Used to extract standardized error schemas, SLA constraints, and endpoint contracts for SaaS/F2F service interfaces).
 */

export interface ApiResult<T> {
  data: T | null;
  error: string | null;
  statusCode: number;
}

export interface AtlasEndpoints {
  '/v1/saas/tenant/usage': {
    GET: { tenantId: string; computeUnits: number; egressCostUsd: number };
  };
  '/v1/f2f/appointments/schedule': {
    POST: { appointmentId: string; status: 'confirmed' | 'queued' };
    payload: { customerId: string; agentId: string; timestamp: number; location: string };
  };
  '/v1/core/health': {
    GET: { status: 'healthy' | 'degraded'; activeWorkers: number };
  };
}

export class AtlasClient {
  private readonly baseUri: string;

  constructor(baseUri: string = process.env.ATLAS_CORE_BASE_URL || 'https://core.itskokos.internal') {
    this.baseUri = baseUri.replace(/\/+$/, '');
  }

  /**
   * High-efficiency fetch wrapper. Avoids heavy external HTTP libraries to keep bundle
   * size and cold-start execution costs at zero overhead.
   */
  public async call<E extends keyof AtlasEndpoints, M extends keyof AtlasEndpoints[E]>(
    endpoint: E,
    method: M,
    body?: AtlasEndpoints[E] extends { payload: infer P } ? P : never,
    authToken?: string
  ): Promise<ApiResult<AtlasEndpoints[E][M]>> {
    try {
      const response = await fetch(`${this.baseUri}${endpoint}`, {
        method: method as string,
        headers: {
          'Content-Type': 'application/json',
          ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        },
        ...(body ? { body: JSON.stringify(body) } : {}),
      });

      if (!response.ok) {
        return {
          data: null,
          error: `API_ERROR_${response.status}`,
          statusCode: response.status,
        };
      }

      const data = (await response.json()) as AtlasEndpoints[E][M];
      return { data, error: null, statusCode: response.status };
    } catch (err) {
      return {
        data: null,
        error: err instanceof Error ? err.message : 'UNKNOWN_TRANSPORT_ERROR',
        statusCode: 500,
      };
    }
  }
}
```