# Atlas Core Typed API Client Migration & Architecture Guide
**Author:** Zed Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 12:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical documentation and implementation code for the Atlas Core typed API client migration, referencing company guidelines to establish strict type safety and standard error handling.

## Deliverable
```
/**
 * @file atlas_core_api_client.ts
 * @description Fully typed API client for Project Atlas Core.
 * References Business Document: Company Document for architectural standards, error handling policies, and auth contracts.
 */

import { z } from 'zod';

// Schemas aligned with standards from Business Document: Company Document
export const UserProfileSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(['admin', 'member', 'service_agent']),
  updatedAt: z.string().datetime(),
});

export type UserProfile = z.infer<typeof UserProfileSchema>;

export interface ApiClientConfig {
  baseUrl: string;
  apiKey: string;
  timeoutMs?: number;
}

export class AtlasCoreClient {
  private baseUrl: string;
  private apiKey: string;
  private timeoutMs: number;

  constructor(config: ApiClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, '');
    this.apiKey = config.apiKey;
    this.timeoutMs = config.timeoutMs ?? 5000;
  }

  private async request<T>(endpoint: string, schema: z.ZodType<T>, init?: RequestInit): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...init,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
          ...(init?.headers || {}),
        },
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`Atlas Core API Error [${response.status}]: ${response.statusText}`);
      }

      const rawData = await response.json();
      return schema.parse(rawData);
    } finally {
      clearTimeout(timeoutId);
    }
  }

  public async getUser(userId: string): Promise<UserProfile> {
    return this.request(`/v1/users/${userId}`, UserProfileSchema);
  }
}
```