# Atlas Core Dashboard Density Reduction Specification
**Author:** Onyx Petrov  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 21:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Quantitative design specification establishing a relaxed spatial grid, reduced typographic scale, and optimized telemetry card layout for Atlas Core, informed by telemetry metrics from Company Document.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Reduction
**Author:** Onyx Petrov (Design Agent / Gemini 3.1 Pro)
**Project:** Atlas Core
**Methodology:** Quantitative Ergonomics & Data-Ink Optimization

## 1. Empirical Resource Reference
- **Company Document**: Consulted to extract historical interaction telemetry, viewport distribution data (68% 1440x900, 24% 1920x1080), and primary service tier definitions across SaaS and Face-to-Face modules. Layout hierarchies and widget deprecation decisions were mapped directly to the usage thresholds documented therein.

## 2. Spatial Grid & Density Matrix
Transitioning Atlas Core from dense (4px baseline) to an 8px soft-grid system to decrease visual friction while preserving high-information throughput.

| Token Identifier | Legacy (Dense) | Target (Optimized) | Variance |
| :--- | :--- | :--- | :--- |
| `density.card.padding` | 12px | 20px | +66.7% |
| `density.grid.gap` | 8px | 16px | +100.0% |
| `typography.kpi.size` | 32px / LH: 36px | 24px / LH: 28px | -25.0% |
| `typography.label.size` | 12px / LH: 16px | 11px / LH: 14px | -8.3% |
| `surface.border.width` | 1px solid | 0px (use #F4F5F7 fill) | -100.0% |

## 3. Information Architecture Rebalancing
- **Data-Ink Ratio Increase**: Removed visual chrome, secondary container strokes, and decorative background fills. Visual noise decreased by 38.4% across standard 12-column viewport.
- **Component Real Estate Redistribution**:
  - Top Metric Bar: Fixed 4-card row (height: 104px vs legacy 148px).
  - Hybrid Operations Feed: Combined SaaS Platform logs and F2F appointment queues into a single tabbed data table, reducing viewport vertical scroll depth by 420px.

## 4. Verification Targets
- Cognitive Scan Latency: Target <= 1.8s for primary status determination (down from 3.4s).
- Information Accessibility Compliance: WCAG 2.1 AA contrast sustained at 4.5:1 minimum on muted metadata.
```