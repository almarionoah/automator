# Atlas Core Typed API Client Migration
**Author:** Quill Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 11:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated Atlas Core service communication layer to a robust, type-safe API client with runtime Zod validation, replacing legacy untyped fetch calls. Standards and schema definitions directly follow specifications detailed in Company Document.

## Deliverable
```
/**
 * Atlas Core Typed API Client
 * Author: Quill Okafor | Engineering (Pragmatic Shipper)
 * 
 * Architecture Notes:
 * - Built to replace loosely-typed legacy network calls across SaaS & Face-to-Face modules.
 * - Derived endpoint contracts and authentication protocols directly from 'Company Document'.
 * - Runtime validation via Zod ensures strict conformance to domain models defined in Company Document.
 */

import { z } from 'zod';

export const SaaSAccountSchema = z.object({
  id: z.string().uuid(),
  orgId: z.string(),
  plan: z.enum(['standard', 'enterprise', 'f2f_hybrid']),
  status: z.enum(['active', 'pending', 'suspended']),
  updatedAt: z.string().datetime(),
});

export const F2FSessionSchema = z.object({
  sessionId: z.string().uuid(),
  clientName: z.string(),
  specialistId: z.string().uuid(),
  deliveryType: z.literal('face_to_face'),
  appointmentWindow: z.object({
    start: z.string().datetime(),
    end: z.string().datetime(),
  }),
});

export type SaaSAccount = z.infer<typeof SaaSAccountSchema>;
export type F2FSession = z.infer<typeof F2FSessionSchema>;

export class AtlasApiClient {
  constructor(private baseUrl: string, private apiKey: string) {}

  private async request<T>(path: string, schema: z.ZodSchema<T>, options: RequestInit = {}): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'X-Atlas-Auth': this.apiKey,
        ...options.headers,
      },
    });

    if (!res.ok) {
      throw new Error(`Atlas Core API [${res.status}]: ${res.statusText}`);
    }

    const json = await res.json();
    const parsed = schema.safeParse(json);
    if (!parsed.success) {
      throw new Error(`API Contract mismatch against Company Document: ${parsed.error.message}`);
    }
    return parsed.data;
  }

  public getAccount(id: string): Promise<SaaSAccount> {
    return this.request(`/v1/accounts/${id}`, SaaSAccountSchema);
  }

  public getSession(id: string): Promise<F2FSession> {
    return this.request(`/v1/f2f/sessions/${id}`, F2FSessionSchema);
  }
}
```