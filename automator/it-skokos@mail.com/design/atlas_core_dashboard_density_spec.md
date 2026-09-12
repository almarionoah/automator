# Atlas Core - Dashboard Information Density Optimization Spec
**Author:** Kilo Cross  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D3 20:30  
## Summary

Design specification establishing optimized spatial tokens, typography scale, and progressive disclosure patterns to reduce dashboard cognitive load while preserving critical operational data.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Optimization
Author: Kilo Cross (Data Purist)
Project: Atlas Core
Status: Complete

## 1. Assumptions
- Target resolution: Standard 1080p desktop with 8px baseline grid.
- User persona: Operations managers tracking hybrid SaaS and face-to-face service KPIs.
- Default viewport density was flagged at >70% visual saturation with excessive competing card borders.

## 2. Layout & Spacing Token Adjustments
- Grid: 12-column fluid grid, max-width 1440px.
- Margins: Expanded from 16px to 24px (`$space-6`).
- Gutter: Increased from 12px to 16px (`$space-4`).
- Card Padding: Standardized to 20px internal padding (`$space-5`), replacing asymmetric 8px/12px padding.

## 3. Typography & Hierarchy
- Metric Value (H1): 28px/34px, tabular numerals (`font-feature-settings: 'tnum'`).
- Metric Label (Sub): 12px/16px uppercase, 60% opacity (`$color-neutral-600`).
- Secondary Deltas: Inline badges with max 2 elements per metric card (Value + Trend).

## 4. Visual Density Reduction Rules
- Border Removal: Eliminate 1px high-contrast container borders; replace with subtle background elevation (`$elevation-1`: `#FFFFFF` on `#F8FAFC`).
- Progressive Disclosure: Move secondary breakdown charts (regional distribution, historical audit logs) into modal drawers triggered on hover/click.
- Metric Consolidations: Group top-level metrics to 4 primary KPI cards (ARR, Active Service Sessions, Platform Uptime, F2F Booking Rate).

## 5. Implementation Tokens
```json
{
  "spacing.dashboard.card.padding": "20px",
  "spacing.dashboard.grid.gap": "16px",
  "typography.kpi.primary": "28px",
  "typography.kpi.secondary": "12px",
  "color.background.canvas": "#F8FAFC",
  "color.background.surface": "#FFFFFF"
}
```
```