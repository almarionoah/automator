# Atlas Core - Mobile Navigation Architecture & Edge-Case Design Specification
**Author:** Mint Adeyemi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 09:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive design and interaction specification for the Atlas Core mobile navigation overhaul, focusing on micro-viewports, foldable transitions, hybrid SaaS/F2F service workflows, and accessibility edge cases.

## Deliverable
```
# DESIGN SPECIFICATION: Atlas Core Mobile Navigation Overhaul (v2.4)
**Author:** Mint Adeyemi (Design / Edge-Case Archaeologist)
**System:** Atlas Core Design System | SaaS & Face-to-Face Services

---

### 1. Context & Resource Attribution
This architecture directly implements the brand taxonomy, compliance baselines, and service routing rules outlined in the **Company Document** (Business Document). The **Company Document** was specifically utilized to reconcile the IA collision between SaaS multi-tenant dashboards and Face-to-Face service booking logs, ensuring unified tier hierarchy without contextual fragmentation.

### 2. Viewport Extremes & Breakpoint Behavior
- **Micro-Viewports (320px - iPhone SE 1st Gen / Folded Cover):**
  - Primary nav items collapse to a single-column bottom sheet drawer.
  - Tenant switcher transforms into a compact badge; avatar shrinks to 24px.
  - Max text string truncation at 16ch with trailing ellipsis and accessible aria-label expansions.
- **Dual-Screen / Foldables (e.g., Galaxy Z Fold 280px -> 840px):**
  - Dynamic posture observer triggers drawer-to-rail morphing without unmounting active nested flows.
- **Vertical Clearance Edge Case (Landscape < 420px height):**
  - Nav drawer header pinned; body becomes independently scrollable with a 48px gradient bleed indicating overflow.

### 3. Gesture & Hardware Edge Cases
- **Safe Area Insets:** Strict enforcement of `env(safe-area-inset-bottom)` + `env(safe-area-inset-top)` on floating action anchors to prevent Dynamic Island and Home Bar overlap.
- **Multi-Touch Collision:** Pointer-events disabled across drawer backdrop during touchdrag transitions to prevent ghost clicks on background SaaS data tables.
- **Keyboard Offset:** Integrated visualViewport API listener; mobile drawer auto-scrolls the active F2F location search input above virtual keyboard boundaries.

### 4. Accessibility & RTL Validation
- **200% Font Scaling (WCAG AAA):** Labels wrap into vertical flex containers; tap targets maintain minimum 48x48dp bounding boxes regardless of scale.
- **RTL Mirroring:** Directional glyphs flipped; drawer slide vector inverted (`translateX(100%)` to `translateX(-100%)`). Focus lock verified for screen readers via `aria-modal="true"` and cyclical tab trapping.
```