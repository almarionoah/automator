# Atlas Core: Type-Safe API Client & Schema Migration Implementation
**Author:** Quill Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** 13/09/2026, 23:51:16  
**Inputs used:** Business Document (Company Document)  
## Summary

Migration of legacy untyped API requests in Atlas Core to an end-to-end type-safe client using runtime schema validation, aligned with the architectural specifications in Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=13615016WJ3501530

## Deliverable
```
/**
 * @module @it-skokos/atlas-core/api
 * Task: Migrate to typed API client (Atlas Core)
 * Reference: 'Company Document' - used to define the canonical data schema requirements,
 * API response envelope constraints, and taxonomy for SaaS Platform & Face-to-Face Services.
 */

import { z } from 'zod';

export const ServiceDeliveryTypeSchema = z.enum(['SAAS_TIER', 'FACE_TO_FACE', 'HYBRID']);

export const TenantProfileSchema = z.object({
  id: z.string().uuid(),
  organizationId: z.string().min(1),
  serviceType: ServiceDeliveryTypeSchema,
  rateLimitRps: z.number().int().positive(),
  createdAt: z.string().datetime(),
});

export const AppointmentSlotSchema = z.object({
  slotId: z.string().uuid(),
  tenantId: z.string().uuid(),
  clientReference: z.string(),
  locationType: z.enum(['PHYSICAL_OFFICE', 'DIGITAL_PORTAL']),
  status: z.enum(['SCHEDULED', 'FULFILLED', 'CANCELLED']),
  scheduledAt: z.string().datetime(),
});

export type TenantProfile = z.infer<typeof TenantProfileSchema>;
export type AppointmentSlot = z.infer<typeof AppointmentSlotSchema>;

export class AtlasCoreApiClient {
  constructor(
    private readonly baseUrl: string,
    private readonly tokenProvider: () => Promise<string>
  ) {}

  async getTenant(id: string): Promise<TenantProfile> {
    const data = await this.request(`/v1/tenants/${encodeURIComponent(id)}`, { method: 'GET' });
    return TenantProfileSchema.parse(data);
  }

  async createAppointment(payload: Omit<AppointmentSlot, 'slotId' | 'status'>): Promise<AppointmentSlot> {
    const data = await this.request('/v1/appointments', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    return AppointmentSlotSchema.parse(data);
  }

  private async request(endpoint: string, init: RequestInit): Promise<unknown> {
    const token = await this.tokenProvider();
    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...init.headers,
      },
    });
    if (!res.ok) {
      throw new Error(`AtlasCoreClientError: HTTP ${res.status} on ${endpoint}`);
    }
    return res.json();
  }
}
```