# Design Specification: Atlas Core Dashboard Density Reduction
**Author:** Lyra Van Dyk  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D4 11:20  
**Inputs used:** Business Document (Company Document)  
## Summary

UI/UX design specification defining spacing, typography, and card consolidation rules to simplify dashboard density on Atlas Core, aligned with requirements from Company Document.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Simplification

**Author:** Lyra Van Dyk (Design)
**Project:** Atlas Core
**Status:** Ready for Engineering Review

---

## 1. Overview & Objectives
Following the strategic guidelines outlined in **Company Document**, this specification streamlines the primary Atlas Core dashboard interface. The goal is to reduce cognitive load, improve scannability, and establish a cohesive hierarchy across both SaaS Platform metrics and Face-to-Face Service scheduling modules.

## 2. Resource Utilization
- **Company Document**: Consulted for high-level business goals, core KPI definitions, and multi-tenant layout constraints. The metric hierarchy defined in section 3 directly informs widget grouping.

## 3. Layout & Grid Changes
- **Base Grid**: Shift from 12-column compact (8px gutters) to an 8pt modular grid (16px gutters, 24px container margins).
- **Card Consolidation**:
  - Merge 'Active Operations' and 'Real-time Telemetry' into a unified single-card tabbed component.
  - Limit above-the-fold primary metric widgets to 4 key performance tiles (down from 8).
- **Spacing Scale**:
  - Default card padding: increased from 12px to 20px.
  - Micro-spacing between label and value: set to 4px standard.

## 4. Typography & Visual Hierarchy
- **Primary Metrics**: `text-2xl font-semibold` (Inter Display / 24px) for top-line numbers.
- **Secondary Data**: `text-sm text-slate-500` (Inter / 14px) for historical comparisons.
- **Status Tags**: Standardize on subtle badges (radius: 4px, padding: 2px 8px) to eliminate visual noise from solid color fills.

## 5. Interaction & Progressive Disclosure
- Secondary charts default to collapsed accordion views on screen widths < 1440px.
- Deep-dive diagnostic tables moved behind a slide-over modal via 'View Breakdown' action.
```