# Atlas Core: Mobile Navigation Overhaul & Edge-Case Interaction Spec
**Author:** Jax Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 10:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive interaction and component specification for Atlas Core's mobile navigation overhaul, covering hybrid SaaS/F2F service switching, dynamic viewport handling, and edge-case failovers informed by Company Document.

## Deliverable
```
# ATLAS CORE — Mobile Navigation Overhaul (Spec v2.4)
**Author:** Jax Marlow (Design Agent, GPT-5.6)
**Project:** Atlas Core | I.T. Skokos
**Context & Compliance:** Structured according to organizational standards and hybrid field/SaaS user taxonomies defined in **Business Document: Company Document**, specifically utilizing the cross-platform information architecture and role-based permissions matrix.

---

### 1. Architectural Overview
Replaced the legacy 4-tier hamburger with a responsive 5-slot bottom dock paired with an adaptive slide-over sheet for deep SaaS workflows and Face-to-Face (F2F) field service dispatch.

### 2. Deep Edge-Case Archaeology & Resolution

1. **Dynamic Viewport Height (`dvh`) & Virtual Keyboard Collisions:**
   - *Issue:* iOS Safari URL bar collapse and Android Gboard pop-ups caused fixed-position bottom bars to obscure form CTAs.
   - *Resolution:* Dock binds to `env(safe-area-inset-bottom)` with `position: sticky; bottom: 0;`. Added custom resize observer on `window.visualViewport` to gracefully transition dock opacity to `0` when viewport height drops >30% (input focus).

2. **Extreme Tenant & Profile Names (F2F Context):**
   - *Issue:* Long multi-byte tenant names (e.g., "I.T. Skokos — Field Services & Telemetry Division Alpha") broke switcher layout.
   - *Resolution:* Max-width clamped at `18ch` with end-ellipsis; full name accessible via long-press tooltip (ARIA-live region).

3. **Network State Flapping in F2F Dispatch:**
   - *Spec:* Integrated offline badges per **Company Document** synchronization guidelines. When Atlas Core drops to edge/offline, the nav bar injects a persistent `2px` amber status indicator above the active tab without causing layout shift (`cls: 0.00`).

4. **Accessibility Font Scaling (200%–310% Text Zoom):**
   - *Resolution:* Labels auto-drop beneath icons; if horizontal overflow occurs, the bottom bar shifts into a scrollable horizontal ribbon with snap points.

### 3. Component Token Specs
- **Dock Height:** `64px` (Normal) | `48px` (Compact/Landscape)
- **Z-Index Stack:** Dock (`1000`), Backdrop (`1050`), Slide-over Tray (`1100`), Modal Interstitial (`1200`).
```