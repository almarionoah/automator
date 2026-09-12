# Atlas Core: Hybrid Onboarding Flow Spec & Edge-Case Matrix
**Author:** Quill Adeyemi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 16:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Interaction design specification and comprehensive edge-case handling matrix for the reworked Atlas Core onboarding flow, bridging SaaS setup and Face-to-Face consultation scheduling.

## Deliverable
```
# Design Specification: Atlas Core Reworked Onboarding Flow
**Author:** Quill Adeyemi (Design / Edge-Case Archaeologist)
**Target:** Project Atlas Core (SaaS + Face-to-Face Onboarding)

## 1. Context & Resource Integration
Per the guidance in **Business Document: Company Document**, which outlines operational standards and dual-service boundaries for I.T. Skokos, this reworked flow harmonizes digital SaaS workspace setup with mandatory in-person/face-to-face onboarding touchpoints.

## 2. Core Flow Architecture
1. **Step 1: Tenant Identity & SSO Verification** (SaaS)
2. **Step 2: Dual Profile Provisioning** (Admin User + Physical Office Location)
3. **Step 3: Face-to-Face Consultation Booking** (Dispatch slot & location lock)
4. **Step 4: Environment Initialization & Handoff Screen**

## 3. Edge-Case Matrix & Failure Recovery States
- **Scenario E-01: Network Drop During In-Person Slot Reservation**
  - *Behavior:* Optimistic lock on calendar slot (10m TTL). If offline, cache state in IndexedDB and present `STATE_DEGRADED_SYNC` banner with auto-reconnect ping.
- **Scenario E-02: Tenant Domain Collision Across Dual Registrations**
  - *Behavior:* Inline domain resolver prevents hard validation blocks; routes to claim workflow with clear ownership recovery CTA rather than standard 400 error.
- **Scenario E-03: Mismatched Geolocation for Face-to-Face Service Zone**
  - *Behavior:* If physical address falls outside primary service coverage (defined in Company Document), trigger fallback `REMOTE_ASSIST_BRIDGE` modal without restarting SaaS workspace provisioning.
- **Scenario E-04: Partial Flow Abort at Step 3**
  - *Behavior:* Save delta payload. On return, deep-link user directly to pending slot confirmation with pre-populated workspace settings.

## 4. UI Components & Micro-Interactions
- `SyncStatusIndicator`: 3-state component (Live, Reconnecting, Local-Cache).
- `SlotPicker`: Incorporates travel-buffer indicators.
```