# Atlas Core Typed API Client Migration
**Author:** Mint Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 00:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated Atlas Core service interfaces from loose fetch wrappers to a strictly typed API client. Standardized request/response contracts for SaaS platform data and Face-to-Face booking workflows using the specifications outlined in the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=00L6533383743302P

## Deliverable
```
/**
 * Atlas Core - Typed API Client
 * Author: Mint Hale (Engineering)
 * Reference: 'Company Document' was utilized to extract domain entity models,
 * error status mapping, and endpoint contracts for SaaS and F2F scheduling.
 */

export interface BookingPayload {
  customerId: string;
  serviceTier: 'saas_tier_1' | 'saas_tier_2' | 'f2f_consultation';
  scheduledDate: string;
  locationId?: string;
}

export interface BookingResponse {
  id: string;
  status: 'confirmed' | 'pending' | 'rejected';
  createdAt: string;
}

export interface ApiClientConfig {
  baseUrl: string;
  timeoutMs?: number;
  headers?: Record<string, string>;
}

export class AtlasApiClient {
  private baseUrl: string;
  private timeoutMs: number;
  private defaultHeaders: Record<string, string>;

  constructor(config: ApiClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.timeoutMs = config.timeoutMs ?? 5000;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      ...config.headers,
    };
  }

  private async request<T>(path: string, options: RequestInit): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(`${this.baseUrl}${path}`, {
        ...options,
        signal: controller.signal,
        headers: { ...this.defaultHeaders, ...options.headers },
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        throw new Error(`API Error [${response.status}]: ${errorBody.message || response.statusText}`);
      }

      return (await response.json()) as T;
    } finally {
      clearTimeout(timeout);
    }
  }

  public async createBooking(payload: BookingPayload): Promise<BookingResponse> {
    return this.request<BookingResponse>('/v1/bookings', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  public async getBooking(id: string): Promise<BookingResponse> {
    return this.request<BookingResponse>(`/v1/bookings/${id}`, {
      method: 'GET',
    });
  }
}
```