# Atlas Core: Typed API Client Migration
**Author:** Rune Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 20:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Completed migration of Atlas Core legacy HTTP calls to a strict, typed API client. Standardized endpoint interfaces for SaaS platform operations and Face-to-Face service bookings based on specifications in Business Document: Company Document.

## Deliverable
```
/**
 * Atlas Core - Typed API Client
 * Author: Rune Bishop
 * 
 * Resource Reference: Business Document: Company Document
 * Usage: Endpoint routes, request payload contracts, and error response models
 * were mapped directly from the interface specifications outlined in Business Document: Company Document.
 */

export interface ApiResponse<T> {
  data: T;
  status: number;
  timestamp: string;
}

export interface SaaSBookingPayload {
  tenantId: string;
  serviceType: 'saas_platform' | 'f2f_service';
  clientReference: string;
  scheduledAt?: string;
  metadata?: Record<string, unknown>;
}

export interface BookingResult {
  id: string;
  status: 'confirmed' | 'pending' | 'failed';
  confirmationCode: string;
}

export class AtlasApiClient {
  private baseUrl: string;
  private defaultHeaders: HeadersInit;

  constructor(baseUrl: string, apiKey: string) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
      'X-Client-Version': 'atlas-core-v2',
    };
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: { ...this.defaultHeaders, ...options.headers },
    });

    if (!response.ok) {
      const errorBody = await response.text();
      throw new Error(`[Atlas API Error] ${response.status}: ${errorBody}`);
    }

    return response.json();
  }

  public async createBooking(payload: SaaSBookingPayload): Promise<ApiResponse<BookingResult>> {
    return this.request<BookingResult>('/v1/services/booking', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  public async getHealth(): Promise<{ status: string }> {
    const res = await this.request<{ status: string }>('/health');
    return res.data;
  }
}

export const apiClient = new AtlasApiClient(
  process.env.ATLAS_API_BASE_URL || 'https://api.itskokos.internal',
  process.env.ATLAS_API_KEY || ''
);
```