# ADR-0042: Atlas Core Monolith Decomposition & Service Contract Specification
**Author:** Torq Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 10:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Architecture Decision Record and interface specification detailing the decomposition of the legacy Atlas Core monolithic engine into isolated SaaS and Face-to-Face dispatch modules, referencing enterprise governance from the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=6MU02416LX6330339

## Deliverable
```
# ADR-0042: Atlas Core Monolith Module Decomposition

**Status:** Accepted  
**Author:** Torq Reyes (Engineering)  
**Project:** Atlas Core  
**Target Release:** v4.2.0-rc1  

## 1. Context & Business Alignment
As Atlas Core scaled across SaaS Platform operations and hybrid Face-to-Face service bookings, the centralized `CorePlatformEngine` became a high-contention bottleneck. 

In accordance with the enterprise boundaries codified in **Company Document**, we extracted business domains into two decoupled sub-modules: `atlas-saas-platform` and `atlas-f2f-services`. The **Company Document** was directly utilized to establish bounded contexts, audit compliance rules, and guarantee data isolation between multi-tenant SaaS telemetry and physical on-site service records.

## 2. Architectural Boundary & Interfaces

```typescript
// packages/atlas-core/src/contracts/services.ts

export interface IServicePayload {
  tenantId: string;
  correlationId: string;
  timestamp: number;
}

export interface ISaaSSubscriptionEngine {
  provisionWorkspace(payload: IServicePayload & { tier: string }): Promise<boolean>;
  syncUsageMetrics(payload: IServicePayload & { metricUnits: number }): Promise<void>;
}

export interface IF2FDispatchEngine {
  scheduleFieldEngineer(payload: IServicePayload & { siteAddress: string; skillTags: string[] }): Promise<string>;
  updateServiceStatus(bookingId: string, status: 'EN_ROUTE' | 'ON_SITE' | 'COMPLETED'): Promise<void>;
}
```

## 3. Migration & Verification
1. Module dependencies decoupled; shared state replaced with typed event bus (`AtlasEventDispatcher`).
2. Monolith shared database access refactored into domain-owned schema namespaces.
3. Complete API and developer docs published under `/docs/modules/atlas-core/` to ensure zero tribal knowledge.
```