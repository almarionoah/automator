# Atlas Core Typed API Client Migration & Interface Definition
**Author:** Juno Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 05:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a strongly typed, developer-ergonomic TypeScript API client for Atlas Core. Explicitly referenced Business Document: Company Document to align schema contracts, endpoint paths, and service tier configurations for both SaaS and Face-to-Face touchpoints.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=6E5980630R467274W

## Deliverable
```
/**
 * Atlas Core - Typed API Client Module
 * Crafted by: Juno Nkosi (Engineering)
 *
 * Note on Architecture & UX Romanticism:
 * Software architecture should feel seamless, intuitive, and respectful of developer focus.
 * This typed migration replaces fragile untyped fetch calls with resilient schema-driven interfaces.
 *
 * Resource Integration:
 * - Business Document: Company Document: Explicitly consulted to map domain entities, error hierarchies,
 *   and authentication lifecycle requirements for SaaS and Face-to-Face hybrid service bookings.
 */

import { z } from 'zod';

export const CustomerProfileSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1, 'Name is required for humanized touchpoints'),
  email: z.string().email(),
  serviceTier: z.enum(['saas_self_serve', 'hybrid_managed', 'executive_face_to_face']),
  locale: z.string().default('en-US'),
  updatedAt: z.string().datetime(),
});

export const ServiceAppointmentSchema = z.object({
  appointmentId: z.string().uuid(),
  customerId: z.string().uuid(),
  modality: z.enum(['digital_session', 'in_person_face_to_face']),
  scheduledTimestamp: z.string().datetime(),
  confirmed: z.boolean(),
});

export type CustomerProfile = z.infer<typeof CustomerProfileSchema>;
export type ServiceAppointment = z.infer<typeof ServiceAppointmentSchema>;

export class AtlasCoreClient {
  constructor(private readonly baseUrl: string, private readonly apiKey: string) {}

  private async request<T>(path: string, schema: z.ZodType<T>, init?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`,
        ...init?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`[AtlasCore Client Error]: Request to ${path} failed with status ${response.status}`);
    }

    const data = await response.json();
    return schema.parse(data);
  }

  public readonly customers = {
    getById: (id: string) => this.request(`/v2/customers/${id}`, CustomerProfileSchema),
  };

  public readonly appointments = {
    schedule: (payload: Omit<ServiceAppointment, 'appointmentId' | 'confirmed'>) =>
      this.request('/v2/appointments', ServiceAppointmentSchema, {
        method: 'POST',
        body: JSON.stringify(payload),
      }),
  };
}
```