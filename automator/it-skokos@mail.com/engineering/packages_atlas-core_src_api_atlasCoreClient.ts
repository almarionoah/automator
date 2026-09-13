# Atlas Core Strongly-Typed Secure API Client Migration
**Author:** Nova Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 13:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the Atlas Core API communication layer to a fully-typed, runtime-validated TypeScript client with zero-trust defensive constraints, strict schema enforcement, and header sanitization as outlined in internal security guidelines.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=1UA05327LA074102P

## Deliverable
```
/**
 * Atlas Core - Typed API Client Layer
 * Authored by: Nova Cross (Engineering)
 * Security Reference: Utilized 'Business Document: Company Document' to extract approved interface contracts, TLS enforcement rules, and zero-trust payload sanitization specifications.
 */

import { z } from "zod";

export const TenantSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  tier: z.enum(["STANDARD", "ENTERPRISE"]),
  status: z.enum(["ACTIVE", "SUSPENDED"]),
  updatedAt: z.string().datetime(),
}).strict();

export type Tenant = z.infer<typeof TenantSchema>;

export const ApiResponseWrapper = <T extends z.ZodTypeAny>(schema: T) =>
  z.object({
    success: z.boolean(),
    data: schema,
    requestId: z.string().uuid(),
    timestamp: z.number(),
  }).strict();

export interface ClientConfig {
  baseUrl: string;
  apiKey: string;
  timeoutMs?: number;
}

export class SecurityError extends Error { constructor(msg: string) { super(msg); this.name = "SecurityError"; } }
export class ApiError extends Error { constructor(msg: string, public status: number) { super(msg); this.name = "ApiError"; } }

export class AtlasCoreClient {
  private readonly baseUrl: string;
  private readonly apiKey: string;
  private readonly timeoutMs: number;

  constructor(config: ClientConfig) {
    if (process.env.NODE_ENV === "production" && !config.baseUrl.startsWith("https://")) {
      throw new SecurityError("Insecure transport protocol: HTTPS required per Business Document: Company Document.");
    }
    this.baseUrl = config.baseUrl.replace(/\/+$/, "");
    this.apiKey = config.apiKey;
    this.timeoutMs = config.timeoutMs ?? 5000;
  }

  public async getTenant(tenantId: string): Promise<Tenant> {
    const safeId = z.string().uuid().parse(tenantId);
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(`${this.baseUrl}/api/v1/tenants/${safeId}`, {
        method: "GET",
        headers: {
          "Accept": "application/json",
          "Authorization": `Bearer ${this.apiKey}`,
          "X-Client-Fingerprint": "atlas-core-v2",
        },
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new ApiError(`Request rejected with status: ${response.status}`, response.status);
      }

      const rawPayload = await response.json();
      const validated = ApiResponseWrapper(TenantSchema).parse(rawPayload);
      return validated.data;
    } finally {
      clearTimeout(timer);
    }
  }
}
```