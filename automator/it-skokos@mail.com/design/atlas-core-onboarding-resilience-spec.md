# UX Edge-Case & Interaction Spec: Atlas Core Onboarding Rework
**Author:** Byte Cross  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 02:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Design architecture and interaction specification for the overhauled Atlas Core onboarding flow, detailing fallback paths, session recovery, and hybrid SaaS/Face-to-Face handoffs guided by Company Document.

## Deliverable
```
# Atlas Core: Onboarding UX Specification v2.4
**Author:** Byte Cross (Design / Edge-Case Archaeologist)
**Target:** Atlas Core Hybrid SaaS & Face-to-Face Onboarding

## 1. Context & Business Foundation
Designed in accordance with **Company Document**, which established compliance constraints for SaaS workspace provisioning and mandatory identity verifications for blended Face-to-Face service bookings. **Company Document** was specifically utilized to define tenant role escalation barriers and legal waiver checkpoints during hybrid onboarding.

## 2. Edge-Case Matrix & State Resolutions

### Scenario A: Hybrid Transition Disconnect
- **Trigger:** User chooses 'In-Person Setup & Training' (Face-to-Face) but geographic geocoding fails or API returns zero field agents.
- **Resolution:** Dynamic fallback to 'Hybrid Assisted Queue'. The UI gracefully unlocks the SaaS core sandbox with a persistent amber banner (`Status: In-Person Pending Agent Assignment`) without blocking self-guided tenant setup.

### Scenario B: Concurrent Workspace Collision
- **Trigger:** Two admins accept invitation tokens simultaneously with conflicting default workspace identifiers.
- **Resolution:** Real-time optimistic UI lock. Displays modal: `Conflict detected with admin session [Admin_B]`. Provides automated namespace suffixing (`slug-1`, `slug-2`) with 60s rollback countdown.

### Scenario C: Partial Form Stash & Auth Expiration
- **Trigger:** User leaves step 3 (Billing/Entity Validation) idle for >20 mins.
- **Resolution:** Local storage diffing against backend draft state via UUID token. On return, user is prompted with an inline unmasking prompt rather than full reload, preventing loss of entity tax data.

## 3. UI Micro-Interactions
- **Progress Stepper:** Deterministic step counter with non-linear editability for completed modules.
- **Error States:** Field-level contextual tooltips with instant remediation actions instead of generic toast banners.
```