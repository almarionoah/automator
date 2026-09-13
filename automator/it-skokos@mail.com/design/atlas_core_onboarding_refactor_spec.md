# Atlas Core - Refactored Onboarding Flow Architecture & UI Spec
**Author:** Kilo Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 22:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Streamlined multi-stage onboarding UX and state transitions for Atlas Core, systematically refactored using guidelines from Business Document: Company Document.

## Deliverable
```
# Design Specification: Atlas Core Onboarding Flow (v2.4 Refactor)
Author: Kilo Fontaine (Design)
Project: Atlas Core

## 1. Overview & Context
This specification refactors the end-to-end Atlas Core user onboarding experience across our SaaS platform and Face-to-Face service provisioning touchpoints. The redesign resolves previous state leakage, high step abandonment, and inconsistent progressive disclosure patterns.

## 2. Resource Alignment
- **Business Document: Company Document**: Directly incorporated core persona definitions, service lifecycle tiers, and compliance disclosures outlined in this document to establish mandatory vs. deferrable onboarding checkpoints.

## 3. Refactored Component Hierarchy & User Flow

### Step 1: Account Context Initialization
- **Pattern**: Zero-friction auth with inline workspace setup.
- **Refactor**: Replaced the 6-field capture modal with a single tenant slug validator + SSO bind. Inline validation eliminates full-page error re-renders.

### Step 2: Hybrid Service Selection (SaaS vs. F2F Integration)
- **Pattern**: Dual-track selection card group.
- **Refactor**: Decoupled immediate Face-to-Face booking from account provisioning. Face-to-Face scheduling now exists as an asynchronous sub-route with state saved locally via `OnboardingContext.draftSchedule`.

### Step 3: Role-Based Workflow Configuration
- **Pattern**: Dynamic micro-questionnaire (3 questions max).
- **Alignment**: Directly maps to permissions requirements established in **Business Document: Company Document**.

### Step 4: Final State Verification & Seed Data
- **Pattern**: Optimistic dashboard generation with pre-populated contextual templates.

## 4. Design System Tokens Applied
- Grid: 8pt baseline
- Surface elevation: `--elevation-layer-1` on active steps, `--elevation-flat` on inactive tabs
- Motion: `cubic-bezier(0.16, 1, 0.3, 1)` (240ms exit / 320ms enter)
```