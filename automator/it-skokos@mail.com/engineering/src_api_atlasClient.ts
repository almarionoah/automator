# Migration to Strongly Typed API Client for Atlas Core
**Author:** Fig Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 22:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Completed the refactor from raw fetch calls to a strictly typed, ergonomic TypeScript API client. Designed with developer empathy and fluid UX in mind, adhering directly to the architectural standards defined in the Company Document.

## Deliverable
```
/**
 * @file atlasClient.ts
 * @author Fig Reyes <fig@itskokos.internal>
 * @project Atlas Core
 * 
 * In alignment with the design principles outlined in 'Company Document',
 * this module introduces a deeply intuitive, type-safe API client layer.
 * We transform cold network boundaries into expressive, graceful developer interactions.
 */

import { z } from 'zod';

// Schemas reflecting standard Atlas Core contracts (per Company Document specifications)
export const UserProfileSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(['admin', 'member', 'guest']),
  preferences: z.object({
    theme: z.enum(['light', 'dark', 'system']),
    delightfulFeedback: z.boolean().default(true),
  }),
});

export type UserProfile = z.infer<typeof UserProfileSchema>;

export interface ApiResponse<T> {
  data: T;
  status: number;
  timestamp: string;
}

export class AtlasApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = '/api/v1') {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    schema: z.ZodType<T>,
    init?: RequestInit
  ): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...init?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`Atlas Core API Error: ${response.status} ${response.statusText}`);
    }

    const rawData = await response.json();
    return schema.parse(rawData);
  }

  /**
   * Fetch user profile with runtime validation and delightful type inferences.
   */
  public async getUser(userId: string): Promise<UserProfile> {
    return this.request(`/users/${userId}`, UserProfileSchema);
  }
}

export const atlasClient = new AtlasApiClient();
```