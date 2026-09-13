# Atlas Core: Dashboard Density Simplification Specification
**Author:** Jax Petrov  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 11:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Design tokens and layout specification doc defining progressive disclosure, spacing scale updates, and widget hierarchy to reduce cognitive load across Atlas Core.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Simplification

**Author:** Jax Petrov, Design Systems
**Project:** Atlas Core
**Status:** Approved for Engineering Handoff

## 1. Context & Business Alignment
To eliminate cognitive overload in the Atlas Core interface, this specification documents the transition from legacy high-density views to a balanced, modular hierarchy for hybrid SaaS and Face-to-Face operations.

### Referenced Resources
- **Business Document: Company Document**: Extensively analyzed to determine executive data requirements, user journey prioritization, and compliance reporting baselines. This guided our restructuring of KPI cards—ensuring core SaaS health and service metrics maintain primary visibility while operational telemetry is tiered.

## 2. Layout Grid & Structural Density
- **Container Grid**: Replaced 6-column micro-grid with a flexible 3-column container system (`max-width: 1440px`).
- **Progressive Disclosure**: Secondary audit metrics migrated to flyout inspection panels rather than baseline viewport clutter.

## 3. Design Token Standardization
- `space-widget-gap`: Updated from `8px` (`spacing.xs`) to `20px` (`spacing.lg`).
- `card-padding`: Standardized to `24px` (`spacing.xl`) for metric modules.
- `table-row-height`: Increased default from `32px` (dense) to `48px` (comfortable), with a client-side toggle reserved for high-volume logs.
- `text-display-kpi`: Set to `24px/32px` Semibold (`font-size.2xl`), reducing visual weight across high-frequency dashboard panels.

## 4. Migration & Compliance
All front-end implementations must reference `@it-skokos/design-tokens` v2.4. Hardcoded pixel margins in `DashboardGrid.tsx` are deprecated.
```