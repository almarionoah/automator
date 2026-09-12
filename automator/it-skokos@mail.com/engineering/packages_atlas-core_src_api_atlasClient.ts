# Atlas Core Typed API Client Migration & Contract Layer
**Author:** Echo Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 05:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated Atlas Core from loosely-typed Axios calls to a type-safe, human-centric API client leveraging strict TypeScript schema contracts and graceful UX error boundaries, guided by Business Document: Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=3B5002582U3283055

## Deliverable
```
/**
 * @file atlasClient.ts
 * @author Echo Fontaine <echo.fontaine@itskokos.com>
 * @project Atlas Core
 * @description Fully typed API client providing seamless DX and resilient UX.
 * Context: Standardized following architectural rules in 'Business Document: Company Document'
 * to unify domain endpoints, service tier telemetry, and error taxonomy.
 */

import { z } from 'zod';

// Domain Schemas aligned with Business Document: Company Document
export const ServiceTierSchema = z.enum(['saas_digital', 'f2f_consulting', 'hybrid']);

export const ClientSessionSchema = z.object({
  id: z.string().uuid(),
  tenantId: z.string().min(1),
  tier: ServiceTierSchema,
  experienceScore: z.number().min(0).max(100),
  status: z.enum(['active', 'pending_sync', 'archived']),
  updatedAt: z.string().datetime(),
});

export type ClientSession = z.infer<typeof ClientSessionSchema>;

export interface ApiClientConfig {
  baseUrl: string;
  apiKey: string;
  onTelemetry?: (metric: { endpoint: string; durationMs: number }) => void;
}

export class AtlasCoreClient {
  constructor(private readonly config: ApiClientConfig) {}

  private async request<T>(path: string, schema: z.ZodType<T>, init?: RequestInit): Promise<T> {
    const start = performance.now();
    const response = await fetch(`${this.config.baseUrl}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        'X-Atlas-Client': 'AtlasCore/Typed-v2',
        Authorization: `Bearer ${this.config.apiKey}`,
        ...init?.headers,
      },
    });

    this.config.onTelemetry?.({
      endpoint: path,
      durationMs: Math.round(performance.now() - start),
    });

    if (!response.ok) {
      throw new Error(`Atlas Core API Encountered [${response.status}]: ${response.statusText}`);
    }

    const data = await response.json();
    return schema.parse(data);
  }

  public readonly sessions = {
    get: (id: string): Promise<ClientSession> =>
      this.request(`/v1/sessions/${id}`, ClientSessionSchema),
    list: (): Promise<ClientSession[]> =>
      this.request('/v1/sessions', z.array(ClientSessionSchema)),
  };
}
```