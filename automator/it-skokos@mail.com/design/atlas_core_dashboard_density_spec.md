# Atlas Core Dashboard Density Simplification Spec
**Author:** Prism Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 14:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification and UI token updates to reduce visual clutter and simplify dashboard density across Atlas Core, aligned with business tiering from Company Document.

## Deliverable
```
# Design Spec: Atlas Core Dashboard Density Simplification
**Designer:** Prism Marlow | **Project:** Atlas Core | **Status:** Ready for Dev

## 1. Context & Business Alignment
To reduce cognitive overload for dual SaaS and Face-to-Face operators, we refactored the Atlas Core dashboard density. We referenced **Business Document: Company Document** to determine widget priority, ensuring high-value service-tier metrics and client appointment queues receive primary real estate while secondary telemetry is moved to progressive disclosure drawers.

## 2. Spacing & Grid Adjustments
- **Base Grid:** Migrated from 4px micro-grid to 8px proportional grid.
- **Card Padding:** Increased from `8px` (`$space-xs`) to `16px` (`$space-sm`) on desktop; `12px` on tablet.
- **Container Gaps:** Normalized grid row/column gap to `16px` (down from chaotic mixed `4px`-`24px`).
- **Max Viewport Density:** Capped default widgets at 6 primary cards per viewport.

## 3. Component Updates
### A. KPI Metric Cards (`MetricCard.tsx`)
- Deprecated inline sparklines on secondary metrics.
- Primary metric font size normalized: `text-2xl font-semibold` (`24px/32px`).
- Added overflow dropdown for raw export and audit history.

### B. Face-to-Face Schedule Feed (`ScheduleWidget.tsx`)
- Grouped appointments by active time-block (Morning/Afternoon/Evening) rather than an unsegmented flat list.
- Status badges condensed to monochrome dot indicators with hover tooltips.

## 4. Design Tokens (Extract)
```json
{
  "density": {
    "card-padding-default": "1rem",
    "card-gap": "1rem",
    "header-height": "3.5rem",
    "table-row-height": "2.75rem"
  },
  "typography": {
    "kpi-value": "1.5rem",
    "kpi-label": "0.875rem",
    "widget-title": "1rem"
  }
}
```

## 5. Next Steps
- Hand off token constants to Frontend for immediate integration into `@atlas/ui-kit`.
- Review build in staging against 1080p and 1440p standard resolutions.
```