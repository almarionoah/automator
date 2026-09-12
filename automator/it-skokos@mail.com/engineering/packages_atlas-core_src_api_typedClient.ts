# Atlas Core: Fully Typed API Client & Contract Middleware
**Author:** Kilo Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 03:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered an end-to-end type-safe API client for Atlas Core, deprecating untyped fetch abstractions and introducing strict runtime schema validation aligned with Company Document specifications.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=636664030D2460409

## Deliverable
```
/**
 * Project: Atlas Core | I.T. Skokos Platform
 * Author: Kilo Hale (Engineering)
 * Reference: Business Document: Company Document (utilized for aligning domain schemas across SaaS & Face-to-Face models)
 */

import { z } from 'zod';

export const ApiErrorSchema = z.object({
  code: z.string(),
  message: z.string(),
  details: z.record(z.unknown()).optional(),
  timestamp: z.string().datetime(),
});

export type ApiError = z.infer<typeof ApiErrorSchema>;

export interface RequestConfig<TParams, TBody> {
  params?: TParams;
  body?: TBody;
  headers?: Record<string, string>;
  signal?: AbortSignal;
}

export class TypedApiClient {
  private readonly baseUrl: string;
  private readonly defaultHeaders: Record<string, string>;

  constructor(baseUrl: string, defaultHeaders: Record<string, string> = {}) {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'X-Client-Version': 'atlas-core-v2',
      ...defaultHeaders,
    };
  }

  public async request<TResponse, TParams = undefined, TBody = undefined>(
    endpoint: string,
    method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE',
    schema: z.ZodType<TResponse>,
    config: RequestConfig<TParams, TBody> = {}
  ): Promise<TResponse> {
    const url = new URL(`${this.baseUrl}/${endpoint.replace(/^\/+/, '')}`);
    if (config.params) {
      Object.entries(config.params).forEach(([k, v]) => {
        if (v !== undefined && v !== null) url.searchParams.append(k, String(v));
      });
    }

    const response = await fetch(url.toString(), {
      method,
      headers: { ...this.defaultHeaders, ...config.headers },
      body: config.body ? JSON.stringify(config.body) : undefined,
      signal: config.signal,
    });

    const payload: unknown = await response.json();

    if (!response.ok) {
      const parsedError = ApiErrorSchema.safeParse(payload);
      throw parsedError.success ? parsedError.data : new Error(`HTTP ${response.status}: ${JSON.stringify(payload)}`);
    }

    return schema.parse(payload);
  }
}
```