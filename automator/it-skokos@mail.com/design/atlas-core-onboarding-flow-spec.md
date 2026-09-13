# Atlas Core Onboarding Flow Refactoring Spec (v2.4)
**Author:** Byte Hale  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 06:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete structural redesign and component architecture for the Atlas Core user onboarding flow, refactored to eliminate UX friction and integrate hybrid SaaS and Face-to-Face activation touchpoints aligned with Company Document.

## Deliverable
```
# Design Specification: Atlas Core Onboarding Flow (v2.4 Refactor)
Author: Byte Hale (Design Agent)
Project: Atlas Core
Target: SaaS Platform & Face-to-Face Hybrid Onboarding

## 1. Context & Governance
- **Reference Resource:** `Company Document` was reviewed to standardize multi-tier tenant requirements and integrate mandatory face-to-face service orientation scheduling alongside SaaS workspace provisioning.

## 2. Refactoring Objectives
- Collapsed previous 7-step linear wizard into a 3-stage adaptive state machine.
- Removed 4 redundant input fields, deferring non-critical profile enrichment post-activation.
- Synchronized design tokens with Atlas UI Core v3.0 (8pt grid, WCAG AAA contrast ratio).

## 3. Flow Architecture

### Stage 1: Identity & Tenant Genesis (`StepTenantSetup.tsx`)
- Micro-step: SSO / Workspace Subdomain validation (real-time async check).
- Form validation: Single-field dynamic reveal pattern.
- Transitions: Auto-advance on deterministic validation (<150ms debounce).

### Stage 2: Operational Topology (`StepTopologyConfig.tsx`)
- Role selector: Card grid matrix (Admin, Practitioner, Hybrid Specialist).
- Face-to-Face Dispatch Integration: Direct lookup module based on `Company Document` regional operational rules.

### Stage 3: Activation & Handoff (`StepActivationReady.tsx`)
- Dynamic split-view:
  - Panel A: SaaS Workspace instant-launch dashboard.
  - Panel B: Face-to-Face dedicated onboarding session booking widget.

## 4. Interaction State Machine
```json
{
  "state": "ONBOARDING_INIT",
  "transitions": {
    "VALIDATE_TENANT": "TOPOLOGY_CONFIG",
    "ASSIGN_ROLE": "SERVICE_DISPATCH",
    "CONFIRM_SCHEDULE": "WORKSPACE_ACTIVE"
  },
  "fallback": "ONBOARDING_SAVE_STATE_RECOVERY"
}
```

## 5. Telemetry & Success Metrics
- Completion Target: < 90 seconds (reduced from 240s).
- Drop-off Budget: < 3.5% between Stage 1 and Stage 2.
```