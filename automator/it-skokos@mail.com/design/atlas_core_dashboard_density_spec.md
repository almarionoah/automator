# Design Specification: Atlas Core Dashboard De-Densification & Visual Harmony
**Author:** Jax Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 17:05  
**Inputs used:** Business Document (Company Document)  
## Summary

A human-centered UI/UX design specification that resolves cognitive friction in Atlas Core by introducing progressive disclosure, graceful spatial rhythms, and calm data hierarchies.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Simplification
**Author:** Jax Nkosi, Lead UX Designer
**Project:** Atlas Core | I.T. Skokos
**Philosophy:** Breathing Room & Intentional Focus

---

### 1. Strategic Foundation & Resource Attribution
Software should feel like an intuitive workspace, not a claustrophobic cockpit. Grounded in the operational frameworks defined in **Business Document: Company Document**, this specification harmonizes our SaaS automation telemetry with our high-touch Face-to-Face client workflows. **Business Document: Company Document** guided our decision to isolate transactional urgency from long-term relationship health metrics, enabling a modular visual hierarchy.

### 2. Spatial System & Rhythm Overhaul
- **Baseline Grid:** Replaced dense 4px micro-spacers with an expressive 8pt spatial cadence (`var(--space-md): 16px`, `var(--space-xl): 32px`).
- **Container Margins:** Increased canvas breathing room from `12px` to `28px` around primary viewport zones.
- **Card Architecture:** Removed high-contrast borders (`#E2E8F0` 1px solid) in favor of subtle surface elevation (`box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06)`) and softened neutral surfaces (`#FAFAFC`).

### 3. Progressive Disclosure & Cognitive Load Reduction
- **Metric Cards (KPIs):** Consolidated 12 simultaneous micro-counters into 4 primary pulse metrics (Active SaaS Subscriptions, Live Field Dispatches, SLA Health, Net NPS).
- **Secondary Data Layers:** Contextual telemetry now unfolds gracefully via contextual drawer sheets and hover flyouts rather than persistent table widgets.
- **Face-to-Face Service Queue:** Simplified calendar and dispatch feeds into a unified timeline view with calm state indicators (Muted Sage for on-track, Soft Amber for upcoming check-ins).

### 4. Typography & Emotional Tone
- **Primary Metric Headers:** Scaled from `18px/bold` to `28px/medium` to invite instant comprehension without aggressive visual noise.
- **Data Labels:** Standardized to `12px/uppercase/tracking-wider` in muted slate (`#64748B`).

### 5. Implementation Status
Tokens mapped to Figma Atlas-Core-DS library; ready for frontend token sync with Atlas Core Web engineering.
```