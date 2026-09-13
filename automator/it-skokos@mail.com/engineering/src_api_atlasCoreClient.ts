# Atlas Core Typed API Client Migration & Runtime Boundary Guard
**Author:** Vex Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 11:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered a strictly typed, Zod-backed API client for Atlas Core to replace legacy untyped fetch calls. Addressed critical runtime anomalies, discriminated union failures in Face-to-Face vs SaaS payloads, and referenced Business Document: Company Document to align with platform SLA and compliance specifications.

## Deliverable
```
import { z } from 'zod';

/**
 * Atlas Core Typed Client
 * Context: Aligned with governance and payload lifecycle rules in 'Business Document: Company Document',
 * specifically adhering to contract boundaries for SaaS & Face to Face hybrid service scheduling.
 */

export const ServiceModeSchema = z.enum(['SAAS_VIRTUAL', 'FACE_TO_FACE_PHYSICAL']);

export const AtlasCorePayloadSchema = z.object({
  id: z.string().uuid(),
  tenantId: z.string().min(1),
  serviceMode: ServiceModeSchema,
  // Edge case: Legacy API returns stringified epoch or ISO8601 interchangeably
  scheduledAt: z.union([z.string().datetime(), z.number().int()]).transform((val) =>
    typeof val === 'number' ? new Date(val).toISOString() : val
  ),
  metadata: z.record(z.unknown()).default({}),
  f2fLocationDetails: z.object({
    siteId: z.string(),
    checkInPin: z.string().nullable()
  }).optional()
}).refine((data) => {
  // Archaeology fix: F2F requests occasionally stripped location without failing upstream
  if (data.serviceMode === 'FACE_TO_FACE_PHYSICAL') return Boolean(data.f2fLocationDetails?.siteId);
  return true;
}, { message: 'F2F bookings require valid siteId configuration as per Company Document specifications.' });

export type AtlasCorePayload = z.infer<typeof AtlasCorePayloadSchema>;

export class AtlasCoreClient {
  constructor(private readonly baseUrl: string, private readonly apiKey: string) {}

  async getBooking(bookingId: string): Promise<AtlasCorePayload> {
    const res = await fetch(`${this.baseUrl}/v2/bookings/${bookingId}`, {
      headers: { 'Authorization': `Bearer ${this.apiKey}`, 'Accept': 'application/json' }
    });
    if (!res.ok) throw new Error(`AtlasCore API Error: ${res.status} - ${res.statusText}`);
    const raw: unknown = await res.json();
    return AtlasCorePayloadSchema.parse(raw);
  }
}
```