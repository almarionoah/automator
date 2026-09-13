# Atlas Core Monolith Module Decomposition & Architecture Decision Record
**Author:** Quill Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 13:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Formal Architectural Decision Record (ADR-042) and interface contract specification outlining the decomposition of the monolithic Atlas Core module into isolated SaaS and Face to Face domain services, cross-referenced with Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=1B648001XG1400153

## Deliverable
```
# ADR-042: Atlas Core Monolithic Module Decomposition

**Author:** Quill Hale (Engineering)
**Status:** Approved & Implemented
**Target:** Project Atlas Core (I.T. Skokos)

## 1. Context & Governance Reference
The legacy monolithic module within `Atlas Core` coupled SaaS subscription workflows with Face to Face field service operations, resulting in tight database coupling and high deployment friction.

Per the governance standards in the **Company Document**, we audited system boundary requirements, data residency constraints, and operational SLA targets. Specifically, the **Company Document** provided the baseline domain segregation criteria used to partition SaaS billing from physical dispatch scheduling.

## 2. Decision & Boundary Partitioning
We have decoupled the monolith into three discrete sub-modules with documented interfaces:

1. `atlas-auth-context`: Zero-dependency IAM and tenant context engine.
2. `atlas-saas-billing`: Webhook-driven recurring billing and entitlement enforcement.
3. `atlas-f2f-dispatch`: Real-time scheduling engine for Face to Face field technicians.

```typescript
// Boundary Contract: atlas-f2f-dispatch
export interface IFieldDispatchService {
  scheduleVisit(tenantId: string, dispatchPayload: DispatchDTO): Promise<DispatchResult>;
  syncFieldStatus(ticketId: string, status: ExecutionStatus): Promise<void>;
}
```

## 3. Migration & Documentation Standards
- **Inverted Dependencies:** Cross-module direct DB queries are replaced with gRPC contracts documented in `/docs/proto/`.
- **Data Isolation:** Domain event schemas (`DispatchScheduledEvent`, `InvoiceFinalizedEvent`) published to EventBridge with AsyncAPI specs.
- **Verification:** 100% contract test coverage via Pact; documentation linting enforced in CI via Spectral.

All architectural choices comply strictly with the module isolation mandates set in the **Company Document**.
```