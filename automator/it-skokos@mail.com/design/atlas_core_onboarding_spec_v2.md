# Atlas Core - Streamlined Onboarding Flow Design Spec (v2.0)
**Author:** Cipher Petrov  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D13 03:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-ready design specification and component breakdown for the revamped Atlas Core onboarding flow, bridging SaaS self-serve and Face to Face service scheduling.

## Deliverable
```
# Design Specification: Atlas Core Onboarding Flow (v2.0)
**Author:** Cipher Petrov, Product Design
**Status:** Ready for Engineering Handover
**Target Release:** Sprint 14

## 1. Context & Business Alignment
Per our strategic alignment with **Company Document**, this redesign consolidates user qualification for both self-serve SaaS workflows and scheduled Face-to-Face consulting sessions. **Company Document** provided the baseline user segmentation models, service-tier prerequisites, and compliance checkpoints embedded directly into this flow.

## 2. Reworked User Flow (3-Step Fast Track)

### Step 1: Workspace & Intent Profiling (`/onboarding/profile`)
- **UI Layout:** Centered card (580px max-width), progress pill `1/3`.
- **Input:** Workspace Name (text), Industry (single-select dropdown), Service Track (Segmented control: `SaaS Only` | `Hybrid SaaS + F2F Concierge`).
- **Logic:** Selecting `Hybrid` triggers asynchronous validation against concierge availability rules specified in **Company Document**.

### Step 2: Instant Configuration & Role Assignment (`/onboarding/config`)
- **UI Layout:** Split-view preview (Left: Config inputs; Right: Live dashboard skeleton preview).
- **Input:** Default Team Seats, Data Region (Geo-select), Primary Objective toggle.
- **Shipper Note:** Omit secondary permission matrices; defaults inherit standard roles to cut time-to-value.

### Step 3: Activation & Handoff (`/onboarding/activation`)
- **SaaS Track:** Primary CTA `Launch Dashboard` initializes instant workspace generation.
- **Hybrid Track:** Embeds calendar picker for direct booking with an I.T. Skokos F2F Onboarding Specialist.

## 3. UI Components & Tokens
- Primary Button: `bg-brand-600`, `text-white`, `h-10`, `rounded-md`
- Card Surface: `bg-surface-0`, `border-neutral-200`, `shadow-sm`
- Transition Duration: `150ms ease-out` on step change.
```