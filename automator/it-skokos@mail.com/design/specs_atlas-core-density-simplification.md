# Design Specification: Atlas Core Dashboard Density Simplification
**Author:** Juno Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 05:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive design and spacing token specification detailing the simplification of Atlas Core dashboard density, aligning layout hierarchy with operational priorities.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Simplification
**Author:** Juno Marlow (Design Agent)
**Project:** Atlas Core | I.T. Skokos
**Status:** Ready for Engineering Review

## 1. Overview & Context
To eliminate cognitive clutter across Atlas Core, we transitioned the primary dashboard from a dense 12-column widget cluster to an 8pt modular grid. We directly referenced `Business Document: Company Document` to map foundational business requirements, determining the critical KPI thresholds and separating core SaaS tenant analytics from Face-to-Face operational queues.

## 2. Layout & Spacing Tokens
- **Base System:** Standardized on an 8pt spatial grid (`$spacing-base: 8px`).
- **Grid Gutters:** Increased canvas gutters from 12px to 24px (`$gutter-canvas: 24px`).
- **Card Inset:** Standardized to 24px internal padding (`$pad-card-lg: 24px`) with 12px corner radiuses (`$radius-md: 12px`).
- **Canvas Background:** Set to `#F9FAFB` (Neutral-50) with pure white `#FFFFFF` elevation-1 surfaces to reduce visual fatigue.

## 3. Information Architecture & Progressive Disclosure
- **Primary Metrics:** Restricted default viewport to 4 core KPI tiles based on the critical metrics identified in `Business Document: Company Document`.
- **Secondary Telemetry:** Shifted secondary tables and drill-down logs into collapsible accordions and off-canvas slide-out drawers.
- **Face-to-Face Service Desk:** Replaced split-pane table density with clean, badge-tagged card items.

## 4. Typography & Accessibility
- **Page Header:** 24px/32px Line Height (Bold)
- **Metric Value:** 32px/40px Line Height (Semibold)
- **Body / Metadata:** 14px/20px Line Height (Regular, `#4B5563` Neutral-600)
- **Contrast Ratio:** Fully audited against WCAG 2.1 AA standards (minimum 4.5:1 for all text).

## 5. Implementation Notes
Design tokens are committed to `@skokos/atlas-tokens` v2.4.0.
```