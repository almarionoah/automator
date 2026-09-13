# Atlas Core Typed API Client Migration
**Author:** Juno Petrov  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D18 23:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated legacy untyped API calls to a strictly typed, schema-validated client implementation in Atlas Core, referencing definitions from Business Document: Company Document.

## Deliverable
```
/**
 * Atlas Core Typed API Client
 * Engineering Author: Juno Petrov (Data Purist)
 * 
 * Resource Context:
 * - Business Document: Company Document was consulted to derive exact domain models,
 *   strict validation rules, and endpoint specifications for SaaS & Face-to-Face data pipelines.
 */

import { z } from 'zod';

// Core Schema Definitions derived from Business Document: Company Document
export const ServiceTypeSchema = z.enum(['SAAS_PLATFORM', 'FACE_TO_FACE']);

export const ServiceEngagementSchema = z.object({
  engagementId: z.string().uuid(),
  clientId: z.string().min(1),
  serviceType: ServiceTypeSchema,
  timestamp: z.string().datetime(),
  metadata: z.record(z.string(), z.unknown()),
});

export type ServiceEngagement = z.infer<typeof ServiceEngagementSchema>;

export const ApiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    status: z.enum(['success', 'error']),
    data: dataSchema,
    errorCode: z.string().optional(),
  });

export interface ApiClientConfig {
  baseUrl: string;
  headers?: Record<string, string>;
}

export class AtlasCoreApiClient {
  private baseUrl: string;
  private defaultHeaders: Record<string, string>;

  constructor(config: ApiClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/+$/, '');
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      ...config.headers,
    };
  }

  public async getEngagement(id: string): Promise<ServiceEngagement> {
    const response = await fetch(`${this.baseUrl}/engagements/${encodeURIComponent(id)}`, {
      method: 'GET',
      headers: this.defaultHeaders,
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    const rawJson = await response.json();
    const validated = ApiResponseSchema(ServiceEngagementSchema).parse(rawJson);
    
    return validated.data;
  }
}
```