# Atlas Core Dashboard Density Simplification & Edge-Case Design Specification
**Author:** Jax Reyes  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 03:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UI architecture and layout specification simplifying dashboard density on Atlas Core, incorporating responsive edge-case rules, progressive disclosure, and tokenized spatial metrics.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Reduction
Author: Jax Reyes (Design / Edge-Case Archaeologist)
Project: Atlas Core | I.T. Skokos Platform

## 1. Executive Summary & Business Baseline
To resolve cognitive overload across hybrid SaaS analytics and face-to-face field dispatch views, this spec establishes a balanced 8pt layout grid with progressive disclosure mechanisms.

### Resource Reference
- Business Document: Company Document: Utilized to audit mandatory operational telemetry vs. secondary analytics across enterprise tiers. We mapped contractual SLA data points defined in the document to prevent accidental hiding of mission-critical dispatch metrics during density trimming.

---

## 2. Density Token Scale
- Base Spacing Grid: 8px
- Standard Widget Inset: 16px (reduced from legacy 24px)
- Inline Metric Gap: 12px horizontal / 8px vertical
- Minimum Touch Hit Target: 44px x 44px (Strict WCAG 2.5.5 compliance across hybrid tablet/pointer sessions)

---

## 3. Progressive Disclosure Architecture
- Primary Surface: 4 high-priority KPI cards + Live Dispatch Stream
- Collapsed Telemetry: Secondary server states and localized SLA telemetry collapsed into expandable side sheets (`Drawer: TelemetryDetail.vue`).
- Micro-Metric Pills: Max 3 inline tags before triggering `+N more` overflow tooltip.

---

## 4. Edge-Case Matrix
1. Extreme Aspect Ratios (32:9 Super-Ultrawide & 4:3 Legacy Kiosks):
   - Cap maximum dashboard width to 1600px centered; gutters scale dynamically (`margin: 0 auto`).
2. Localization String Expansion (e.g., German/Finnish text >35% width expansion):
   - Text containers employ multi-line clamp (2 lines max) with automatic font-size fallback (`14px` -> `12px`) before ellipsis truncation.
3. Dynamic Zero/Empty States:
   - If telemetry feed drops to 0 records, cards retain structured height (220px fixed) with skeleton baseline illustrations to prevent layout shifts.
4. Input Switching (F2F Field Tablet vs SaaS Desktop Mouse):
   - Media feature `@media (pointer: coarse)` increases action icon padding from 6px to 12px seamlessly.
```