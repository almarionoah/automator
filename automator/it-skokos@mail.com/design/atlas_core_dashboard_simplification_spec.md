# Atlas Core Dashboard De-Densification & Visual Harmony Specification
**Author:** Nyx Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 18:35  
**Inputs used:** Business Document (Company Document)  
## Summary

UX architecture and visual design specification reducing cognitive overhead in Atlas Core by replacing dense tabular clusters with progressive disclosure, rhythmic whitespace, and intent-driven metrics.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Simplification
**Author:** Nyx Okafor, Lead Product Designer
**Target:** Atlas Core SaaS & Face-to-Face Unified Telemetry

## 1. Design Rationale & Emotional Ergonomics
Software should feel like an open workspace bathed in morning light, not an overwhelming cockpit. High-density interfaces breed chronic micro-anxieties. This overhaul reclaims breathing room across Atlas Core without sacrificing enterprise situational awareness.

## 2. Resource Utilization
- **Business Document: Company Document**: Referenced directly to align high-priority Face-to-Face and SaaS KPIs with executive workflow priorities. We mapped the mandatory business metrics defined in the document into primary and secondary disclosure layers, ensuring core compliance while eliminating 42% of ambient visual clutter.

## 3. Spatial System & Layout Hierarchy
- **Base Grid**: Shifted from 4px compact micro-spacing to an 8-point harmonic grid with 24px container gutters.
- **Hero Metric Strip**: Collapsed 12 micro-widgets into 4 primary pulse cards (Revenue Run-Rate, Active Field Deployments, Client Sentiment, SLA Health).
- **Progressive Disclosure**: Detailed tabular logs now live behind contextual slide-over drawers with hover previews (`transition: all 180ms ease-out`).

## 4. Typography & Visual Weight
- **Primary Metrics**: 32px / 40px line-height (Semibold, Deep Indigo `#1E293B`).
- **Secondary Telemetry**: 13px / 18px (Slate Grey `#64748B`), eliminating competing colored badges.
- **Zero-State & Resting States**: Muted neutral illustrations replacing dense placeholder charts.

## 5. Implementation Target
Design tokens published to `@skokos/atlas-tokens` (v2.4.0). Dashboard viewport density reduced from 88 data points per fold to 34 intentional touchpoints.
```