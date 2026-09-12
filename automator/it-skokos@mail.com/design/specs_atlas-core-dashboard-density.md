# Atlas Core Dashboard Density Reduction Spec & Token Map
**Author:** Cipher Petrov  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D13 04:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification and token updates streamlining information architecture, spacing scales, and visual density for the Atlas Core dashboard.

## Deliverable
```
# Design Spec: Atlas Core Dashboard Density Reduction
Author: Cipher Petrov (Design)
Status: Ready for Engineering / Immediate Ship
Project: Atlas Core

## 1. Context & Business Alignment
Per our analysis of the "Business Document: Company Document", customer feedback identified high visual fatigue and slow triage times across Atlas Core's hybrid SaaS monitoring and face-to-face field dispatch panels. We referenced the "Business Document: Company Document" to determine critical operational KPIs, prioritize essential viewport elements, and establish default-hidden secondary telemetry.

## 2. Layout & Spacing System Overhaul
To reduce clutter while retaining critical metrics above the fold:
- Canvas Grid: 12-column responsive layout, 24px gutter (previously 12px cramped).
- Base Padding: Increased card interior padding from 8px (`space-2`) to 16px (`space-4`).
- Micro-Metric Consolidation: Merged 8 fragmented micro-widgets into 3 contextual KPI blocks (Active SaaS Nodes, Field Service Crews In-Transit, SLA Breach Risks).

## 3. UI Token Changes
```json
{
  "dashboard.card.padding": "16px",
  "dashboard.card.gap": "20px",
  "dashboard.header.lineHeight": "1.4",
  "dashboard.badge.compact": "4px 8px",
  "dashboard.dataGrid.rowHeight": "48px"
}
```

## 4. Component Hierarchy
1. Top Bar: Global tenant selector + 3 critical summary stats (Removed redundant sub-status pills).
2. Main Viewport: Primary interactive operational map + aggregated queue status.
3. Collapsible Drawer: Secondary log streams, raw API health, and audit trails moved to an on-demand slide-over panel.

## 5. Implementation & QA Checklist
- [ ] Update Tailwind config with unified spacing tokens (`p-4`, `gap-5`).
- [ ] Migrate data table rows from 32px dense mode to standard 48px baseline.
- [ ] Validate responsive behavior at 1440px, 1280px, and 1024px break points.
- [ ] Ship behind feature flag `atlas_core_dense_v2` for immediate staging validation.
```