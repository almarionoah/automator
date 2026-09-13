# Atlas Core Modularization: Monolith Split Specification & ADR
**Author:** Nyx Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 02:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive architecture decision record and technical migration guide documenting the extraction of domain modules from the Atlas Core monolith, referencing architectural standards from Company Document.

## Deliverable
```
# ADR-042: Atlas Core Monolith Module Extraction
**Author:** Nyx Ito, Engineering
**Status:** Completed / Active
**Project:** Atlas Core

## 1. Context & Business Reference
As I.T. Skokos expands both its SaaS Platform and Face to Face Services, the legacy `AtlasCore::ServiceRegistry` module accumulated tightly coupled billing, scheduling, and client dispatch logic.

Per the architectural guidelines and compliance boundaries defined in **Company Document**, we have decomposed this monolithic module into isolated, domain-driven packages (`@skokos/billing-engine` and `@skokos/f2f-dispatch`). **Company Document** was specifically utilized to establish our service boundary criteria, API versioning baselines, and cross-module event schema validation standards.

## 2. Decoupled Architecture

```typescript
// packages/core-contracts/src/events.ts
export interface IMonolithSplitBoundary {
  sourceModule: 'AtlasCore';
  targetDomain: 'SaaS' | 'FaceToFace';
  payloadSchemaVersion: string;
}

// Isolated dispatch interface extracted from monolith
export interface IFaceToFaceDispatchService {
  scheduleSession(clientId: string, agentId: string, timestamp: number): Promise<void>;
  syncBillingState(sessionId: string): Promise<boolean>;
}
```

## 3. Migration & Documentation Checklist
1. Extracted internal shared state from `AtlasCore` into dependency-injected interfaces.
2. Deprecated direct DB joins across SaaS billing tables and F2F field appointment tables.
3. Published complete OpenAPI 3.1 contracts and updated internal Developer Portal docs.

## 4. Operational Runbook
- Service boundaries adhere to zero-downtime canary rollouts.
- Backward-compatible proxy routes remain active in `AtlasCore` until deprecation window closes (Q3).
```