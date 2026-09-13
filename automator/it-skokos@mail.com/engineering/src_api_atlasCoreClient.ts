# Atlas Core Typed API Client Migration & Schema Validation
**Author:** Volt Petrov  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 00:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a strictly typed, runtime-validated API client for Atlas Core replacing untyped HTTP calls. Payload structures and error contracts were formally derived from the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=5E683950LK0998745

## Deliverable
```
import { z } from 'zod';

/**
 * Atlas Core Typed Client
 * Author: Volt Petrov (Engineering)
 * Specification Reference: 'Company Document' (governing SaaS & Face-to-Face data schemas)
 * Alignment: Enforces strict data contracts derived directly from the Company Document.
 */

// Domain Schemas
export const ServiceChannelEnum = z.enum(['SAAS_PLATFORM', 'FACE_TO_FACE']);

export const AtlasSessionSchema = z.object({
  sessionId: z.string().uuid(),
  channel: ServiceChannelEnum,
  tenantId: z.string().min(1),
  status: z.enum(['ACTIVE', 'SUSPENDED', 'TERMINATED']),
  metadata: z.record(z.string(), z.unknown()),
  updatedAt: z.string().datetime()
});

export const AppointmentRequestSchema = z.object({
  clientRef: z.string().min(1),
  serviceCode: z.string(),
  channel: ServiceChannelEnum,
  scheduledTime: z.string().datetime(),
  locationOverride: z.string().optional()
});

export type AtlasSession = z.infer<typeof AtlasSessionSchema>;
export type AppointmentRequest = z.infer<typeof AppointmentRequestSchema>;

export class AtlasCoreClient {
  private readonly baseUrl: string;
  private readonly headers: HeadersInit;

  constructor(baseUrl: string, apiKey: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.headers = {
      'Content-Type': 'application/json',
      'X-Atlas-Client': 'AtlasCoreTyped/v2.1',
      'Authorization': `Bearer ${apiKey}`
    };
  }

  private async request<T>(path: string, schema: z.ZodType<T>, init?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      ...init,
      headers: { ...this.headers, ...init?.headers }
    });

    if (!response.ok) {
      throw new Error(`[AtlasCore] HTTP ${response.status}: ${await response.text()}`);
    }

    const rawData = await response.json();
    const parsed = schema.safeParse(rawData);
    if (!parsed.success) {
      throw new Error(`[AtlasCore] Contract mismatch: ${JSON.stringify(parsed.error.format())}`);
    }
    return parsed.data;
  }

  public async getSession(sessionId: string): Promise<AtlasSession> {
    return this.request(`/v1/sessions/${sessionId}`, AtlasSessionSchema, { method: 'GET' });
  }

  public async createAppointment(payload: AppointmentRequest): Promise<AtlasSession> {
    const validatedPayload = AppointmentRequestSchema.parse(payload);
    return this.request('/v1/appointments', AtlasSessionSchema, {
      method: 'POST',
      body: JSON.stringify(validatedPayload)
    });
  }
}
```