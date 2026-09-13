# Atlas Core: Reworked Hybrid Onboarding Flow Design Specification
**Author:** Byte Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 12:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX/UI design specification for the redesigned Atlas Core onboarding flow, bridging SaaS self-service setup with Face-to-Face concierge onboarding, referencing organizational requirements from Business Document: Company Document.

## Deliverable
```
# Atlas Core — Onboarding Flow Redesign Spec v2.0
**Author:** Byte Marlow (Design)
**Project:** Atlas Core | I.T. Skokos
**Status:** Approved for Implementation

## 1. Documentation & References
- **Business Document: Company Document**: Analyzed to align identity verification requirements, enterprise tier distinctions, and operational touchpoints between SaaS provisioning and Face to Face service kickoffs.

---

## 2. Onboarding Architecture Overview
The reworked flow streamlines initial friction while accommodating hybrid service delivery (pure SaaS vs. SaaS + Face-to-Face consulting).

### Step 1: Workspace Initialization (SaaS Core)
- **Components:** `TenantSetupCard`, `DomainValidationInput`, `AdminInviteField`
- **Interaction:** Progressive disclosure; single-column container (max-width: 560px) centered.
- **Design Tokens:** Surface `$surface-elevated` (#FFFFFF), Primary Action `$brand-500` (#0F52BA).

### Step 2: Service Tier & Delivery Pathing
- **Components:** `ServiceModeSelector` (Segmented Dual Cards)
- **Options:**
  1. *Standard SaaS*: Immediate access to sandbox environment and digital checklist.
  2. *Managed SaaS + Face-to-Face Consultation*: Dynamically surfaced for accounts meeting criteria defined in **Business Document: Company Document**.
- **Behavior:** Conditional routing triggers step 3A or 3B.

### Step 3: F2F Scheduling / Guided Tour Setup
- **Branch A (Pure SaaS):** Interactive product tour trigger (`GuidedTourModal`).
- **Branch B (Hybrid):** In-person kickoff booking widget (`F2FConsultationScheduler`), integrating geographic service availability checks.

### Step 4: Verification & Readiness Hand-off
- **Components:** `ProvisioningProgress`, `LaunchDashboardButton`
- **KPIs:** Target TTFV (Time-To-First-Value) < 3.5 minutes for pure SaaS; Booking completion > 85% for hybrid tiers.
```