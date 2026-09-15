# Atlas Core Onboarding Flow & Edge-Case Design Specification
**Author:** Volt Ito  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** 13/09/2026, 23:50:51  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX architecture and state transition spec for the Atlas Core hybrid onboarding flow, accounting for edge-case recovery, SaaS-to-in-person handoffs, and compliance baselines.

## Deliverable
```
# Atlas Core: Hybrid Onboarding Flow & Edge-Case Spec
Author: Volt Ito, Design
Target: Atlas Core Platform & Face-to-Face Services

## 1. Context & Governance
This design specification details the reworked onboarding flow for Atlas Core. In developing this architecture, the **Company Document** was explicitly used to benchmark standard operating procedures for hybrid user intake, verify SLA commitments for in-person service appointments, and enforce client data sovereignty rules across self-serve SaaS workflows.

## 2. Onboarding Flow State Machine & Edge Cases

### Step 1: Identity & Domain Verification (SaaS)
- Primary: Email/SSO auth + workspace creation.
- Edge Case 1.A (Domain Collision): User registers under an existing corporate domain with active SSO. System intercepts standard creation, routes to Just-In-Time (JIT) provisioning request without exposing existing admin names.
- Edge Case 1.B (Intermittent Drops): Form caching via local IndexedDB; zero data loss on step restoration.

### Step 2: Service Tier Routing & Face-to-Face Ingestion
- Hybrid Switch: If tier involves Face to Face Services, trigger physical intake scheduling sub-flow.
- Edge Case 2.A (Geofence / Location Mismatch): Client coordinates outside supported physical dispatch zones dynamically fallback to a remote intake session while queueing a manual logistics override.
- Edge Case 2.B (Simultaneous Calendar Lockout): Double-booking contention on intake staff resolved by 90-second soft-lock with visual countdown ticker.

## 3. UI Component Specs & Fallback Microcopy
- **Progress Stepper**: Non-linear recovery; users can jump backwards to correct enterprise metadata without losing downstream inputs.
- **Error State UX**: Inline diagnostics explaining exact payload/field validation errors rather than generic 'Something went wrong' banners.
```