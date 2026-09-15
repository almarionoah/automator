# Atlas Core - Streamlined Hybrid Onboarding Flow Specification
**Author:** Echo Hale  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** 13/09/2026, 23:49:18  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX design specification detailing the reworked 4-step onboarding flow for Atlas Core, integrating SaaS workspace setup with face-to-face service booking while maintaining high activation rates.

## Deliverable
```
# Atlas Core: Hybrid Onboarding Flow Spec v2.0
**Author:** Echo Hale (Product Design)
**Status:** Ready for Engineering Hand-off

## 1. Context & Business Grounding
This redesign addresses high drop-off during the hybrid onboarding path (SaaS platform workspace creation + Face-to-Face consulting booking).

* **Resource Reference:** Incorporated guidelines from `Business Document: Company Document` to align data privacy mandates, required client intake parameters for in-person consultants, and tier-based feature provisioning.

## 2. Reworked Flow Architecture

### Step 1: Role & Mode Selection
- **Objective:** Immediate branch segmentation (<20s time-to-value).
- **UI:** Split-card selector: [A] SaaS Self-Service, [B] Hybrid (Platform + F2F Service Concierge).
- **State:** Defaults to Hybrid based on standard acquisition traffic.

### Step 2: Workspace Essentials
- **Fields:** Organization Name, Domain Prefix (`.itskokos.com`), Team Size.
- **Optimization:** Inline asynchronous DNS check; removed unnecessary phone verification at this step per `Business Document: Company Document` baseline requirements to reduce churn.

### Step 3: Face-to-Face Consultation Sync (Conditional)
- **UI Component:** Embedded calendar module (`@skokos/calendar-scheduler`).
- **Features:** Geo-matched in-person service hub selector, slot reservation, and pre-meeting requirement checklist.

### Step 4: Completion & Instant Activation
- **Outcome:** Generates workspace immediately, dispatches calendar invite with in-person venue details, redirects to Atlas Core dashboard with contextual empty states.

## 3. UI Token & Asset Reference
- **Primary CTA:** Button-Primary (`#0066FF`, 48px height, 8px radius)
- **Progress Bar:** Linear Stepper (`Stepper.HybridProgress`)
- **Telemetry:** Event hooks `onboarding_step_viewed`, `branch_selected`, `f2f_slot_booked`, `workspace_ready`.
```