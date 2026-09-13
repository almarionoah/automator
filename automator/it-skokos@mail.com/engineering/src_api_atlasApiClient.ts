# Atlas Core - Typed API Client Migration & Security Hardening
**Author:** Vex Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 23:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Completed migration of Atlas Core network layer to a strictly typed, schema-validated API client adhering to specifications from Business Document: Company Document. Added runtime payload verification and zero-trust header enforcement.

## Deliverable
```
/**
 * Project: Atlas Core
 * Module: Typed API Client Migration
 * Author: Vex Van Dyk (Engineering)
 * Reference: Business Document: Company Document (Section 4: Data Security & Transport Policies)
 *
 * Note: Replaced legacy loose fetch interfaces with strict typed contracts and
 * runtime Zod schema parsing to eliminate type pollution and untrusted data injection.
 */

import { z } from 'zod';

// Strict schemas enforced per Business Document: Company Document guidelines
export const AtlasUserSchema = z.object({
  id: z.string().uuid(),
  tenantId: z.string().min(1),
  role: z.enum(['admin', 'operator', 'auditor']),
  email: z.string().email(),
  mfaEnabled: z.boolean(),
  lastAuthenticatedAt: z.string().datetime()
}).strict();

export type AtlasUser = z.infer<typeof AtlasUserSchema>;

export interface ApiClientConfig {
  baseUrl: string;
  apiKey: string;
  timeoutMs?: number;
}

export class AtlasApiClient {
  private readonly baseUrl: string;
  private readonly apiKey: string;
  private readonly timeoutMs: number;

  constructor(config: ApiClientConfig) {
    if (!config.baseUrl.startsWith('https://')) {
      throw new Error('SECURITY VIOLATION: Insecure HTTP transport rejected.');
    }
    this.baseUrl = config.baseUrl.replace(/\/+$/, '');
    this.apiKey = config.apiKey;
    this.timeoutMs = config.timeoutMs ?? 5000;
  }

  private getHeaders(): HeadersInit {
    return {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json',
      'X-Client-Origin': 'Atlas-Core-Production',
      'X-Content-Type-Options': 'nosniff'
    };
  }

  public async getUser(userId: string): Promise<AtlasUser> {
    const sanitizedId = encodeURIComponent(userId.trim());
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(`${this.baseUrl}/v2/users/${sanitizedId}`, {
        method: 'GET',
        headers: this.getHeaders(),
        signal: controller.signal
      });

      if (!response.ok) {
        throw new Error(`API error: status ${response.status}`);
      }

      const rawData = await response.json();
      return AtlasUserSchema.parse(rawData);
    } finally {
      clearTimeout(timer);
    }
  }
}
```