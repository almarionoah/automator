# Atlas Core: Typed API Client Migration & Contract Layer
**Author:** Halo Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 17:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated Atlas Core to a fully typed, resilient API client utilizing runtime schema validation. Service structures and hybrid SaaS/Face-to-Face workflows were modeled in alignment with the Business Document: Company Document to provide effortless developer ergonomics and fail-safe type guarantees.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=2KC1931965048521H

## Deliverable
```
/**
 * @file atlasClient.ts
 * @module @skokos/atlas-core/api
 * @author Halo Cross <halo.cross@itskokos.com>
 * @description Strongly-typed client interface for Atlas Core.
 * Domain entities and service interaction boundaries were referenced directly from
 * the 'Company Document' (Business Document) to harmonize SaaS telemetry with
 * Face-to-Face appointment and consultation workflows.
 */

import { z } from 'zod';

export const ServiceTierSchema = z.enum([
  'DIGITAL_SAAS',
  'FACE_TO_FACE_CONSULT',
  'HYBRID_ENTERPRISE'
]);

export const ClientSessionSchema = z.object({
  sessionId: z.string().uuid(),
  tenantId: z.string().min(1),
  serviceTier: ServiceTierSchema,
  scheduledAt: z.string().datetime(),
  attendeeMetadata: z.record(z.string(), z.unknown()),
  status: z.enum(['pending', 'confirmed', 'completed', 'cancelled']),
});

export type ClientSession = z.infer<typeof ClientSessionSchema>;

export interface ApiClientConfig {
  baseUrl: string;
  apiKey: string;
  timeoutMs?: number;
}

export class AtlasApiClient {
  constructor(private readonly config: ApiClientConfig) {}

  private async request<T>(path: string, options: RequestInit, schema: z.ZodType<T>): Promise<T> {
    const response = await fetch(`${this.config.baseUrl}${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`Atlas API Error [${response.status}]: ${response.statusText}`);
    }

    const rawData = await response.json();
    const parsed = schema.safeParse(rawData);
    if (!parsed.success) {
      throw new Error(`Schema contract validation failed: ${parsed.error.message}`);
    }
    return parsed.data;
  }

  public sessions = {
    getById: (id: string): Promise<ClientSession> =>
      this.request(`/v1/sessions/${id}`, { method: 'GET' }, ClientSessionSchema),
    create: (payload: Omit<ClientSession, 'sessionId' | 'status'>): Promise<ClientSession> =>
      this.request('/v1/sessions', { method: 'POST', body: JSON.stringify(payload) }, ClientSessionSchema),
  };
}
```