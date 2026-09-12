# UI/UX Design Spec: Dashboard Density Optimization for Atlas Core
**Author:** Zed Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 12:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic design spec and token refactor reducing visual density on the Atlas Core dashboard via simplified 8pt grid metrics, card consolidation, and progressive disclosure.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Reduction
Author: Zed Fontaine (Design)
Project: Atlas Core
Status: Ready for Implementation

## 1. Overview & Objective
Simplify visual density across the Atlas Core primary dashboard to decrease user cognitive overhead without sacrificing operational throughput for both SaaS platform workflows and Face to Face service scheduling.

## 2. Resource Alignment
- Business Document: Company Document: Utilized to audit existing dashboard widgets against primary operational KPIs. Metrics not explicitly required by the business document were demoted from primary cards to secondary tabs, ensuring high-priority business targets remain prominent while eliminating visual clutter.

## 3. Layout & Spacing Token Updates
- Base Spacing Scale: Transitioned from condensed 4px increments to a standard 8px grid (spacing-md: 16px, spacing-lg: 24px).
- Widget Grid: Replaced 4-column micro-card layout with a responsive 3-column modular grid (min-width: 360px per card).
- Padding Refactor:
  - Card container padding: Increased from 12px to 20px.
  - Table cell padding: Increased vertical padding from 6px to 12px for improved legibility.

## 4. Visual Hierarchy & Progressive Disclosure
- Metric Card Consolidation: Merged 6 standalone KPI widgets into 3 unified metric summaries with inline trend sparklines.
- Collapsible Activity Feeds: Converted continuous live feeds into expandable drawers with default 5-item display limit.
- Action Demotion: Secondary actions (e.g., Export, Filter Presets) moved into a consolidated header utility menu.

## 5. Next Steps
- Ship token updates to `@skokos/atlas-ui` package.
- Validate telemetry on task completion speed post-deployment.
```