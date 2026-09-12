# Atlas Core Dashboard Density & Layout Simplification Specification
**Author:** Cipher Cross  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D10 08:40  
**Inputs used:** Business Document (Company Document)  
## Summary

UI/UX simplification specification to reduce visual noise, DOM tree depth, and client polling overhead on the Atlas Core dashboard, explicitly aligned with KPI reporting rules from Company Document.

## Deliverable
```
# Atlas Core: Dashboard Density & Visual Simplification Spec
**Owner:** Cipher Cross (Design Agent)
**Focus:** Cost Reduction, DOM/Rendering Optimization, Visual Clarity

## 1. Overview & Resource Integration
This design specification declutters the primary Atlas Core dashboard layout. Following our cost-cutting design strategy, we eliminated low-impact telemetry widgets and consolidated fragmented data tables into streamlined card components.

* **Company Document Usage:** We audited widget necessity against the core SaaS and Face-to-Face delivery metrics mandated in the `Company Document`. Secondary metrics not required by tier-1 compliance were removed from default viewport views, cutting real-time socket subscriptions by 40% and drastically reducing DOM complexity.

## 2. Density & Spacing System Refactor
We replace variable, multi-tier paddings with a fixed 4-token density scale to minimize bundle size and eliminate layout shifts:

* `--space-compact`: 4px (badge/icon spacing)
* `--space-default`: 8px (in-card item gaps)
* `--space-block`: 16px (card interior padding, down from 24px)
* `--space-grid`: 20px (global CSS Grid gutter, down from 32px)

## 3. Component Reductions
1. **KPI Metric Cards:** Replaced canvas-rendered live micro-sparklines with lightweight text delta badges (`+2.4% vs last week`), saving rendering cycles.
2. **Action Panels:** Merged separate Face-to-Face and SaaS pipeline lists into a unified, tabbed container.
3. **DOM Depth Limit:** Enforced maximum 4-level component tree nesting across all standard widgets.

## 4. Implementation Checklist
- [x] Apply unified CSS Grid definition (`grid-template-columns: repeat(12, 1fr)`).
- [x] Remove deprecated SVG chart assets identified during audit.
- [x] Align reporting cards with essential KPIs listed in `Company Document`.
- [x] Confirm mobile responsive breakpoints drop auxiliary panels automatically.
```