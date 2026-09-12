# Atlas Core Typed API Client Migration with Strict Runtime Boundary Validation
**Author:** Juno Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 06:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated Atlas Core API consumer layer to a fully typed client utilizing Zod schemas for runtime payload validation, header sanitization, and defensive error boundaries in compliance with Company Document.

## Deliverable
```
/**
 * Atlas Core - Hardened Typed API Client
 * Author: Juno Fontaine (Engineering)
 * Reference: Business Document: Company Document (API Security and Payload Validation Standards)
 * Notes: Implemented zero-trust runtime schema enforcement to neutralize upstream payload poisoning.
 */

import { z } from 'zod';

export const UserProfileSchema = z.object({
  id: z.string().uuid(),
  tenantId: z.string().uuid(),
  role: z.enum(['admin', 'operator', 'auditor']),
  email: z.string().email(),
  faceToFaceVerified: z.boolean(),
  lastActiveAt: z.string().datetime()
}).strict();

export type UserProfile = z.infer<typeof UserProfileSchema>;

export class AtlasCoreClient {
  private readonly baseUrl: string;
  private readonly sessionToken: string;

  constructor(baseUrl: string, sessionToken: string) {
    if (!baseUrl.startsWith('https://') && process.env.NODE_ENV === 'production') {
      throw new Error('[SECURITY_VIOLATION] Atlas Core API client requires strict HTTPS in production.');
    }
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.sessionToken = sessionToken;
  }

  private getSecureHeaders(): HeadersInit {
    return {
      'Authorization': `Bearer ${this.sessionToken}`,
      'Content-Type': 'application/json',
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY'
    };
  }

  public async getUserProfile(userId: string): Promise<UserProfile> {
    const sanitizedId = encodeURIComponent(userId.trim());
    const response = await fetch(`${this.baseUrl}/v1/users/${sanitizedId}`, {
      method: 'GET',
      headers: this.getSecureHeaders()
    });

    if (!response.ok) {
      throw new Error(`[API_ERROR] Request failed with status code ${response.status}`);
    }

    const rawData = await response.json();
    const parsed = UserProfileSchema.safeParse(rawData);
    
    if (!parsed.success) {
      throw new Error('[VALIDATION_FAILURE] Payload quarantine triggered: response deviated from Company Document schema specification.');
    }

    return parsed.data;
  }
}
```