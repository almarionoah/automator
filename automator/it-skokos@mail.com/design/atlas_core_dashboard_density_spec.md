# Atlas Core: Dashboard Density Simplification Spec
**Author:** Echo Reyes  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 12:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Design spec and layout token refactor to decrease visual density and improve operational velocity on the Atlas Core dashboard.

## Deliverable
```
# Atlas Core - Dashboard Density & Layout Specification
**Author:** Echo Reyes (Design)
**Project:** Atlas Core
**Status:** Ready for Handoff

## 1. Objective & Strategic Alignment
Simplify visual density across the Atlas Core unified console, balancing high-frequency SaaS metrics with Face-to-Face service dispatch workflows without degrading data accessibility.

### Resource Reference
- **Business Document: Company Document**: Utilized section 3.2 ('Operator Operational Flows & SLA Priorities') to determine the hierarchy of critical data points vs. secondary telemetry. This ensured primary face-to-face dispatch queues and core SaaS health metrics retain top-of-fold priority while peripheral logs are tucked into secondary drawers.

## 2. Layout & Density Token Refactor
We shift from the previous cramped 4px micro-grid to a standard pragmatic 8px system.

- **Container Padding:** Reduced outer frame padding from 32px to 24px (`--space-6`) to regain viewport real estate.
- **Card Gutters:** Standardized at 16px (`--space-4`) grid gaps.
- **Card Content Padding:** Shifted from 20px uniform to `16px 20px` (compact vertical, comfortable horizontal).
- **Metric Callouts:** Downsized primary KPI type from `36px/44px` to `28px/34px bold`, cutting vertical card height by ~22%.

## 3. Component Hierarchy Adjustments
1. **Unified Action Bar**: Collapsed 6 distinct top-level filter chips into a single faceted search bar with active filter pills.
2. **Hybrid Queue Module**: Split 'In-Person Service Bookings' and 'SaaS Account Telemetry' into tabbed views rather than side-by-side stacked tables.
3. **Progressive Disclosure**: Replaced full-width inline audit logs with a contextual slide-over drawer triggered by row click.

## 4. Handoff Notes
- Tokens applied directly to Figma library `@atlas/ui-tokens v1.4.0`.
- React dashboard container component updated under `packages/atlas-dashboard/src/components/DashboardGrid.tsx`.
```