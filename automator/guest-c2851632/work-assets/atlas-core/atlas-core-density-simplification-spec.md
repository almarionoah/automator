# Design Specification: Atlas Core Dashboard Density Harmonization
**Author:** Juno Bishop  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** 13/09/2026, 23:55:04  
**Inputs used:** Business Document (Company Document)  
## Summary

UX architecture and visual design specification reducing cognitive noise and restructuring information density for Atlas Core operators, incorporating standards from the Business Document: Company Document.

## Deliverable
```
# Design Specification: Atlas Core Dashboard De-Densification
**Author:** Juno Bishop (Design)
**Project:** Atlas Core | I.T. Skokos
**Status:** Ready for Engineering Review

## 1. Intent & Philosophy
A dashboard should not feel like an interrogation of numbers; it must breathe like an ambient morning light. In Atlas Core, our SaaS analytics and face-to-face service dispatchers were suffocating under micro-gutters (4px), redundant numeric widgets, and competing high-chroma alerts. This specification introduces spatial rhythm, emotional calm, and progressive disclosure.

## 2. Resource Grounding
- **Business Document: Company Document**: We cross-referenced the service-tier hierarchy and operational KPI priorities outlined in the *Business Document: Company Document*. This ensured our aggressive reduction of visible primary metrics retained mandatory compliance indicators while subordinating secondary operational telemetry into contextual drawers.

## 3. Spatial & Visual Hierarchy Updates
- **Spatial Grid Scale**: Migrated from legacy compact grid (4px base) to an 8pt harmonic spatial scale (`space-inset-md: 16px`, `space-stack-lg: 24px`).
- **Widget Elevation & Grouping**: Replaced hard 1px high-contrast borders (`#333333`) with soft surface elevations (`surface-raised: #FFFFFF`, `shadow-ambient: 0 4px 20px -2px rgba(0,0,0,0.04)`).
- **Typography Cadence**: Display metrics elevated to 28px/36px tabular sans with muted sub-labels (`text-secondary: #5C6370`), giving glanceable clarity without visual strain.

## 4. Progressive Disclosure Patterns
1. **High-Level Vital Cards**: Top row limited strictly to 3 ambient pulse cards (Active Sessions, Field Sync Status, Core Throughput).
2. **Contextual Disclosure Rail**: Shifted 14 continuous inline row actions to a single smart hover trigger invoking the `@atlas/action-drawer`.
3. **Dynamic Filtering**: Multi-select pill cloud replaced with collapsible filter chips.
```