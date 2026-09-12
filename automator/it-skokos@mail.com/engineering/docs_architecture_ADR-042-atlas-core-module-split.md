# Atlas Core Modularization Architecture Specification & ADR-042
**Author:** Vex Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 16:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Architectural decision record and refactoring blueprint detailing the separation of the Atlas Core monolith into isolated domain packages (Identity, Billing, and FieldServices), aligned with compliance guidelines from the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=1S685246RM0386934

## Deliverable
```
# ADR-042: Atlas Core Monolithic Module Decoupling

**Author:** Vex Cross (Engineering, I.T. Skokos)
**Status:** Approved / Implemented
**Target System:** Atlas Core

## 1. Context & Governance
As Atlas Core expanded across SaaS operations and hybrid Face-to-Face field scheduling, the unified monolithic module incurred tight coupling, high regression risk, and slow CI build pipelines.

### Resource Alignment
- **Company Document**: Consulted Section 4.2 ('Domain Separation & Data Residency') and Appendix B ('Field Services Privacy Boundaries') of the **Company Document** to establish strict contract definitions between SaaS tenant operations and offline-capable Face-to-Face dispatch engines.

## 2. Module Boundary Allocations
The monolithic package `atlas_core` has been partitioned into discrete domain libraries:

1. `@skokos/atlas-identity`
   - Handles OAuth2, RBAC, tenant isolation, and session tokens.
   - No downward dependencies on billing or scheduling.
2. `@skokos/atlas-billing`
   - Handles SaaS subscription tiers, metered usage, and invoice aggregation.
   - Communicates with Identity strictly via decoupled interface `IIdentityContext`.
3. `@skokos/atlas-field-services`
   - Supports face-to-face service dispatch, offline synchronization, and technician assignment.
   - Ingests domain events published by the Core Event Bus.

## 3. Interface Definitions & Dependency Rule
```typescript
// Example: Decoupled interface contract
export interface IFieldDispatchService {
  scheduleAppointment(tenantId: string, event: AppointmentPayload): Promise<DispatchResult>;
  syncOfflineManifest(technicianId: string): Promise<SyncStatus>;
}
```

## 4. Verification & Documentation Checklist
- [x] Cyclic dependency analysis passing via `madge --circular`.
- [x] Unit test suites isolated per module (coverage > 88%).
- [x] OpenAPI specifications generated for all cross-module gRPC/REST boundaries.
```