# Atlas Core UI Spec: Dashboard Information Density Refactor
**Author:** Vex Reyes  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 14:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Design token specification and layout guideline reducing visual density across Atlas Core dashboard panels, referencing layout standards from Company Document.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Reduction
**Author:** Vex Reyes, Design
**Project:** Atlas Core (I.T. Skokos SaaS & Face-to-Face Platform)
**Status:** Approved for Engineering Handoff

## 1. Overview & Objectives
To eliminate cognitive fatigue and improve operational efficiency across hybrid SaaS telemetry and face-to-face service queues, this specification establishes relaxed grid spacing, streamlined data visualizations, and hierarchical progressive disclosure.

## 2. Resource Attribution
- **Business Document: Company Document**: Evaluated sections governing multi-modal service accessibility and typography baselines. Applied its cross-channel usability metrics to balance on-screen SaaS analytics with high-priority face-to-face appointment schedules.

## 3. Spatial System & Layout Tokens
- **Base Grid**: Transitioned from tight 4px baseline sub-grids to an 8px spatial grid.
- **Card Padding**: Increased from `padding: 12px 16px` to `padding: 24px` (`--space-6`).
- **Column Architecture**: Converted dense 6-widget dashboard layouts into a 3-column modular structure:
  - Col 1 (40% width): Primary F2F Service Dispatch & Live Status
  - Col 2 (35% width): SaaS Utilization & Platform Health
  - Col 3 (25% width): Activity Stream & Actionable Insights (Collapsible drawer on viewport < 1440px)

## 4. Component Refinements
- **KPI Stat Cards**: Removed inline sparklines from default view; converted raw secondary metrics into contextual tooltip drilldowns (`--tooltip-delay: 200ms`).
- **Table Density**: Shifted default table row height from `32px` (compact) to `48px` (standard) with optional table density toggle stored in user preferences.

## 5. Implementation Documentation Note
All frontend components in `atlas-core/web` must adopt the updated design token tokenset `@itskokos/tokens-core@v2.4.0`.
```