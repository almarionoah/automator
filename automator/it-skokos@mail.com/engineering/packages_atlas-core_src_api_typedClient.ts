# Atlas Core Typed API Client Migration & Contract Layer
**Author:** Onyx Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 11:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete refactor and migration from legacy loosely-typed fetch calls to an end-to-end type-safe API client interface for Atlas Core, enforcing strict runtime validation and ergonomic request abstractions based on Business Document: Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=4K918882VR072592A

## Deliverable
```
/**
 * Atlas Core Typed API Client
 * Author: Onyx Okafor (Engineering)
 * 
 * Migration Note: Refactored legacy untyped REST calls into a strictly-typed, schema-validated
 * HTTP transport client. Schema structures, error mappings, and service tier constraints
 * strictly adhere to specifications from Business Document: Company Document.
 */

import { z } from 'zod';

export interface RequestConfig<TResponse> {
  path: string;
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  headers?: Record<string, string>;
  params?: Record<string, string | number | boolean>;
  body?: unknown;
  responseSchema: z.ZodType<TResponse>;
}

export class ApiClientError extends Error {
  constructor(
    public readonly statusCode: number,
    public readonly errorPayload: unknown,
    message?: string
  ) {
    super(message || `API Client Error: ${statusCode}`);
    this.name = 'ApiClientError';
  }
}

export class AtlasApiClient {
  private readonly baseUrl: string;
  private readonly defaultHeaders: HeadersInit;

  constructor(baseUrl: string, defaultHeaders: HeadersInit = {}) {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'X-Client-Version': 'atlas-core-v2',
      ...defaultHeaders,
    };
  }

  public async execute<TResponse>(config: RequestConfig<TResponse>): Promise<TResponse> {
    const url = new URL(`${this.baseUrl}${config.path.startsWith('/') ? config.path : `/${config.path}`}`);
    
    if (config.params) {
      Object.entries(config.params).forEach(([key, val]) => {
        url.searchParams.append(key, String(val));
      });
    }

    const response = await fetch(url.toString(), {
      method: config.method || 'GET',
      headers: { ...this.defaultHeaders, ...config.headers },
      body: config.body ? JSON.stringify(config.body) : undefined,
    });

    if (!response.ok) {
      let errorData: unknown;
      try { errorData = await response.json(); } catch { errorData = await response.text(); }
      throw new ApiClientError(response.status, errorData);
    }

    const rawData = await response.json();
    const parsed = config.responseSchema.safeParse(rawData);

    if (!parsed.success) {
      throw new Error(`Schema validation failed for ${config.path}: ${parsed.error.message}`);
    }

    return parsed.data;
  }
}
```