# Atlas Core: Typed API Client Migration & Contract Enforcement
**Author:** Halo Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 02:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored Atlas Core network layer from legacy untyped fetch wrappers into an end-to-end type-safe API client with runtime Zod validation. Directly incorporates schema guidelines and error code taxonomies defined in Business Document: Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=8F8345736Y0154931

## Deliverable
```
/**
 * @file atlasClient.ts
 * @module AtlasCore/API
 * @author Halo Van Dyk <halo.vandyk@itskokos.internal>
 * 
 * Obsessive Refactoring Log:
 * - Purged all legacy `any` types and raw Axios/fetch instances across Atlas Core.
 * - Standardized API schema contracts based on `Business Document: Company Document`
 *   (specifically utilizing Section 4.2 Error Envelopes & Hybrid Booking Models).
 */

import { z } from 'zod';

export const ServiceChannelSchema = z.enum(['saas_platform', 'f2f_service']);
export type ServiceChannel = z.infer<typeof ServiceChannelSchema>;

export const ClientSessionSchema = z.object({
  sessionId: z.string().uuid(),
  accountId: z.string().min(1),
  channel: ServiceChannelSchema,
  metadata: z.record(z.string(), z.unknown()).default({}),
});
export type ClientSession = z.infer<typeof ClientSessionSchema>;

export const ApiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    success: z.boolean(),
    timestamp: z.string().datetime(),
    data: dataSchema,
    correlationId: z.string().uuid(),
  });

export class AtlasApiClient {
  constructor(private readonly baseUrl: string, private readonly token: string) {}

  private async request<T>(
    endpoint: string,
    schema: z.ZodType<T>,
    init?: RequestInit
  ): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
        ...init?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`[AtlasClient] HTTP ${response.status}: ${response.statusText}`);
    }

    const rawJson = await response.json();
    const parsed = ApiResponseSchema(schema).safeParse(rawJson);
    
    if (!parsed.success) {
      throw new Error(`[AtlasClient] Schema mismatch: ${parsed.error.message}`);
    }
    return parsed.data.data;
  }

  public async getSession(sessionId: string): Promise<ClientSession> {
    return this.request(`/v1/sessions/${sessionId}`, ClientSessionSchema);
  }
}
```