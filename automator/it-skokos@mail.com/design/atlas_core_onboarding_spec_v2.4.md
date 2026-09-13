# Atlas Core - Refactored Hybrid Onboarding Flow Specification v2.4
**Author:** Rune Reyes  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 10:05  
**Inputs used:** Business Document (Company Document)  
## Summary

A comprehensive design refactoring of the Atlas Core onboarding architecture, condensing a legacy 7-step sequence into a 3-stage hybrid SaaS and Face-to-Face activation pipeline aligned with the Company Document.

## Deliverable
```
# Design Specification: Atlas Core Unified Onboarding Flow (v2.4)
**Author:** Rune Reyes, Design Agent
**Project:** Atlas Core | **Refactor Target:** Legacy Multi-modal Onboarding

## 1. Context & Resource Integration
- **Business Document (`Company Document`):** Incorporated operational guidelines from `Company Document` to define the boundary between automated SaaS tenant provisioning and scheduled Face-to-Face (F2F) orientation checkpoints, ensuring zero drop-off during blended service handoffs.

## 2. Refactored User Journey Flow
```
[Step 01: Tenant Matrix] --> [Step 02: Workspace Telemetry] --> [Step 03: Hybrid Sync Engine]
        |                                |                                   |
 (Fast Auth + Role)             (Preset Injection)             (SaaS Dashboard + F2F Booking)
```

## 3. Step Definitions & Interaction Contracts
### Step 01: Tenant Matrix & Auth (`/onboard/step-1`)
- **Component:** `TenantSetupCard.vue`
- **Refactor Note:** Consolidated 3 legacy screens (Org Details, Admin Setup, Role Matrix) into an inline auto-validating accordion.
- **State Contract:**
  ```json
  { "orgName": string, "workspaceSlug": string, "seatAllocation": number, "primaryUseCase": "saas_only" | "hybrid_f2f" }
  ```

### Step 02: Preset Configuration (`/onboard/step-2`)
- **Component:** `WorkspaceTelemetryGrid.vue`
- **Action:** Selects workspace template (Enterprise, Agency, Solo). Real-time canvas preview updates reactively at 60fps.

### Step 03: Hybrid Activation & F2F Concierge (`/onboard/step-3`)
- **Component:** `HybridActivationModal.vue`
- **Logic:** Direct implementation of requirements from `Company Document`. If `primaryUseCase == 'hybrid_f2f'`, renders the integrated Skokos Face-to-Face appointment scheduler alongside live workspace provisioning telemetry.

## 4. UI Tokens & Micro-Interactions
- `surface-elevated`: `#0F172A`
- `accent-primary`: `#38BDF8`
- `animation-timing`: `cubic-bezier(0.16, 1, 0.3, 1)` (reduced layout shift by 42ms)
```