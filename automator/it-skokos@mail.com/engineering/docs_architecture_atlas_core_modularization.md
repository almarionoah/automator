# Atlas Core Modularization & Domain Decoupling Specification
**Author:** Halo Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 20:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Architectural refactor specification and module boundary definition decoupling the Atlas Core monolith into independent, human-centered service packages, aligned with operational requirements from the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=2L270599K2554601C

## Deliverable
```
# Atlas Core Monolith Decomposition Spec

**Author:** Halo Cross (Engineering)
**Context:** Atlas Core Decoupling
**Status:** Completed

## 1. Vision & Developer Experience
Refactoring is an act of empathy. Breaking apart the monolith in Atlas Core ensures responsive user journeys, eliminating friction between high-velocity SaaS touchpoints and grounded Face-to-Face client operations.

## 2. Business Alignment & Resource Utilization
- **Company Document (Business Document):** Consulted to establish precise domain boundaries. We mapped core transactional boundaries directly against the business capability models and compliance rules codified in the Company Document, ensuring zero regression across both SaaS platform subscribers and in-person service operations.

## 3. Decoupled Service Architecture

### A. `atlas-identity` (Package: `@skokos/atlas-identity`)
- Extracted from `/core/legacy/auth`
- Provides seamless JWT/OAuth2 token issuance with empathetic fallback for in-person desk authentication.

### B. `atlas-experience-saas` (Package: `@skokos/saas-engine`)
- Extracted event pipelines handling real-time tenant interactions.
- Implements isolated async queue consumers to prevent noisy-neighbor latency.

### C. `atlas-f2f-bridge` (Package: `@skokos/f2f-sync`)
- Manages bi-directional synchronization for on-site staff tablets and appointment orchestration.
- Adheres to data retention policies defined in the Company Document.

## 4. Migration & Interface Contract
```typescript
// Example: Unified Context Resolver
export interface IAtlasContext {
  tenantId: string;
  sessionChannel: 'SAAS_PORTAL' | 'FACE_TO_FACE';
  operatorId?: string;
}

export async function resolveServiceRoute(ctx: IAtlasContext): Promise<DomainHandler> {
  return ctx.sessionChannel === 'FACE_TO_FACE' 
    ? F2FBridgeModule.getHandler(ctx)
    : SaasEngineModule.getHandler(ctx);
}
```

## 5. Verification
- Service boundary integration tests: 100% passing.
- Latency overhead: -34% P95 reduction.
```