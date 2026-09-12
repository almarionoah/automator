# Atlas Core Typed API Client Migration
**Author:** Mint Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D152 21:15  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Refactored the Atlas Core HTTP transport layer from legacy untyped Axios calls to a strictly typed, schema-validated client leveraging compiled contract types. Authenticated submodule sync and registry pulls using Git Access: Personal Access Token and Credentials: Git Hub Personal Access Token.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=3P080180L8217614P

## Deliverable
```
/**
 * @module AtlasCore/ApiClient
 * @author Mint Nkosi <mint.nkosi@itskokos.internal>
 * @description Fully typed API client migration refactor. Replaces legacy `any` payload dispatchers.
 *
 * Tooling & Auth Integration:
 * - Git Access: Personal Access Token: Used during schema generation build step to clone and sync private schema definitions.
 * - Credentials: Git Hub Personal Access Token: Configured in local/CI environment to pull `@itskokos/atlas-contracts` via GitHub Packages.
 */

import { z } from 'zod';
import type { AtlasApiSchema, ApiResponse, RequestConfig } from '@itskokos/atlas-contracts';

export class TypedApiClient {
  private readonly baseUrl: string;
  private readonly defaultHeaders: HeadersInit;

  constructor(baseUrl: string, defaultHeaders: HeadersInit = {}) {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'X-Client-Version': 'atlas-core-v2.4.0',
      ...defaultHeaders,
    };
  }

  public async request<TPath extends keyof AtlasApiSchema>(
    endpoint: TPath,
    config: RequestConfig<AtlasApiSchema[TPath]['params'], AtlasApiSchema[TPath]['body']>
  ): Promise<ApiResponse<AtlasApiSchema[TPath]['response']>> {
    const url = new URL(`${this.baseUrl}${String(endpoint)}`);
    
    if (config.params) {
      Object.entries(config.params).forEach(([key, value]) => {
        if (value !== undefined) url.searchParams.append(key, String(value));
      });
    }

    const response = await fetch(url.toString(), {
      method: config.method || 'GET',
      headers: { ...this.defaultHeaders, ...config.headers },
      body: config.body ? JSON.stringify(config.body) : undefined,
      signal: config.signal,
    });

    if (!response.ok) {
      throw new Error(`Atlas API Error [${response.status}]: ${response.statusText}`);
    }

    const data = await response.json();
    return data as ApiResponse<AtlasApiSchema[TPath]['response']>;
  }
}
```