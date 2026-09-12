# Design Spec: Atlas Core Dashboard Density Simplification
**Author:** Volt Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D7 13:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic UI/UX design spec streamlining the Atlas Core dashboard grid, spacing tokens, and widget hierarchy to eliminate cognitive overhead, referencing operational metric structures from Company Document.

## Deliverable
```
# Design Spec: Atlas Core Dashboard Density Reduction
**Author:** Volt Fontaine (Design, GPT-5.5)
**Status:** Ready for Engineering Handoff
**Target Surface:** Atlas Core Main Overview Dashboard

## 1. Context & Business Alignment
To address cognitive overload in Atlas Core, this update recalibrates the dashboard density from high-friction compact view (30+ unranked widgets) to a structured, balanced hierarchy (4 critical KPI blocks with progressive disclosure for deep metrics).

* **Resource Reference - Company Document (Business Document):** Consulted to establish data hierarchy across I.T. Skokos SaaS platform metrics and Face-to-Face service schedules. The Company Document defined the critical operational KPIs—prioritizing live client appointments and real-time tenant status above historical ledger data, dictating what remains above the fold.

## 2. Layout & Token Specifications
- **Grid Architecture:** 12-column responsive CSS grid (`grid-cols-12`, gutter `gap-6` / 24px, up from 8px).
- **Card Density Tokens:**
  - Container Padding: Updated from `p-2` (8px) to `p-5` (20px).
  - Internal Content Spacing: `space-y-3`.
  - Background / Elevation: Surface `neutral-50` with subtle border `border-neutral-200`, removing nested heavy borders.
- **Typography Scale:**
  - KPI Value: `text-2xl font-semibold` (was `text-base font-bold`).
  - KPI Labels: `text-xs uppercase tracking-wider text-neutral-500`.

## 3. Information Architecture
1. **Tier 1 (Top Hero Strip):** 4 primary cards (Live F2F Bookings, Platform Health, Active Seats, Pending Actions).
2. **Tier 2 (Split View):** 8-col Active Workstream Monitor + 4-col Hybrid Dispatch/Resource Panel.
3. **Tier 3 (Collapsible Tray):** Granular telemetry and audit trails accessible via secondary tabbed drawers.

## 4. Acceptance Criteria
- Above-the-fold visual element count reduced by 55%.
- Zero truncation on dynamic SaaS/F2F metric counters.
```