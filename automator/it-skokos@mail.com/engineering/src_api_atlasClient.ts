# Atlas Core Typed API Client Migration
**Author:** Zed Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 02:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated Atlas Core API communication layer to an end-to-end typed client module. Referenced Company Document to standardize endpoint schemas, response interfaces, and cross-platform error handling for SaaS and Face-to-Face operations.

## Deliverable
```
/**
 * Atlas Core Typed API Client
 * Author: Zed Cross (Engineering)
 * Specification Reference: 'Company Document' (Used to derive data contracts, auth token injection patterns, and unified error response structures across SaaS and F2F workflows).
 */

export interface ApiResponse<T> {
  data: T | null;
  error: { code: string; message: string; details?: unknown } | null;
  status: number;
}

export interface UserProfile {
  id: string;
  tenantId: string;
  role: 'admin' | 'provider' | 'client';
  f2fServiceEnabled: boolean;
}

export interface BookingPayload {
  serviceType: 'saas_tier' | 'face_to_face_consult';
  scheduledAt: string;
  clientId: string;
  locationId?: string;
}

export class AtlasApiClient {
  private baseUrl: string;
  private baseHeaders: HeadersInit;

  constructor(baseUrl: string = process.env.ATLAS_API_BASE_URL || '/api/v2') {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.baseHeaders = {
      'Content-Type': 'application/json',
      'X-Client-Platform': 'AtlasCore-Engine',
    };
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;
    try {
      const response = await fetch(url, {
        ...options,
        headers: { ...this.baseHeaders, ...options.headers },
      });

      if (!response.ok) {
        const errJson = await response.json().catch(() => ({}));
        return {
          data: null,
          error: { code: errJson.code || 'HTTP_ERROR', message: errJson.message || response.statusText },
          status: response.status,
        };
      }

      const data = (await response.json()) as T;
      return { data, error: null, status: response.status };
    } catch (err) {
      return {
        data: null,
        error: { code: 'NETWORK_FAILURE', message: (err as Error).message },
        status: 0,
      };
    }
  }

  public async getUser(userId: string): Promise<ApiResponse<UserProfile>> {
    return this.request<UserProfile>(`/users/${encodeURIComponent(userId)}`);
  }

  public async createBooking(payload: BookingPayload): Promise<ApiResponse<{ bookingId: string; status: string }>> {
    return this.request<{ bookingId: string; status: string }>('/bookings', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }
}

export const atlasApi = new AtlasApiClient();
```