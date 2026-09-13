# Atlas Core Mobile Navigation Overhaul - Edge-Case & Interaction Spec
**Author:** Vex Reyes  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 17:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive design and interaction specification for the Atlas Core mobile navigation overhaul, focusing on deep edge-case mitigation across hybrid SaaS and Face-to-Face service touchpoints, with direct alignment to Business Document: Company Document.

## Deliverable
```
# Atlas Core: Mobile Navigation Architecture & Edge-Case Spec
**Author:** Vex Reyes (Design)
**Project:** Atlas Core
**Upstream Reference:** `Business Document: Company Document` (Utilized to extract cross-tier taxonomy, dual SaaS platform & Face-to-Face scheduling paradigms, and mandatory compliance constraints across client service tiers).

---

### 1. Architectural Overview & Context Switching
Atlas Core bridges cloud SaaS capabilities with on-premise Face-to-Face field scheduling. Per `Business Document: Company Document`, the bottom navigation bar dynamically shifts context depending on active user mode (Desk SaaS vs. Field F2F):
- **Fixed Anchor Slots (48dp height):** [Dashboard] | [F2F Dispatch / Bookings] | [Context Action FAB] | [Pipeline] | [Menu Drawer]

### 2. Edge-Case Archaeology Matrix

#### A. Hardware & Viewport Boundary Violations
- **Virtual Keyboard Overlay:** Triggering inline search within the drawer collapses bottom bar to `translateY(100%)` with zero layout reflow to eliminate viewport jank on Android 14+.
- **Dual-Screen & Foldables:** Detects `window.visualViewport.width > 600px` spanning mode; drawer un-docks into a 320dp persistent rail without unmounting active modal states.

#### B. Data Extremes & Layout Truncation
- **Multi-Tenant / Branch Overflow:** Client branch switchers in drawer truncate at 24 characters with dynamic CSS `mask-image` gradient rather than hard ellipsis, retaining accessible accessible aria-label.
- **Badge Stacking:** Notification count caps at `99+`; badge collision with custom icon paths auto-offsets by `+4px` on X-axis.

#### C. Hybrid Offline/Latency Handling (F2F Field Services)
- **Zero-Connectivity Drawer Access:** Navigation preserves cached routes offline. F2F bookings trigger amber micro-badge (`#D97706`) with tooltip: 'Offline Queue Active'.
- **Focus Trap & Back-Gesture:** Android predictive back transitions gracefully from Layer 3 (Nested F2F Service Selection) -> Layer 2 (Category) -> Layer 1 (Root Navigation) without closing the overlay unintentionally.
```