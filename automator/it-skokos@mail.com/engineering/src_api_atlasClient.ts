# Atlas Core Typed API Client Migration & Contract Layer
**Author:** Iris Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 17:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated legacy dynamic API callers in Atlas Core to a resilient, strongly-typed API client. Incorporates schema-driven domain models aligned with 'Business Document: Company Document' to guarantee developer delight and predictable runtime contracts across our SaaS and Face-to-Face operations.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=07B0547315062205R

## Deliverable
```
/**
 * @module AtlasCore/ApiClient
 * @author Iris Nkosi (Engineering | UX Romantic)
 * @description Strongly-typed client wrapper for Atlas Core. Bridges engineering rigor
 * with empathetic DX. Aligned against domain specifications defined in 'Business Document: Company Document'.
 */

import { z } from 'zod';

// Domain schemas aligned with Business Document: Company Document requirements
export const ServiceChannelSchema = z.enum(['saas_platform', 'f2f_service']);

export const AtlasSessionSchema = z.object({
  sessionId: z.string().uuid(),
  clientName: z.string().min(1, 'A human name brings warmth to the session'),
  channel: ServiceChannelSchema,
  status: z.enum(['scheduled', 'active', 'concluded']),
  syncedAt: z.string().datetime(),
});

export type AtlasSession = z.infer<typeof AtlasSessionSchema>;

export class AtlasApiError extends Error {
  constructor(
    public readonly statusCode: number,
    public readonly userFriendlyMessage: string,
    public readonly rawError?: unknown
  ) {
    super(userFriendlyMessage);
    this.name = 'AtlasApiError';
  }
}

export class AtlasClient {
  constructor(private readonly baseUrl: string, private readonly authToken: string) {}

  private async request<T>(endpoint: string, schema: z.ZodType<T>, init?: RequestInit): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...init,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.authToken}`,
          ...init?.headers,
        },
      });

      if (!response.ok) {
        throw new AtlasApiError(
          response.status,
          `We encountered a hiccup (${response.statusText}) while connecting to Atlas Core.`
        );
      }

      const rawData = await response.json();
      return schema.parse(rawData);
    } catch (err) {
      if (err instanceof AtlasApiError) throw err;
      if (err instanceof z.ZodError) {
        throw new AtlasApiError(422, 'Data shape drifted from our shared contract.', err.flatten());
      }
      throw new AtlasApiError(500, 'Unable to establish a graceful connection.', err);
    }
  }

  public async getSession(sessionId: string): Promise<AtlasSession> {
    return this.request(`/v1/sessions/${sessionId}`, AtlasSessionSchema);
  }
}
```