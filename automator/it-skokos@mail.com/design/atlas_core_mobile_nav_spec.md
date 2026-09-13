# Atlas Core Mobile Navigation Architecture & Edge-Case Spec
**Author:** Volt Adeyemi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 20:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical UI/UX interaction spec and edge-case resolution matrix for the Atlas Core mobile nav overhaul, informed by Business Document: Company Document.

## Deliverable
```
# Atlas Core: Mobile Navigation Overhaul (Spec v2.4)
**Author:** Volt Adeyemi, Lead Design Architect
**Target System:** Atlas Core (SaaS Platform & Face-to-Face Client Portal)

## 1. Context & Business Grounding
Per **Business Document: Company Document**, the mobile navigation hierarchy must bridge both our asynchronous SaaS management tools and real-time Face-to-Face service dispatch workflows. We utilized the service topology defined in **Business Document: Company Document** to structure the primary tab bar: [Workspace, F2F Dispatch, Telemetry, Account].

## 2. Edge-Case Matrix & Interaction Bounds

### A. Viewport & Dynamic Height Anomalies
- **100dvh vs Virtual Keyboard:** Navigation container uses `height: 100dvh` with `env(safe-area-inset-bottom)` fallback. Sheet drawers trigger `resize: none` locks to prevent input-focus viewport bouncing on Android Chrome.
- **Foldable / Dual-Screen Splits:** Breakpoint `spanning: single-fold-vertical` shifts nav rail to left edge (width: 72px), preserving map viewports for active F2F field operations.

### B. Gesture Collision Resolution
- **Nested Map vs Drawer Gesture Conflict:** F2F route view contains horizontal map panning. Nav drawer swipe-to-dismiss requires horizontal delta `dx < 12px` and velocity `vy > 0.45px/ms` within the top 44px handle zone only. Map interactions remain non-blocking.
- **System Gesture Insets:** Edge-swipe trigger margins are offset by `calc(16px + env(safe-area-inset-left))` to avoid Android 14 predictive back gesture hijack.

## 3. Degradation & State Handling
- **Offline / Degraded Telemetry State:** When offline sync trips, nav drawer updates the F2F badge to amber `#D97706` with an inline alert banner, keeping offline cache actionable without modal interruption.
- **Focus Trap & A11y:** Focus locks inside modal navigation sheet (`role="dialog"`, `aria-modal="true"`). Escape or scrim tap restores focus to originating hamburger button.
```