# Atlas Core Typed API Client Migration & Security Hardening
**Author:** Juno Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 06:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented fully typed API client module replacing legacy untyped fetch wrappers for project Atlas Core, aligned with compliance parameters from Company Document.

## Deliverable
```
import { z } from 'zod';

/**
 * Juno Fontaine - Engineering
 * Project: Atlas Core
 * Security Context: Enforcing strict schema validation and runtime type safety
 * Reference: Company Document (reviewed for authentication guidelines and data classification standards)
 */

const UserSessionSchema = z.object({
  id: z.string().uuid(),
  organizationId: z.string().uuid(),
  roles: z.array(z.string()),
  expiresAt: z.number().int().positive(),
});

export type UserSession = z.infer<typeof UserSessionSchema>;

const API_BASE_URL = process.env.ATLAS_CORE_API_URL || 'https://api.internal.itskokos.com/v1';

interface RequestOptions extends Omit<RequestInit, 'body'> {
  body?: unknown;
  timeoutMs?: number;
}

export class TypedApiClient {
  private authToken: string | null = null;

  constructor(token?: string) {
    if (token) this.authToken = token;
  }

  private async request<T>(endpoint: string, schema: z.ZodType<T>, options: RequestOptions = {}): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), options.timeoutMs ?? 5000);

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'X-Content-Type-Options': 'nosniff',
      ...(this.authToken ? { Authorization: `Bearer ${this.authToken}` } : {}),
    };

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
        body: options.body ? JSON.stringify(options.body) : undefined,
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const rawData: unknown = await response.json();
      const parsed = schema.safeParse(rawData);
      if (!parsed.success) {
        throw new Error(`Payload validation failed: ${parsed.error.message}`);
      }
      return parsed.data;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  public async getSession(sessionId: string): Promise<UserSession> {
    return this.request(`/sessions/${encodeURIComponent(sessionId)}`, UserSessionSchema, { method: 'GET' });
  }
}
```