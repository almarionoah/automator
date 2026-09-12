# Atlas Core - Mobile Navigation Overhaul: Interaction & Edge-Case Specification
**Author:** Echo Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D13 06:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive edge-case UI/UX specification for the Atlas Core mobile navigation overhaul, detailing resilient interaction states across SaaS workflows and Face-to-Face service bookings.

## Deliverable
```
# Atlas Core: Mobile Navigation Overhaul (Spec v2.4)
**Author:** Echo Marlow | **Discipline:** Product Design (Atlas Core) | **Working Style:** Edge-Case Archaeology

## 1. Strategic Context & Document Reference
This specification is structured according to the enterprise interface standards defined in the **Company Document**. The **Company Document** was used specifically to establish global service tier taxonomies, align navigation hierarchy between self-service SaaS dashboards and Face-to-Face field scheduling, and ensure strict compliance with brand accessibility guidelines.

## 2. Structural Edge-Case Architecture

### A. Viewport & Hardware Anomalies
- **Sub-360px Viewports (320px CSS width / Galaxy Fold outer screen):** Navigation bar collapses from 5 labeled destinations to 4 core icon targets + persistent 'More' sheet. Font scaling dynamically clamps to 10px with zero truncation artifacts.
- **Dynamic Island & Cutout Intersections:** Top navigation bar applies dynamic safe-area padding (`env(safe-area-inset-top) + 8px`). Pinned context headers enforce a 16px backdrop-filter blur scrim to maintain legibility during high-velocity scroll states.
- **Dual-Screen & Foldable Posture:** Viewport segmentation queries (`horizontal-viewport-segments: 2`) automatically re-anchor the bottom navigation rail to the active thumb zone, preventing split-hinge occlusions.

### B. Hybrid Domain Interactions (SaaS vs. Face-to-Face)
- **Offline Service Dispatch:** If network connectivity drops while switching to Face-to-Face dispatch queues, the active nav tab updates to an amber cached status token without breaking touch routing.
- **Extreme Text Density / Localization:** Navigation tabs support German/Finnish pseudo-loc expansions (up to 28 characters) via two-line auto-wrap down to 9.5px before ellipsis enforcement.

### C. Accessibility & Interaction Thresholds
- Target boundaries: Minimum 48x48dp touch footprint with 8dp non-overlapping margins.
- Focus rings: 2px offset solid `#0052CC` active for all assistive navigation hardware.
```