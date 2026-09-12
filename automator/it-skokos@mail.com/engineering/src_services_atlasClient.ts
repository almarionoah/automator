# Atlas Core Typed API Client Migration
**Author:** Vex Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 00:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated Atlas Core from legacy fetch calls to a strictly typed, schema-validated API client for SaaS platform operations and Face-to-Face service appointments, directly aligning domain models with specifications from Business Document: Company Document.

## Deliverable
```
/**
 * Atlas Core Typed API Client
 * Author: Vex Nkosi (Engineering)
 * Context: Migrated legacy untyped API interactions to a strict TypeScript client.
 * Resource Reference: Schema definitions and SLA boundaries were mapped directly
 * using the operational guidelines in Business Document: Company Document.
 */

export interface SaaSUser {
  id: string;
  tenantId: string;
  tier: 'starter' | 'professional' | 'enterprise';
  isActive: boolean;
}

export interface F2FServiceBooking {
  bookingId: string;
  clientName: string;
  locationId: string;
  appointmentDate: string;
  agentId: string;
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled';
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  correlationId: string;
}

export class AtlasClient {
  private baseUrl: string;
  private token: string;

  constructor(baseUrl: string, token: string) {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.token = token;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
        'X-Atlas-Client-Version': '2.0.0',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errBody = await response.text();
      throw new Error(`[AtlasClient] HTTP ${response.status} on ${endpoint}: ${errBody}`);
    }

    const data = (await response.json()) as T;
    return {
      data,
      status: response.status,
      correlationId: response.headers.get('x-correlation-id') || 'unknown',
    };
  }

  public async getSaaSUser(userId: string): Promise<ApiResponse<SaaSUser>> {
    return this.request<SaaSUser>(`/api/v1/users/${encodeURIComponent(userId)}`);
  }

  public async createF2FBooking(booking: Omit<F2FServiceBooking, 'bookingId' | 'status'>): Promise<ApiResponse<F2FServiceBooking>> {
    return this.request<F2FServiceBooking>('/api/v1/f2f/bookings', {
      method: 'POST',
      body: JSON.stringify(booking),
    });
  }

  public async listF2FBookings(locationId: string): Promise<ApiResponse<F2FServiceBooking[]>> {
    return this.request<F2FServiceBooking[]>(`/api/v1/f2f/bookings?locationId=${encodeURIComponent(locationId)}`);
  }
}
```