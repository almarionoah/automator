# Atlas Core: Monolith Module Extraction ADR & Interface Specification
**Author:** Onyx Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 04:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Architecture Decision Record (ADR) and interface contracts detailing the extraction of the monolithic Atlas Core module into decoupled SaaS Platform and Face-to-Face Services packages, guided by the Business Document: Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=5BM06797BM076042L

## Deliverable
```
# ADR 0042: Atlas Core Monolith Module Separation

**Status:** Accepted  
**Author:** Onyx Van Dyk (Engineering)  
**Governing Resource:** Business Document: Company Document (utilized to align domain boundaries, data retention rules, and separation requirements between SaaS multi-tenant workflows and Face to Face physical service logistics).

## 1. Context & Rationale
Atlas Core historically combined core platform tenancy with real-time field service dispatch in `atlas_core.monolith`. As mandated by the architecture standards in `Business Document: Company Document`, we have decoupled these into isolated domain modules to eliminate circular dependencies and ensure horizontal scalability.

## 2. Decoupled Module Interfaces

### SaaS Platform Package (`@skokos/atlas-saas`)
```typescript
export interface ISaaSSubscriptionManager {
  provisionTenant(tenantId: string, tier: string): Promise<TenantRecord>;
  processUsageEvent(tenantId: string, metric: UsageMetric): Promise<void>;
}
```

### Face to Face Services Package (`@skokos/atlas-f2f`)
```typescript
export interface IF2FDispatchManager {
  scheduleAgent(request: DispatchRequest): Promise<DispatchConfirmation>;
  resolveServiceTicket(ticketId: string, notes: string): Promise<TicketResolution>;
}
```

## 3. Communication Contract
- Synchronous in-memory calls have been replaced with the internal event bus (`CoreEventBus`).
- Events `TenantBillingCycleClosed` and `F2FServiceCompleted` handle cross-module lifecycle syncing without direct relational database coupling.

## 4. Documentation & Verification
- Isolated unit test suites confirmed 0 cross-module cyclic imports.
- Architecture conforms strictly to the SLA definitions documented in Business Document: Company Document.
```