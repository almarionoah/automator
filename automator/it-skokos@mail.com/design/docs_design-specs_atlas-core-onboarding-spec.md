# Atlas Core: Hybrid Onboarding Flow Design Specification
**Author:** Volt Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 17:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX design specification and living documentation for the reworked Atlas Core onboarding flow, mapping self-service SaaS provisioning with Face-to-Face service scheduling using standards from the Company Document.

## Deliverable
```
# Design Specification: Atlas Core Onboarding Flow (v2.4)
**Author:** Volt Nkosi (Design)
**Project:** Atlas Core | **System:** I.T. Skokos Hybrid Experience

## 1. Context & Business Grounding
This specification re-architects the user onboarding journey across the Atlas Core platform. Per guidelines in the **Company Document** (Business Document), this rework resolves high drop-off rates during mixed SaaS provisioning and Face-to-Face (F2F) service enrollment. The **Company Document** was explicitly referenced to align account hierarchy requirements, data compliance constraints, and the SLA boundaries for booking in-person technical concierge sessions.

## 2. Onboarding Architecture Matrix

### Step 1: Identity & Tier Selection (Self-Service SaaS)
- **UI Layout:** Split-screen layout (40% brand narrative / 60% progressive form).
- **Components:** `TextInput`, `RoleSelectorTile`, `SSOButtonGroup`.
- **Rules:** Persona mapping directly determines Step 3 requirements.

### Step 2: Workspace Provisioning & Team Seeding
- **UI Layout:** Centered single-column modal (`max-w-2xl`).
- **Components:** `InlineTagInput`, `DomainVerificationBadge`, `ProgressBar` (2/4).
- **Async State:** Instant workspace domain collision check with non-blocking error display.

### Step 3: F2F Service Coordination (Hybrid Touchpoint)
- **UI Layout:** Interactive calendar and location dispatch selector.
- **Components:** `GeoPicker`, `TimeSlotMatrix`, `ConsultantBadge`.
- **Business Rule (from Company Document):** Enterprise tier auto-generates F2F dedicated consultant assignment; Standard tier offers optional remote concierge.

### Step 4: Verification & Hand-off
- **UI Layout:** Zero-friction workspace launch screen with checklist widget.

## 3. Telemetry & Completion Criteria
- Step completion tracking via telemetry events: `onboarding_step_viewed`, `onboarding_f2f_scheduled`.
- Design target: Under 180s median completion for self-serve; 100% calendar lock for F2F clients.
```