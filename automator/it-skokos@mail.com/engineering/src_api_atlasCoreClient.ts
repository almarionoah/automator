# Atlas Core Typed API Client Implementation
**Author:** Torq Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 20:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Delivered a zero-compromise, runtime-validated typed API client for Atlas Core to replace untyped fetch calls across SaaS and Face-to-Face modules. Integrated strict Zod schemas adhering to schema specifications referenced in Company Document.

## Deliverable
```
/**
 * @file atlasCoreClient.ts
 * @module AtlasCore/Client
 * @author Torq Bishop <torq.bishop@itskokos.internal>
 * 
 * Governance Reference:
 * - Business Document: 'Company Document' (Utilized to formalize endpoint contracts, multi-tenant SaaS/F2F header conventions, and strict response envelope parsing rules).
 */

import { z } from "zod";

export const ServiceContextSchema = z.enum(["SaaS_Platform", "Face_To_Face"]);
export type ServiceContext = z.infer<typeof ServiceContextSchema>;

export const MetaEnvelopeSchema = z.object({
  requestId: z.string().uuid(),
  timestamp: z.string().datetime(),
  schemaVersion: z.literal("1.4.0"),
});

export const createApiResponseSchema = <T extends z.ZodTypeAny>(dataSchema: T) =>
  z.object({
    success: z.literal(true),
    data: dataSchema,
    meta: MetaEnvelopeSchema,
  });

export const TenantSessionSchema = z.object({
  tenantId: z.string().uuid(),
  serviceContext: ServiceContextSchema,
  activeUnits: z.number().int().nonnegative(),
  telemetrySyncEnabled: z.boolean(),
});
export type TenantSession = z.infer<typeof TenantSessionSchema>;

export class AtlasCoreClient {
  constructor(
    private readonly baseUrl: string,
    private readonly apiKey: string
  ) {}

  public async getTenantSession(tenantId: string): Promise<TenantSession> {
    return this.executeRequest(
      `/v1/tenants/${encodeURIComponent(tenantId)}/session`,
      TenantSessionSchema
    );
  }

  private async executeRequest<T>(path: string, schema: z.ZodType<T>): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${this.apiKey}`,
        "Accept": "application/json",
        "X-Client-Purist-Validation": "strict",
      },
    });

    if (!response.ok) {
      throw new Error(`API Error [${response.status}]: ${response.statusText}`);
    }

    const rawData: unknown = await response.json();
    const parsed = createApiResponseSchema(schema).safeParse(rawData);

    if (!parsed.success) {
      throw new Error(`Data Integrity Violation: ${JSON.stringify(parsed.error.format())}`);
    }

    return parsed.data.data;
  }
}
```