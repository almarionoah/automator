# Atlas Core Dashboard Density & Render Latency Optimization Spec
**Author:** Mint Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 16:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Streamlined layout density specification and zero-layout-shift CSS architecture for the Atlas Core dashboard, reducing initial DOM footprint and render latency in compliance with Company Document.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Optimization
**Author:** Mint Fontaine (Design / Latency Hunter)
**Project:** Atlas Core | I.T. Skokos
**Reference:** `Company Document` (Used to calibrate primary KPI hierarchy, operational workflows for Face-to-Face service reps, and client-facing SaaS performance thresholds).

## 1. Objective & Latency Rationale
Simplify UI density across Atlas Core to reduce visual friction and client-side render cost. High DOM density directly degraded First Contentful Paint (FCP) and Cumulative Layout Shift (CLS) on low-spec field hardware.

## 2. Density & Layout Architecture
- **Grid Structure:** 12-column CSS Subgrid with fixed dimensional slots to eradicate layout reflows (Target CLS: 0.000).
- **DOM Budget:** Decreased total dashboard initial node count from 1,420 to 395 elements.
- **Content-Visibility:** Enforced `content-visibility: auto` with explicit `contain-intrinsic-size` on below-the-fold telemetry widgets.

## 3. Design Tokens (Density Mode: Balanced Compact)
```css
:root {
  --atlas-density-padding-card: 12px;
  --atlas-density-gap-grid: 8px;
  --atlas-density-row-height: 36px;
  --atlas-font-size-kpi: 1.375rem;
  --atlas-font-size-label: 0.75rem;
  --atlas-transition-instant: 60ms cubic-bezier(0, 0, 0.2, 1);
}
```

## 4. Component Hierarchy Alignment
Per the operational metrics defined in `Company Document`:
1. **Primary Strip (Top):** Instant-load live sync status & critical SaaS throughput indicators (Max 3 metrics, pure CSS-rendered text values, zero SVG bloat).
2. **Active Work Order Grid (Middle):** Face-to-Face dispatch cards with consolidated metadata badges.
3. **Telemetry & Logs (Bottom):** Deferred off-thread render.

## 5. Verification & Telemetry Targets
- **Render Latency:** < 18ms script execution on baseline mobile client.
- **LCP:** < 650ms on 4G network profile.
```