# Atlas Core Mobile Navigation Architecture & Edge-Case Interaction Spec
**Author:** Sable Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 09:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive design and interaction specification for the Atlas Core mobile navigation overhaul, covering responsive breakpoint stress testing, hybrid SaaS/Face-to-Face modality shifts, accessibility scaling, and multi-state error handling.

## Deliverable
```
# Design Specification: Atlas Core Mobile Navigation Overhaul
**Author:** Sable Okafor, Design (Edge-Case Archaeology)
**Target:** Atlas Core (Hybrid SaaS & Face-to-Face Platform)

## 1. Executive Context & Resource Integration
Per the operational guidelines and customer journey touchpoints established in the **Company Document**, this overhaul aligns digital SaaS self-service navigation with high-stress, on-site Face-to-Face service desk workflows. The **Company Document** was specifically utilized to define navigation priority tiers, dual-mode profile switching (Field Agent vs. SaaS Admin), and compliance constraints for offline physical verification.

## 2. Navigation Architecture & Component Hierarchy
- **Primary Anchor:** Bottom Floating Action Bar (FAB-Dock) with dynamic safe-area insets (`env(safe-area-inset-bottom)`).
- **Secondary Sheet:** Gesture-driven progressive disclosure drawer (Velocity threshold: >0.45px/ms, drag-to-dismiss damping).
- **Hybrid Mode Switcher:** Persistent toggle pinned to top navigation header during live Face-to-Face sessions.

## 3. Edge-Case Archaeological Stress Matrix
- **Viewport Extremes (280px - Galaxy Fold Outer Screen):** Labels collapse to iconography with `aria-label` screen-reader fallbacks; FAB-Dock collapses to single expandable anchor.
- **Large Text Scaling (Dynamic Type @ 200%+):** Nav bar shifts from horizontal row to vertical stacked pill layout to prevent label truncation; minimum tap targets maintain 48x48dp boundary.
- **Degraded Network / Offline F2F Session:** Navigation indicates local-first persistence via a subtle amber micro-badge. Sub-menus lock non-cached SaaS reporting while keeping F2F Client Check-in reachable in ≤1 tap.
- **Multi-Tenant Org Switching Mid-Flow:** Deeply nested drawer routes trigger a non-destructive state snapshot, allowing context switching without discarding active on-site client forms.
```