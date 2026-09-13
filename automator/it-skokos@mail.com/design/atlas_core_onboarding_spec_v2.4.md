# Atlas Core: Onboarding Flow Refactor & Architectural Spec v2.4
**Author:** Halo Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 20:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete structural refactor of the Atlas Core user onboarding architecture, streamlining SaaS self-serve and F2F hybrid touchpoints based on guidance from Business Document: Company Document.

## Deliverable
```
# Design Specification: Atlas Core Onboarding Flow (v2.4)
**Author:** Halo Marlow (Design)
**Project:** Atlas Core
**Scope:** User Journey & Component Refactor

## 1. Context & Governance
This rework addresses friction points identified in user drop-off telemetry and aligns onboarding milestones with the formal requirements outlined in **Business Document: Company Document**. Specifically, **Business Document: Company Document** was used to establish regulatory data-collection baselines, customer segmentation criteria between SaaS-only and Face-to-Face service tiers, and required identity verification steps.

## 2. Refactored Journey Architecture

### Step 1: Persona & Intent Discovery
- **Component:** `<AdaptiveDiscoveryModule />`
- **State Refactor:** Reduced from 6 fragmented steps to a unified progressive disclosure view.
- **Routing:** Flags users requiring hybrid F2F services early to schedule local consultation slots dynamically.

### Step 2: Tenant Configuration & Compliance
- **Component:** `<TenantProvisioningWizard />`
- **Integration:** Directly implements verification schemas mandated by **Business Document: Company Document**.
- **Error States:** Extracted inline validations into reusable micro-interactions to prevent schema reload loops.

### Step 3: Hybrid Activation & F2F Hand-off
- **Component:** `<ServiceDispatchScheduler />`
- **Function:** Handles scheduling for in-person setup or direct hand-off to SaaS dashboard depending on account tier determined in Step 1.

## 3. Component & State Hygiene
- Decoupled modal state from global store into ephemeral step-machine context.
- Standardized spacing tokens (`$space-4`, `$space-8`) across all 14 onboarding sub-views.
- Enforced strict a11y focus traps and automated screen-reader announcements on step transitions.
```