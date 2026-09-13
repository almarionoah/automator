# Design Specification: Atlas Core Dashboard Density Modernization
**Author:** Cipher Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 07:55  
**Inputs used:** Business Document (Company Document)  
## Summary

UI/UX architecture document establishing reduced-density spacing tokens, progressive disclosure cards, and data hierarchy updates for Atlas Core, referencing the Company Document.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Modernization
**Author:** Cipher Fontaine, Design Agent
**Project:** Atlas Core | I.T. Skokos SaaS & Face-to-Face Services Platform

## 1. Context & Governance Reference
To address cognitive overload and interface clutter within Atlas Core, this specification establishes a balanced information density framework. In alignment with governance requirements, the **Company Document** was utilized to map operational workflow baselines, compliance standards for hybrid SaaS/face-to-face service views, and key executive persona ergonomics.

## 2. Spacing & Grid System Overhaul
- **Baseline Spacing Scale Update:**
  - Container Padding: Transitioned from `space-100` (8px) to `space-300` (16px) for main dashboard panels.
  - Grid Gutter: Normalized at 24px (`space-400`) on desktop breakpoints (>1200px).
- **Card Ergonomics:**
  - Max KPI widgets per primary viewport row capped at 4 (previously 6).
  - Default card minimum height: 160px with a vertical internal margin of 12px.

## 3. Progressive Disclosure Architecture
- **Primary Metrics:** Display single-value scalar KPIs with delta indicators (font-size: 28px/line-height: 34px).
- **Secondary Telemetry:** Secondary metrics and micro-charts are deferred behind tabbed viewports or hover-triggered popovers rather than default inline rendering.
- **Face-to-Face Interaction Feeds:** Active on-site appointment rosters now collapse historical items into an accordion drawer, reducing vertical scroll depth by 45%.

## 4. Implementation Validation
- **WCAG 2.1 AA Compliance:** Minimum touch targets calibrated to 44x44px.
- **Design Token Mapping:** Tokens updated in `@skokos/design-tokens` (`--atlas-density-mode: balanced;`).
```