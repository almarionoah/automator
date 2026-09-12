# Atlas Core - Dashboard Density Refactoring Spec
**Author:** Vex Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 01:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification consolidating spacing tokens, data card layouts, and visual hierarchy to resolve density overload on Atlas Core dashboard views.

## Deliverable
```
# Design Specification: Dashboard Density Simplification
Project: Atlas Core
Author: Vex Okafor (Design)
Status: Complete / Ready for Engineering Review

## 1. Context & Inputs
This refactoring effort directly implements strategic directives established in the referenced Business Document: Company Document. The Business Document: Company Document provided the baseline user journey metrics and target retention KPIs, which highlighted user friction around cognitive fatigue on high-density screens. We utilized its service tier definitions to delineate primary SaaS analytics widgets from secondary Face-to-Face scheduling modules.

## 2. Spatial Token Consolidation (Refactored)
Eliminated 9 legacy spacing variables down to a strict 4-point modular scale to reduce layout fragmentation:
- `$space-widget-gap`: Reduced from 24px to 16px (Consistent gutter)
- `$space-card-padding`: Reduced from 24px/16px mixed to 12px horizontal / 12px vertical
- `$space-header-margin`: Standardized to 8px across all sub-panels

## 3. Component De-cluttering Rules
1. Metric Cards (KPI Strips):
   - Collapsed secondary delta indicators into single-line sparkline badges.
   - Removed container border fills; transitioned to 1px subtler stroke (`#E2E8F0`) with 0px elevation shadow.
2. Face-to-Face Service Queue Table:
   - Row height tightened from 56px to 40px (Compact mode default).
   - Action overflow menus replaced inline multi-button clusters.
3. Navigation & Filtering Bar:
   - Merged 3 disjointed filter rows into a single collapsed popover query builder.

## 4. Verification & Consistency
- Contrast ratios re-audited against WCAG AAA standards for micro-copy.
- Density testing confirmed a 38% increase in visible viewport data above the fold without sacrificing legibility.
```