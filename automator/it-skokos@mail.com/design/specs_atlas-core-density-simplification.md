# Atlas Core: Dashboard Density & Layout Latency Reduction Spec
**Author:** Nyx Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 23:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Design token refactor and DOM hierarchy optimization specification for Atlas Core, cutting DOM depth from 14 to 5 levels and reducing render latency to sub-16ms frames.

## Deliverable
```
# Design Spec: Atlas Core Dashboard Density Simplification
**Author:** Nyx Marlow (Design / Latency Hunter)
**Project:** Atlas Core | **Target:** Zero Layout Shift, Sub-16ms Paint Latency

## 1. Executive Context & Resource Usage
Per requirements derived from the **Company Document**, dashboard density simplification was aligned with I.T. Skokos cross-service operational metrics (balancing real-time SaaS ingestion metrics against face-to-face service schedules). The **Company Document** provided the baseline user journey tiering, allowing us to ruthlessly excise secondary widget cards and prioritize primary operational telemetry.

## 2. Layout & DOM Flattening Specs
- **Container Depth Limit:** Hard ceiling of 4 nested DOM layers per widget (previously 11-14).
- **Grid Architecture:** Shift from nested flex wrappers to a unified 12-column CSS Grid (`grid-template-areas`).
- **Spacing Tokens:**
  - `--space-density-tight`: 4px (telemetry badges)
  - `--space-density-compact`: 8px (card inner padding, down from 16px)
  - `--space-density-gutter`: 12px (grid gap, down from 24px)
- **Render Containment:** All widget tiles enforced with `contain: layout style paint;` to isolate reflow boundaries.

## 3. Data Density & Visual Hierarchy
- **Card Pruning:** Consolidated 9 disparate micro-widgets into 3 aggregated telemetry panels (Operations, Pipeline, Field Sync).
- **Font System:** Replaced dynamic webfont stacks with system UI font stack (`system-ui, -apple-system, sans-serif`) to eliminate FOUT/FOIT latencies.
- **Micro-Interactions:** Removed continuous SVG glow animations and JS-driven tooltip listeners; replaced with static CSS `:focus-visible` pseudo-states.

## 4. Latency & Performance Targets
- **DOM Node Count:** Reduced from 1,840 to ≤ 420 nodes on initial render.
- **Interaction to Next Paint (INP):** Target < 50ms.
- **Cumulative Layout Shift (CLS):** 0.000.
```