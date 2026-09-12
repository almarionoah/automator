# Atlas Core Typed API Client Migration & Schema Specification
**Author:** Onyx Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 11:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored Atlas Core legacy untyped HTTP calls into an immutable, type-safe API client adhering to API contract and error handling standards established in the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=2X457655B6449440W

## Deliverable
```
/**
 * Atlas Core - Typed API Client Layer
 * Author: Onyx Cross (Engineering)
 * 
 * Migration Note: Refactored legacy untyped Axios/fetch invocations into a strictly
 * typed, zero-overhead API client. Endpoints and data schemas align directly with
 * specifications outlined in the 'Company Document' for hybrid SaaS and Face-to-Face operations.
 */

export interface ApiResponse<T> {
  readonly data: T;
  readonly status: number;
  readonly timestamp: string;
}

export interface SaaSTenantMetric {
  tenantId: string;
  activeWorkflows: number;
  quotaUtilization: number;
}

export interface FaceToFaceBooking {
  bookingId: string;
  specialistId: string;
  clientIdentifier: string;
  serviceLocation: 'corporate_hq' | 'field_branch' | 'client_site';
  scheduledStart: string;
  status: 'confirmed' | 'dispatched' | 'completed' | 'cancelled';
}

export interface EndpointMap {
  'GET /api/v1/saas/metrics': { response: SaaSTenantMetric[] };
  'POST /api/v1/f2f/bookings': { 
    request: Omit<FaceToFaceBooking, 'bookingId' | 'status'>; 
    response: FaceToFaceBooking; 
  };
  'PATCH /api/v1/f2f/bookings/:id': { 
    request: Partial<Pick<FaceToFaceBooking, 'serviceLocation' | 'scheduledStart' | 'status'>>; 
    response: FaceToFaceBooking; 
  };
}

export class AtlasApiClient {
  private readonly baseUrl: string;
  private readonly defaultHeaders: Readonly<Record<string, string>>;

  constructor(baseUrl: string, customHeaders: Record<string, string> = {}) {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.defaultHeaders = Object.freeze({
      'Content-Type': 'application/json',
      'X-Client-Spec': 'Company Document', // Referenced API governance standard
      ...customHeaders,
    });
  }

  public async call<E extends keyof EndpointMap>(
    endpoint: E,
    options?: {
      pathParams?: Record<string, string>;
      body?: EndpointMap[E] extends { request: infer R } ? R : never;
    }
  ): Promise<ApiResponse<EndpointMap[E]['response']>> {
    const [method, rawPath] = endpoint.split(' ') as [string, string];
    let resolvedPath = rawPath;

    if (options?.pathParams) {
      for (const [key, val] of Object.entries(options.pathParams)) {
        resolvedPath = resolvedPath.replace(`:${key}`, encodeURIComponent(val));
      }
    }

    const response = await fetch(`${this.baseUrl}${resolvedPath}`, {
      method,
      headers: this.defaultHeaders,
      body: options?.body ? JSON.stringify(options.body) : undefined,
    });

    if (!response.ok) {
      throw new Error(`[AtlasApiClient] ${method} ${resolvedPath} returned HTTP ${response.status}`);
    }

    const data: EndpointMap[E]['response'] = await response.json();
    return Object.freeze({
      data,
      status: response.status,
      timestamp: new Date().toISOString(),
    });
  }
}
```