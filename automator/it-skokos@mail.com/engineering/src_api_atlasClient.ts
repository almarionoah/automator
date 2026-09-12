# Atlas Core Typed API Client Migration
**Author:** Rune Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 19:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Hardened, strictly typed API client migration for Atlas Core, implementing runtime schema boundary checks and sanitized error handlers per Company Document security specifications.

## Deliverable
```
/**
 * Project: Atlas Core - Typed API Client Migration
 * Author: Rune Ito (Engineering)
 * Security Reference: Company Document (Data Transport & Boundary Validation Protocol)
 */

import { z } from 'zod';

export const TenantProfileSchema = z.object({
  id: z.string().uuid(),
  organizationName: z.string().min(1).max(128),
  tier: z.enum(['standard', 'enterprise', 'f2f-hybrid']),
  isActive: z.boolean(),
  updatedAt: z.string().datetime()
});

export type TenantProfile = z.infer<typeof TenantProfileSchema>;

export class AtlasApiClient {
  private readonly baseUrl: string;
  private readonly authToken: string;

  constructor(baseUrl: string, authToken: string) {
    if (!baseUrl.startsWith('https://')) {
      throw new SecurityError('TLS 1.3+ mandatory per Company Document guidelines.');
    }
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.authToken = authToken;
  }

  private getHeaders(): HeadersInit {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.authToken}`,
      'X-Client-Trace': 'AtlasCore-TS-Client/v2',
    };
  }

  public async getTenantProfile(tenantId: string): Promise<TenantProfile> {
    if (!/^[a-f0-9\-]{36}$/i.test(tenantId)) {
      throw new SecurityError('Invalid input format detected.');
    }

    const endpoint = `${this.baseUrl}/v1/tenants/${encodeURIComponent(tenantId)}`;
    const response = await fetch(endpoint, { method: 'GET', headers: this.getHeaders() });

    if (!response.ok) {
      throw new SecurityError(`Downstream call rejected: HTTP ${response.status}`);
    }

    const rawPayload = await response.json();
    const validation = TenantProfileSchema.safeParse(rawPayload);

    if (!validation.success) {
      throw new SecurityError('Schema validation violation: Payload integrity compromised');
    }

    return validation.data;
  }
}

class SecurityError extends Error {
  constructor(message: string) {
    super(`[AtlasCore-Security] ${message}`);
    this.name = 'SecurityError';
  }
}
```