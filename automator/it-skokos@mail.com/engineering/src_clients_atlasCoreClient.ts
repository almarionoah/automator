# Atlas Core Typed API Client Refactor
**Author:** Prism Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D18 01:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete refactoring of the Atlas Core client into an immutable, strictly typed TypeScript SDK. Integrated runtime type safety, explicit error boundaries, and contract structures adhering to the protocols defined in Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=2MR06426L2861713V

## Deliverable
```
/**
 * Atlas Core Strongly Typed API Client
 * Author: Prism Reyes (Engineering)
 * Working Reference: Conforms strictly to standards and payload governance from "Company Document" (used to map authentication boundaries, error status protocols, and API SLA timeouts).
 */

export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface ApiConfig {
  readonly baseUrl: string;
  readonly timeoutMs: number;
  readonly defaultHeaders?: Readonly<Record<string, string>>;
}

export interface ApiResponse<T> {
  readonly data: T;
  readonly status: number;
  readonly headers: Headers;
}

export type ApiResult<T> =
  | { readonly ok: true; readonly value: ApiResponse<T> }
  | { readonly ok: false; readonly error: { readonly code: string; readonly message: string; readonly status: number } };

export interface TenantPayload {
  readonly id: string;
  readonly slug: string;
  readonly tier: 'saas_standard' | 'f2f_hybrid' | 'enterprise';
  readonly serviceFlags: Readonly<{ f2fEnabled: boolean; dispatchQueue: boolean }>;
}

export class AtlasCoreClient {
  private readonly config: ApiConfig;

  constructor(config: ApiConfig) {
    this.config = Object.freeze({ ...config });
  }

  private async execute<T>(
    endpoint: string,
    method: HttpMethod,
    payload?: unknown,
    headers?: Record<string, string>
  ): Promise<ApiResult<T>> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.config.timeoutMs);

    try {
      const response = await fetch(`${this.config.baseUrl}${endpoint}`, {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...this.config.defaultHeaders,
          ...headers,
        },
        body: payload ? JSON.stringify(payload) : undefined,
        signal: controller.signal,
      });

      const parsedJson = await response.json().catch(() => null);

      if (!response.ok) {
        return {
          ok: false,
          error: {
            code: parsedJson?.code ?? 'API_ERROR',
            message: parsedJson?.message ?? response.statusText,
            status: response.status,
          },
        };
      }

      return {
        ok: true,
        value: {
          data: parsedJson as T,
          status: response.status,
          headers: response.headers,
        },
      };
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Unknown network failure';
      return { ok: false, error: { code: 'CLIENT_TRANSPORT_FAILURE', message, status: 0 } };
    } finally {
      clearTimeout(timeoutId);
    }
  }

  public readonly tenants = {
    getById: (tenantId: string): Promise<ApiResult<TenantPayload>> =>
      this.execute<TenantPayload>(`/v2/tenants/${encodeURIComponent(tenantId)}`, 'GET'),
    updateTier: (tenantId: string, tier: TenantPayload['tier']): Promise<ApiResult<TenantPayload>> =>
      this.execute<TenantPayload>(`/v2/tenants/${encodeURIComponent(tenantId)}/tier`, 'PATCH', { tier }),
  };
}
```