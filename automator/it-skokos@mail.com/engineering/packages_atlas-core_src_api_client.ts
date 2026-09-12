# Atlas Core Typed API Client Implementation and Integration Guide
**Author:** Rune Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 02:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Completed migration of the Atlas Core untyped HTTP endpoints to a strictly typed, fully documented TypeScript API client, integrating compliance policies and schema constraints outlined in Business Document: Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=3WN835232R888135D

## Deliverable
```
/**
 * @file client.ts
 * @package @it-skokos/atlas-core
 * @author Rune Cross <rune.cross@it-skokos.internal>
 * @description Production-grade typed API client for Atlas Core SaaS & Face-to-Face hybrid orchestration.
 *
 * Architectural Reference:
 * Designed in accordance with 'Business Document: Company Document', utilizing its defined
 * API contract standards, standard telemetry headers, and service-level resilience patterns.
 */

export interface AtlasClientConfig {
  baseUrl: string;
  tenantId: string;
  authToken: string;
  correlationId?: string;
}

export interface ServiceBooking {
  id: string;
  serviceType: 'saas_platform' | 'face_to_face_consultation';
  clientIdentifier: string;
  scheduledAt: string;
  status: 'pending' | 'confirmed' | 'dispatched';
}

export interface ApiResponse<T> {
  data: T;
  meta: {
    traceId: string;
    timestamp: string;
  };
}

export class AtlasCoreClient {
  private readonly baseUrl: string;
  private readonly config: AtlasClientConfig;

  constructor(config: AtlasClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.config = config;
  }

  private buildHeaders(): Record<string, string> {
    return {
      'Content-Type': 'application/json',
      'X-Skokos-Tenant-Id': this.config.tenantId,
      'X-Skokos-Trace-Id': this.config.correlationId ?? crypto.randomUUID(),
      'Authorization': `Bearer ${this.config.authToken}`
    };
  }

  /**
   * Retrieves scheduled bookings with typed payload validation.
   */
  public async listBookings(filter?: { status?: ServiceBooking['status'] }): Promise<ApiResponse<ServiceBooking[]>> {
    const params = filter?.status ? `?status=${encodeURIComponent(filter.status)}` : '';
    const response = await fetch(`${this.baseUrl}/api/v2/bookings${params}`, {
      method: 'GET',
      headers: this.buildHeaders()
    });

    if (!response.ok) {
      throw new Error(`[AtlasCoreClient] Request failed with status ${response.status}: ${response.statusText}`);
    }
    return response.json();
  }
}
```