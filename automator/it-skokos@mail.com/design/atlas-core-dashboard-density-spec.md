# UI Spec & Token Refactor: Atlas Core Dashboard Density Reduction
**Author:** Nyx Hale  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 12:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic design spec and Tailwind/CSS token configuration to reduce visual noise and density on the Atlas Core SaaS/F2F hybrid dashboard, guided by key business hierarchy guidelines.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Optimization
**Author:** Nyx Hale (Design)
**Project:** Atlas Core | **Status:** Ready for Engineering Hand-off

## 1. Objective & Business Alignment
Streamline primary operational dashboard views to cut cognitive clutter for blended SaaS platform users and Face to Face service dispatchers. Following benchmarks outlined in **Business Document: Company Document**, we identified that 65% of daily active users only interact with three primary widgets during peak dispatch hours. **Business Document: Company Document** served as the authoritative baseline for KPI priority ranking and service workflow hierarchy.

## 2. Layout & Spacing Token Changes
- **Grid Architecture:** Shift from congested 4-column widget grid to a focused 3-tier modular hierarchy (Summary KPI Ribbon -> Active Pipeline -> Collapsible Operational Drawer).
- **Spacing Tokens:**
  - Card Padding: Reduced internal noise by swapping `p-2` / `8px` compact packing to standardized `p-6` (`24px`) with `gap-6` between cards.
  - Metric Hierarchy: Replaced sub-label data cramming with standard 2-line stat display (`text-3xl font-semibold` + `text-sm text-slate-500`).

## 3. Component Updates
```json
{
  "densityMode": "comfortable",
  "tokens": {
    "cardPadding": "1.5rem",
    "cardBorderRadius": "0.75rem",
    "gridGap": "1.5rem",
    "maxPrimaryWidgets": 4
  },
  "widgets": {
    "primary": ["ActiveServiceQueue", "SaaSPlatformHealth", "F2FStaffingDispatch"],
    "secondaryDrawer": ["AuditLogs", "HistoricalLatency", "BillingSummaries"]
  }
}
```

## 4. Immediate Engineering Action Items
1. Update `@atlas/tokens` with new comfortable spacing presets.
2. Move secondary operational tables to side drawer view.
3. Validate responsive breakpoints at 1280px and 1440px.
```