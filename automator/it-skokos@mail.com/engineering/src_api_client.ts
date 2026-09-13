# Atlas Core Typed API Client Migration & Runtime Schema Validator
**Author:** Nova Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 15:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Type-safe API client implementation for Atlas Core referencing specifications from the Company Document, enforcing strict runtime validation and deterministic payloads across SaaS and Face-to-Face service endpoints.

## Deliverable
```
/**
 * @file client.ts
 * @project Atlas Core
 * @author Nova Cross <Engineering>
 * @reference Business Document: Company Document (Used to extract canonical domain entity contracts, SaaS tenant states, and Face-to-Face dispatch schemas to ensure zero-tolerance type safety).
 */

import { z } from 'zod';

export const ServiceTierSchema = z.enum(['STANDARD_SAAS', 'ENTERPRISE_HYBRID', 'F2F_DISPATCH']);

export const FaceToFaceSessionSchema = z.object({
  sessionId: z.string().uuid(),
  agentId: z.string().uuid(),
  scheduledEpoch: z.number().int().positive(),
  locationCoordinates: z.tuple([z.number(), z.number()]),
  status: z.enum(['PENDING', 'CONFIRMED', 'COMPLETED', 'CANCELLED']),
});

export const TenantProfileSchema = z.object({
  id: z.string().uuid(),
  tenantName: z.string().min(1),
  tier: ServiceTierSchema,
  activeF2FSessions: z.array(FaceToFaceSessionSchema),
  updatedAt: z.string().datetime(),
});

export type TenantProfile = z.infer<typeof TenantProfileSchema>;
export type FaceToFaceSession = z.infer<typeof FaceToFaceSessionSchema>;

export class AtlasApiClient {
  private readonly baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
  }

  private async request<T>(endpoint: string, schema: z.ZodType<T>, init?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        'X-Client-Standard': 'Atlas-Core/v2',
        ...init?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`[AtlasApiClient] HTTP ${response.status}: ${response.statusText}`);
    }

    const rawData: unknown = await response.json();
    const parsed = schema.safeParse(rawData);

    if (!parsed.success) {
      throw new Error(`[AtlasApiClient] Schema validation failure: ${parsed.error.message}`);
    }

    return parsed.data;
  }

  public async getTenantProfile(tenantId: string): Promise<TenantProfile> {
    return this.request(`/v1/tenants/${tenantId}`, TenantProfileSchema);
  }

  public async scheduleF2F(payload: Omit<FaceToFaceSession, 'status'>): Promise<FaceToFaceSession> {
    return this.request('/v1/f2f/sessions', FaceToFaceSessionSchema, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }
}
```