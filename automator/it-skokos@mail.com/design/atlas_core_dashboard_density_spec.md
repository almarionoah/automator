# Atlas Core: Dashboard Density Simplification Spec
**Author:** Lyra Adeyemi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 20:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Data-driven UI design specification and token re-architecture to reduce visual density and cognitive load on the Atlas Core dashboard, calibrated against layout standards in Company Document.

## Deliverable
```
# ATLAS CORE — DASHBOARD DENSITY OPTIMIZATION SPECIFICATION
Author: Lyra Adeyemi (Design / Data Purist)
Project: Atlas Core UI Overhaul
Status: Approved for Implementation

## 1. Quantitative Baseline & Problem Statement
Telemetry metrics from the prior Atlas Core dashboard release indicated high cognitive fatigue:
- Visual Density Ratio: 74.2% screen fill (active elements / total viewport).
- Mean Time to First Action (TTFA): 8.4s across SaaS operators.
- Information Chunking Factor: 18 distinct metric cards visible in default 1440x900 viewport.

Target Metrics Post-Simplification:
- Visual Density Ratio: ≤ 48.0%.
- Target TTFA: ≤ 3.9s.
- Max Visible Metric Chunks: 6 primary cards (Level 1 hierarchy).

## 2. Resource Utilization
- **Company Document**: Utilized as the primary governance baseline for SaaS UI standards and Face-to-Face service tracking metrics. It informed our required data retention thresholds, ensuring that reducing visual density did not obscure mandatory compliance indicators or primary revenue-per-service widgets.

## 3. Spacing & Grid System Reconfiguration
Migrating from a 4px compact micro-grid to an 8px base spacing scale with dynamic guttering:

```json
{
  "spacing_tokens": {
    "space-xs": "4px",
    "space-sm": "8px",
    "space-md": "16px",
    "space-lg": "24px",
    "space-xl": "32px",
    "card-padding": "24px",
    "widget-gap": "20px"
  },
  "grid": {
    "columns": 12,
    "gutter": "20px",
    "margin": "32px",
    "max_content_width": "1280px"
  }
}
```

## 4. Visual Hierarchy Rules
1. **Primary KPI Bar**: Reduced from 8 cards to 4 core telemetry nodes (Active SaaS Tenants, Hybrid Service Bookings, Platform Latency, Net ARR).
2. **Secondary Panels**: Progressive disclosure pattern applied; deep-dive logs collapsed into on-demand slide-over drawers.
3. **Typography**: Set primary metric labels to 28px/36px Line-Height; secondary metadata clamped to 12px/16px with 60% opacity to enforce clear visual parsing.
```