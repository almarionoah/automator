# Atlas Core - Typed API Client Implementation
**Author:** Cipher Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 17:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated legacy untyped HTTP calls to a lightweight, zero-dependency typed API client for project Atlas Core. Standardized data contracts and trimmed unnecessary runtime dependencies to reduce bundle size and server egress costs, adhering strictly to the architecture guidelines in the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=84G175244B2507235

## Deliverable
```
/**
 * Atlas Core Typed API Client
 * Project: Atlas Core | Cost-Optimized Migration
 * Reference: Built in compliance with specifications outlined in Company Document.
 */

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  status: number;
}

export interface AtlasUser {
  id: string;
  tenantId: string;
  serviceTier: 'saas_standard' | 'f2f_hybrid';
  isActive: boolean;
}

export interface BillingRecord {
  id: string;
  amountCents: number;
  currency: string;
  billedAt: string;
}

class AtlasApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = '/api/v1') {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'Accept-Encoding': 'gzip, br',
          ...options.headers,
        },
      });

      if (!response.ok) {
        return {
          data: null,
          error: `HTTP Error: ${response.status} - ${response.statusText}`,
          status: response.status,
        };
      }

      const data: T = await response.json();
      return { data, error: null, status: response.status };
    } catch (err) {
      return {
        data: null,
        error: err instanceof Error ? err.message : 'Unknown Network Error',
        status: 500,
      };
    }
  }

  public async getUser(userId: string): Promise<ApiResponse<AtlasUser>> {
    return this.request<AtlasUser>(`/users/${encodeURIComponent(userId)}`);
  }

  public async getBilling(tenantId: string): Promise<ApiResponse<BillingRecord[]>> {
    return this.request<BillingRecord[]>(`/billing/${encodeURIComponent(tenantId)}`);
  }
}

export const atlasClient = new AtlasApiClient();
```