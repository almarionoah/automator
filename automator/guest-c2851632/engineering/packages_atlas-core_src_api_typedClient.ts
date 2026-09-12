# Atlas Core Typed API Client Migration & Lightweight HTTP Layer
**Author:** Sable Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D7 03:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Replaced legacy untyped API requests with a zero-dependency, strongly typed client interface aligned with specifications from Business Document: Company Document to minimize cloud compute and memory overhead.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=8U1662758B222321M

## Deliverable
```
/**
 * Atlas Core - Typed API Client Layer
 * Author: Sable Hale (Engineering)
 * Specification Reference: Business Document: Company Document (utilized for endpoint schema verification and error model mapping).
 * Optimization: Built with zero runtime dependencies using native fetch to minimize runtime bundle costs.
 */

export interface AtlasApiResponse<T> {
  data: T | null;
  error: { code: string; message: string } | null;
  status: number;
}

export interface UserProfile {
  id: string;
  tenantId: string;
  tier: 'free' | 'pro' | 'enterprise';
  f2fServiceEnabled: boolean;
}

export interface ServiceBooking {
  bookingId: string;
  userId: string;
  serviceType: 'saas_consultation' | 'face_to_face_dispatch';
  scheduledTimestamp: number;
}

export class AtlasCoreClient {
  private readonly baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<AtlasApiResponse<T>> {
    const url = `${this.baseUrl}/${endpoint.replace(/^\//, '')}`;
    const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
    
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      return {
        data: null,
        error: { code: `ERR_${res.status}`, message: res.statusText },
        status: res.status
      };
    }
    const data = (await res.json()) as T;
    return { data, error: null, status: res.status };
  }

  public async getUser(userId: string): Promise<AtlasApiResponse<UserProfile>> {
    return this.request<UserProfile>(`users/${userId}`);
  }

  public async createBooking(payload: Omit<ServiceBooking, 'bookingId'>): Promise<AtlasApiResponse<ServiceBooking>> {
    return this.request<ServiceBooking>('bookings', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  }
}
```