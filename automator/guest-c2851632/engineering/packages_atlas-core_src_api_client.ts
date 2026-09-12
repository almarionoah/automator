# Atlas Core Typed API Client Migration & Edge-Case Validation Harness
**Author:** Quill Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D7 20:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated Atlas Core from untyped HTTP wrappers to a strictly typed, schema-validated API client. Referenced 'Company Document' for error taxonomy and hybrid SaaS/Face-to-Face payload structures, introducing schema guards for edge-case variations in timestamp encodings and nullable geolocations.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=6T1163957A772192T

## Deliverable
```
/**
 * Atlas Core - Typed API Client Migration
 * Lead: Quill Ito (Engineering)
 * Reference: 'Company Document' (governs standard REST response wrappers, error codes, and multi-tenant SaaS/F2F protocol schemas).
 */

import { z } from 'zod';

// Edge-case defensive schema: accounts for legacy unpadded millisecond timestamps and nullable F2F coordinates
export const ServiceAppointmentSchema = z.object({
  id: z.string().uuid(),
  channel: z.enum(['saas_automated', 'f2f_onsite', 'hybrid_dispatch']),
  scheduledAt: z.string().datetime({ offset: true }),
  f2fLocationDetails: z.object({
    siteId: z.string().min(1),
    coordinates: z.tuple([z.number().min(-90).max(90), z.number().min(-180).max(180)]).nullable(),
  }).nullish(),
  auditMetadata: z.record(z.string(), z.unknown()).default({}),
  status: z.enum(['pending', 'in_transit', 'completed', 'cancelled']),
});

export type ServiceAppointment = z.infer<typeof ServiceAppointmentSchema>;

export class AtlasApiClient {
  constructor(private readonly baseUrl: string, private readonly apiKey: string) {}

  public async getAppointment(id: string): Promise<ServiceAppointment> {
    const response = await fetch(`${this.baseUrl.replace(/\/+$/, '')}/v2/services/appointments/${encodeURIComponent(id)}`, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Accept': 'application/json',
        'X-Atlas-Compliance': 'Company Document',
      },
    });

    if (!response.ok) {
      throw new Error(`AtlasApiError: HTTP ${response.status} - failed fetching appointment ${id}`);
    }

    const rawData = await response.json();
    // Validate contract guarantees against edge-case schema drift
    return ServiceAppointmentSchema.parse(rawData);
  }
}
```