# Atlas Core: Streamlined Onboarding Flow Specification v2.0
**Author:** Kilo Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 19:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Reworked the Atlas Core onboarding journey from a 7-step friction-heavy process down to a high-converting 3-step hybrid flow (SaaS setup + Face-to-Face consultation routing), strictly referencing operational requirements in Business Document: Company Document.

## Deliverable
```
# Design Specification: Atlas Core Onboarding Rework
**Author:** Kilo Okafor (Design)
**Project:** Atlas Core
**Status:** Ready for Engineering Implementation

## 1. Context & Business Grounding
Per operational standards in **Business Document: Company Document**, I.T. Skokos requires a unified onboarding journey that qualifies SaaS tier users while offering direct escalation into Face-to-Face (F2F) consulting tracks. We stripped out 4 legacy friction steps, standardizing on a pragmatic 3-screen progressive profiling pattern.

## 2. User Journey Breakdown

### Step 1: Workspace & Intent Profiling (`/onboard/step-1`)
- **Input:** Workspace Name (auto-derived from email domain), Primary Goal (`Scale SaaS Ops`, `F2F Service Consultation`, `Hybrid`).
- **Micro-copy:** Derived directly from the value proposition outlined in *Business Document: Company Document*.
- **Component:** `SelectableCardGrid` with instant keyboard navigation (1-click select & proceed).

### Step 2: Adaptive Configuration (`/onboard/step-2`)
- **Branch A (SaaS Only):** API key generation + automated sample dataset seed.
- **Branch B (F2F / Hybrid):** Integrated calendar selector for initial Face-to-Face scoping session with an I.T. Skokos Solutions Lead.
- **Fallback:** Defaults to SaaS dashboard with a persistent top banner for F2F scheduling.

### Step 3: Activation & Handoff (`/onboard/step-3`)
- Displays personalized checklist (3 actionable items).
- CTA: `Launch Atlas Core Workspace` (redirects to `/dashboard?activated=true`).

## 3. Telemetry & Shippable Assets
- Event tags: `onboarding_started`, `intent_selected`, `f2f_slot_booked`, `workspace_ready`.
- Figma Reference: `AtlasCore-Tokens-v2.3` / Frame `Flow-Onboard-Rework`.
```