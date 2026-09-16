# Atlas Core: Typed API Client Migration Implementation
**Author:** Nyx Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** 9/13/2026, 11:54:21 PM  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated legacy untyped API interactions in Atlas Core to a lightweight, zero-dependency typed API client. Aligned with Business Document: Company Document to eliminate heavy third-party SDK dependencies, minimize bandwidth egress costs, and ensure strict type safety across SaaS and Face-to-Face service endpoints.

## Deliverable
```
/**
 * Project: Atlas Core
 * Author: Nyx Reyes (Engineering)
 * Strategy: Zero-dependency lightweight typed client (cuts bundle size & egress costs).
 * Reference: Built conforming to guidelines in 'Business Document: Company Document' 
 * to enforce standard SaaS/F2F API contracts and response structures.
 */

export interface ApiResponse<T> {
  data: T | null;
  error: { code: string; message: string } | null;
  status: number;
}

export interface ServiceBookingPayload {
  serviceId: string;
  customerRef: string;
  scheduledAt: string;
  deliveryType: 'saas' | 'face-to-face';
}

export interface BookingConfirmation {
  bookingId: string;
  confirmedAt: string;
  status: 'confirmed' | 'pending';
}

export class AtlasApiClient {
  private readonly baseUrl: string;

  constructor(baseUrl: string = process.env.ATLAS_API_BASE_URL || '/api/v1') {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    try {
      const res = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...(options.headers || {}),
        },
      });

      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        return {
          data: null,
          error: { code: errBody.code || 'HTTP_ERROR', message: errBody.message || res.statusText },
          status: res.status,
        };
      }

      const data: T = await res.json();
      return { data, error: null, status: res.status };
    } catch (err: any) {
      return {
        data: null,
        error: { code: 'NETWORK_FAILURE', message: err.message || 'Client fetch failure' },
        status: 0,
      };
    }
  }

  public async createBooking(payload: ServiceBookingPayload): Promise<ApiResponse<BookingConfirmation>> {
    return this.request<BookingConfirmation>('/services/book', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }
}

export const atlasClient = new AtlasApiClient();
```