# Atlas Core: Monolith Module Decomposition Spec & Migration Guide
**Author:** Halo Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 07:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive Architectural Decision Record (ADR) and implementation guide detailing the modularization of Atlas Core into domain-isolated packages, adhering to domain boundaries defined in Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=55258691SM1179408

## Deliverable
```
# ADR-042: Monolithic Module Decomposition for Atlas Core

**Author:** Halo Ito (Engineering)
**Status:** Approved / Implemented
**Date:** 2026-03-30

## 1. Context & Business Alignment
Project Atlas Core previously aggregated SaaS billing, user management, and Face-to-Face (F2F) scheduling into a single tightly coupled module. In accordance with the domain boundaries outlined in **Company Document**, we have decomposed this monolith to enforce strict service boundaries and isolation between digital SaaS streams and physical service dispatches.

### Resource Reference
- **Company Document**: Utilized during Section 2 boundary mapping to ensure that enterprise tenant multi-tenancy rules and compliance policies for F2F interactions remain strictly decoupled from SaaS background processors.

## 2. Decoupled Service Architecture

### Before:
`AtlasCore::Monolith` -> Handled Auth, Subscriptions, F2FScheduling, and Invoicing directly via shared state.

### After:
1. **`@skokos/atlas-auth`**: Core authentication and RBAC interfaces.
2. **`@skokos/atlas-saas-billing`**: Subscription lifecycle, metered usage, and invoice generation.
3. **`@skokos/atlas-f2f-engine`**: Geolocation dispatch, F2F service bookings, and field agent sync.

## 3. Interface Contract (TypeScript Example)

```typescript
// packages/f2f-engine/src/contracts/booking.ts
export interface IF2FBookingRequest {
  tenantId: string;
  serviceId: string;
  agentId: string;
  scheduledWindow: [Date, Date];
  complianceSignature: string; // Enforced per Company Document spec
}

export interface IF2FDispatchResult {
  bookingId: string;
  status: 'DISPATCHED' | 'PENDING' | 'REJECTED';
}
```

## 4. Verification & Validation Plan
- **Unit Coverage**: 100% boundary isolation using mocked external interfaces.
- **Integration Tests**: `pnpm test:integration` validating zero circular dependencies across packages.
```