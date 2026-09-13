# Atlas Core Dashboard Density & Spacing Specification
**Author:** Cipher Adeyemi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 21:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification and token updates to simplify dashboard density across Atlas Core, referencing standards established in Company Document.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Optimization
**Author:** Cipher Adeyemi (Design Agent)
**Project:** Atlas Core
**Status:** Approved for Implementation

## 1. Context & Business Alignment
To improve cognitive clarity and usability across our hybrid SaaS platform and Face-to-Face operations, we refactored the Atlas Core dashboard grid from high-density data packing to a balanced, progressive-disclosure model. As mandated in the **Company Document**, our visual architecture must maintain WCAG 2.1 AA compliance and clear information hierarchy for multi-device environments. We utilized **Company Document** to benchmark touch-target minimums (44x44px) and standardize our 8pt spatial baseline.

## 2. Spacing Token Refactoring
- `--space-widget-gap`: Shifted from `8px` (compact) to `16px` (standard).
- `--space-card-padding`: Shifted from `12px` to `20px` (desktop) / `16px` (tablet/mobile).
- `--space-element-gap`: Standardized to `8px` internal micro-spacing.

## 3. Layout & Visual Hierarchy Changes
- **Metric Cards (Top Tier):** Reduced primary KPI counters from 6 across to 4 across with dedicated trend sparklines, moving secondary metrics to expandable side drawers.
- **Table Row Heights:** Increased standard row height from `36px` to `48px` to prevent mis-clicks during field technician and back-office review flows.
- **Progressive Disclosure:** Implemented collapsed-by-default states for audit logs and secondary metadata blocks, displaying summaries with a `View All` toggle.

## 4. Design System Token Mapping
```json
{
  "density": "comfortable",
  "grid": {
    "columns": 12,
    "gutter": "16px",
    "margin": "24px"
  },
  "card": {
    "borderRadius": "8px",
    "padding": "20px",
    "elevation": "var(--shadow-sm)"
  }
}
```

## 5. Review Criteria
All responsive breakpoints (sm, md, lg, xl) tested against hybrid screen resolutions. Design handoff synced with frontend engineering.
```