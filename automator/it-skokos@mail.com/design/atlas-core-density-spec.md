# Atlas Core - Dashboard Density Simplification Spec
**Author:** Nyx Ito  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 13:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic UI design spec and layout token updates reducing cognitive load and density across Atlas Core dashboard widgets, grounded in metrics priority from the Business Document: Company Document.

## Deliverable
```
# UI Spec: Atlas Core Dashboard Density Simplification
**Author:** Nyx Ito | Design
**Status:** Ready for Engineering Handoff

## 1. Context & Business Reference
To optimize operator workflows across SaaS metrics and Face-to-Face booking workflows, we refined the Atlas Core primary dashboard density. In accordance with **Business Document: Company Document**, we cross-referenced operational KPI priority rankings to determine what stays top-level and what collapses into progressive disclosure drawers.

## 2. Layout & Spacing Token Changes
Replaced rigid 8px micro-grid packing with responsive comfortable density tiers:
- `--atlas-widget-gap`: Reduced from dense 8px grid to unified `16px` (`spacing-md`).
- `--atlas-card-padding`: Standardized to `20px` (was inconsistent 8px/12px/24px).
- `--atlas-header-height`: Compacted from `64px` to `52px` to preserve vertical real estate.

## 3. Component Hierarchy Reductions
1. **Primary KPI Strip (Top Grid):**
   - Consolidated 8 fragmented stat tiles into 4 composite metric cards (SaaS ARR, Active F2F Dispatches, Seat Utilization, SLA Health).
   - Secondary variance charts hidden by default, accessible via on-hover tooltip drilldown.
2. **Operations Data Table:**
   - Row height standard: `40px` (Comfortable) with toggle for `32px` (Dense).
   - Removed inline action buttons; unified under single overflow menu `...` per row.
   - Truncated secondary metadata (IDs, legacy tags) into flyout preview panel.
3. **F2F Service Schedule Widget:**
   - Switched from full 7-day expanded block view to a collapsed daily agenda with quick-filter pills.

## 4. CSS Token Updates (Atlas Core)
```css
:root {
  --atlas-density-mode: 'comfortable';
  --atlas-space-card: 1.25rem;
  --atlas-space-stack: 1rem;
  --atlas-table-row-h: 2.5rem;
  --atlas-kpi-font-size: 1.75rem;
}
```

## 5. Next Steps
- Handoff tokens to frontend team.
- Validate telemetry on click-depth vs bounce rates post-release.
```