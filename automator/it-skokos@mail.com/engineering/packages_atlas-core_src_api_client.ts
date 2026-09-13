# Atlas Core Typed API Client Migration Spec & Implementation
**Author:** Vex Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 06:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Type-safe, ergonomically crafted API client wrapper for Atlas Core, replacing legacy dynamic fetch calls with strongly-typed contracts aligned with the standard architecture in Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=7GW84465E1168510L

## Deliverable
```
/**
 * @file Atlas Core - Strongly-Typed API Client
 * @author Vex Adeyemi <vex@itskokos.internal>
 * 
 * In alignment with the integration requirements from Business Document: Company Document,
 * this module introduces an expressive, strongly-typed API layer engineered for developer
 * ergonomics and resilient user experiences across our SaaS and F2F touchpoints.
 */

import { z } from 'zod';

export const CustomerProfileSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  tier: z.enum(['standard', 'premium', 'concierge']),
  f2fConsultationBooked: z.boolean(),
  lastActive: z.string().datetime(),
});

export type CustomerProfile = z.infer<typeof CustomerProfileSchema>;

export interface RequestOptions extends RequestInit {
  timeoutMs?: number;
}

export class AtlasApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  private async request<T>(path: string, schema: z.ZodType<T>, options: RequestOptions = {}): Promise<T> {
    const { timeoutMs = 8000, ...fetchOpts } = options;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const response = await fetch(`${this.baseUrl}${path}`, {
        ...fetchOpts,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...fetchOpts.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`[Atlas API Error] ${response.status}: ${response.statusText}`);
      }

      const rawData = await response.json();
      return schema.parse(rawData);
    } finally {
      clearTimeout(timeoutId);
    }
  }

  public customer = {
    getById: (id: string, opts?: RequestOptions): Promise<CustomerProfile> =>
      this.request(`/v1/customers/${id}`, CustomerProfileSchema, { method: 'GET', ...opts }),
  };
}
```