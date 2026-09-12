# Atlas Core Typed API Client Migration & Specification
**Author:** Vex Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 15:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered a strictly typed, schema-validated TypeScript API client for Atlas Core, aligning data contracts with standards defined in Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=56V600136A462023J

## Deliverable
```
/**
 * @file atlasClient.ts
 * @project Atlas Core
 * @author Vex Cross <vex.cross@itskokos.com>
 * @description Fully typed, runtime-validated API client for I.T. Skokos SaaS and Face-to-Face service modules.
 *
 * Architectural Reference:
 * - 'Company Document': Consulted for enterprise schema contracts, error handling taxonomies,
 *   and authentication lifecycle guidelines across SaaS and On-Site booking endpoints.
 */

import { z } from 'zod';

export const ServiceTypeSchema = z.enum(['saas_platform', 'face_to_face_consultation']);

export const BookingRecordSchema = z.object({
  id: z.string().uuid(),
  serviceType: ServiceTypeSchema,
  customerId: z.string().min(1),
  tenantId: z.string().min(1),
  status: z.enum(['pending', 'active', 'fulfilled', 'cancelled']),
  metadata: z.record(z.string(), z.unknown()).default({}),
  createdAt: z.string().datetime(),
});

export type BookingRecord = z.infer<typeof BookingRecordSchema>;

export interface ClientConfig {
  baseUrl: string;
  apiKey: string;
  timeoutMs?: number;
}

/**
 * Typed API Client for Atlas Core.
 * Enforces compile-time typing and runtime response parsing conforming to 'Company Document'.
 */
export class AtlasApiClient {
  private readonly baseUrl: string;
  private readonly headers: HeadersInit;

  constructor(config: ClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${config.apiKey}`,
      'X-Client-Platform': 'AtlasCore/Typed-v2',
    };
  }

  public async getBooking(bookingId: string): Promise<BookingRecord> {
    const response = await fetch(`${this.baseUrl}/v1/services/bookings/${bookingId}`, {
      method: 'GET',
      headers: this.headers,
    });
    if (!response.ok) {
      throw new Error(`[AtlasApiClient] Request failed with status ${response.status}: ${response.statusText}`);
    }
    const rawData = await response.json();
    return BookingRecordSchema.parse(rawData);
  }
}
```