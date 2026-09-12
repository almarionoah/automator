# Atlas Core - Mobile Navigation Overhaul: Edge-Case Specification & Interaction Matrix
**Author:** Pixel Ito  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 11:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UI/UX interaction specification and edge-case matrix for Atlas Core's mobile navigation system, bridging SaaS and Face-to-Face service touchpoints across constrained viewports.

## Deliverable
```
# Atlas Core — Mobile Navigation Overhaul (Spec v2.4)
**Author:** Pixel Ito (Design Agent)
**Reference Document:** `Business Document: Company Document` (Used to map hybrid SaaS platform permissions against Face to Face Services booking states and tier entitlements across responsive breakpoints).

---

### 1. Viewport & Hardware Edge-Case Matrix
- **Ultra-Narrow (320px - Galaxy Fold Front / iPhone SE1):**
  - Bottom bar collapses from 5 to 4 primary items; 5th item routes into 'More' overflow.
  - Label typography shifts to `font-size: 10px; line-height: 12px; letter-spacing: -0.2px`.
  - Touch target remains compliant at 48x48dp via invisible touch padding.
- **Safe-Area Dynamic Insets:**
  - Bottom Bar: `padding-bottom: max(env(safe-area-inset-bottom), 16px)`.
  - Handles dynamic Android 3-button vs gesture navigation switches without layout shift.
- **Landscape / Split-Screen (Aspect ratio < 4:3 or height < 500px):**
  - Converts bottom nav into a compact vertical side-rail (width: 56px) to preserve vertical data canvas.

### 2. Localization & Multi-Modal State Archeology
- **Text Expansion (+40% Localization):** Dynamic text truncation with marquee on active focus for extended strings (e.g., DE/FI translations of 'Appointment Management').
- **Degraded/Offline State:**
  - Offline badge anchored to F2F Booking icon with pulse animation indicating queued sync.
  - SaaS live metrics disable gracefully with skeleton states while retaining local F2F schedule cache.
- **Multi-Role Switching:** Single-tap profile context switch integrated directly into drawer header without full-page reloads.

### 3. Component Specs
- **BottomNav Container:** Elevation `Level 3` (0 -2px 8px rgba(0,0,0,0.08)), `backdrop-filter: blur(12px)`.
- **Active Tab Pill:** `background: var(--atlas-brand-subtle); color: var(--atlas-primary); border-radius: 9999px;`
```