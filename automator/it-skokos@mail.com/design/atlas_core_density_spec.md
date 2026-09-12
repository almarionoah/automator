# Atlas Core Dashboard Density Rationalization & Spatial Design Spec
**Author:** Ash Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 00:55  
**Inputs used:** Business Document (Company Document)  
## Summary

A UX spatial rhythm and density overhaul design specification for Atlas Core, reducing cognitive strain and honoring the human-centric principles outlined in Business Document: Company Document.

## Deliverable
```
# Design Specification: Atlas Core — Dashboard Density & Spatial Cadence

**Author:** Ash Nkosi (Lead Product Designer)
**Project:** Atlas Core (I.T. Skokos SaaS & Face-to-Face Services Platform)
**Focus:** Cognitive Calm, Progressive Disclosure, and Visual Breathing Room

---

### 1. Foundational Intent & Resource Attribution
In accordance with **Business Document: Company Document**, which establishes our hybrid service philosophy of balancing automated SaaS velocity with meaningful Face-to-Face human connection, this redesign eliminates the overwhelming metric gridlock on Atlas Core. The **Company Document** guided our prioritization matrix: service-critical KPIs receive contemplative focus, while secondary analytical telemetry shifts to contextual progressive reveal.

### 2. Spatial Rhythm & Grid Refinement
We replace the 12-column condensed layout with an 8pt organic spatial cadence to restore emotional equilibrium:
- **Canvas Margins:** Increased from `16px` to `48px` fluid (`min-width: 1440px`) to frame the workspace with dignity.
- **Component Inset (Padding):** Elevated from compact `8px/12px` to `24px` uniform internal rhythm.
- **Card Gutter Gap:** Restructured to `28px` with subtle elevated borders (`rgba(15, 23, 42, 0.04)`) over heavy drop-shadows.

### 3. Metric Card Architecture
*Before:* 18 competing micro-cards with dense sparklines.
*After:* 4 Primary Sentinel Cards + 1 Expandable 'Horizon Panel'.

- **Primary Anchor:** Face-to-Face Consult Queue & SaaS Health Index (Dominant 24pt Display Font, generous white space).
- **Secondary Metrics:** Bundled under intuitive collapsible accordions with smooth `180ms cubic-bezier(0.16, 1, 0.3, 1)` transitions.
- **Telemetry Sparsity:** Chart data points downsampled dynamically; micro-interactions provide precision via quiet hover tooltips.
```