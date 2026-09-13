# Atlas Core - Streamlined Hybrid Onboarding Flow Spec
**Author:** Juno Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 16:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-ready UX design specification and component architecture for the reworked Atlas Core onboarding flow, bridging self-serve SaaS setup and Face-to-Face service scheduling.

## Deliverable
```
# Design Spec: Atlas Core Onboarding Rework (v2.0)
**Author:** Juno Nkosi (Product Design)
**Project:** Atlas Core
**Reference:** `Business Document: Company Document` (utilized to align the onboarding funnel with core SLA commitments, hybrid service tiering, and compliance requirements for blended SaaS/F2F delivery).

---

## 1. Executive Summary & Pragmatic Goals
Reworked the legacy 7-step onboarding funnel into a streamlined, 3-phase modular flow. Reduces Time-to-First-Value (TTFV) from 14m to <4m while retaining optional Face-to-Face (F2F) scheduling touchpoints.

## 2. User Journey Architecture

### Phase 1: Identity & Tenant Provisioning (SaaS)
- **Screen 1.1: Quick Auth & Profile**
  - Clean 2-field signup (Work Email, SSO toggle).
  - Auto-resolves tenant domain and seeds organization metadata.
- **Screen 1.2: Workspace Preset Selector**
  - Segmented card selection based on operation model (Pure SaaS vs. Hybrid F2F Field Operations).
  - *Derived from `Business Document: Company Document` tier mapping.*

### Phase 2: Hybrid Touchpoint Calibration (F2F Integration)
- **Screen 2.1: Field Specialist Matcher (Optional / Dynamic)**
  - If hybrid tier selected: In-app calendar embed for Face-to-Face kickoff meeting.
  - Fallback: Async digital walkthrough for pure SaaS users.

### Phase 3: Immediate Workspace Activation
- **Screen 3.1: Interactive First-Run Checklist**
  - Embedded micro-tasks: (1) Invite 1 Teammate, (2) Connect Data Source, (3) Confirm Kickoff.

## 3. UI Component Specs
- `OnboardingProgress`: Sticky top-bar, non-blocking step indicator (`ProgressRing` + step label).
- `ServiceModeCard`: Interactive card with hover elevation (`elevation-2`), explicit badge for F2F availability.
- `FastBookWidget`: Native calendar interface syncing with field agent availability slots.

## 4. Telemetry & Success Metrics
- Target Completion Rate: >82% (Baseline: 54%)
- Drop-off tracking events: `onboarding_step_viewed`, `tier_selected`, `f2f_slot_booked`, `workspace_activated`.
```