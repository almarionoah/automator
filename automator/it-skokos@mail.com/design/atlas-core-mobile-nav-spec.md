# Atlas Core - Mobile Navigation Overhaul: Interaction & Edge-Case Specification
**Author:** Onyx Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 09:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive interaction design and edge-case architectural specification for the Atlas Core mobile navigation overhaul, unifying SaaS management and Face to Face service workflows.

## Deliverable
```
# Atlas Core — Mobile Navigation Overhaul Specification
Author: Onyx Marlow, Design (Edge-Case Archeologist)
Project: Atlas Core | Platform: I.T. Skokos Hybrid SaaS & F2F Engine

## 1. Context & Business Integration
This overhaul restructures mobile information architecture across dual-mode operations (Cloud SaaS Tenant vs. In-Person F2F Service Dispatch). In crafting this system, I directly referenced **Business Document: Company Document** to map service tier hierarchy, SLA-bound dispatch controls, and compliance-mandated touch targets, ensuring in-field operators and digital admins share an uninterrupted navigation model.

## 2. Navigation Architecture & Component Matrix
- **Primary Anchor**: Bottom Dynamic Dock (48dp min touch target, elevation 8dp, blur 16px).
- **F2F Context Switcher**: Quick-toggle drawer for live client check-ins vs. analytics.
- **Secondary Sheet**: Progressive modal expanding from 45% peek to 95% viewport.

## 3. Excavated Edge-Cases & Behavioral Resolutions
- **Extreme Dynamic Type (200% Accessibility)**: Text wraps with vertical auto-layout stacking; icon-only labels switch to text-under-icon with zero truncated glyphs.
- **Foldable & Split-Screen Viewports**: Dock gracefully switches to floating rail (left/right configurable) when horizontal width > 600dp.
- **Gesture Collisions**: Bottom sheet swipe down overrides native OS back gesture via 150ms directional threshold lock (dy/dx > 1.8).
- **Offline F2F Mode**: Status banner injects at z-index 100 without pushing navigation items off-screen; persistent cache pill appears inside the floating dock.
- **RTL & Bi-Directional Layouts**: Full mirroring of drawer origin, gesture velocity curves, and breadcrumb chevron vectors.
```