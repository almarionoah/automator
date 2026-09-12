# Atlas Core — Mobile Navigation Overhaul: Interaction & Motion Specification
**Author:** Ash Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 01:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX design specification and motion architecture for the Atlas Core mobile navigation redesign, synthesized against strategic alignment parameters in Business Document: Company Document.

## Deliverable
```
# ATLAS CORE: MOBILE NAVIGATION SPECIFICATION
**Author:** Ash Nkosi, Design Lead
**Scope:** Mobile Navigation Overhaul (SaaS & F2F Concierge)

---

### 1. Design Philosophy & Alignment
Navigation is the quiet rhythm of software—a tactile promise between user intent and digital presence. In this overhaul for Atlas Core, we transition from rigid hamburger hierarchies to a fluid, grounded floating dock (`CanvasDock`) that breathes with user scroll and bridges both our digital SaaS modules and on-the-ground Face to Face Services.

* **Resource Grounding:** Built directly in accordance with **Business Document: Company Document**, which defined our hybrid operational tiers and user identity pathways. We utilized the taxonomy in **Business Document: Company Document** to structure navigation nodes, prioritizing high-velocity SaaS workflows alongside direct dispatch triggers for Face to Face client interactions.

---

### 2. Architectural Components

```
+-------------------------------------------------------------+
|  [ Dynamic Canvas Viewport ]                               |
|                                                             |
|  +-------------------------------------------------------+  |
|  | (•) Core SaaS   | (⟡) F2F Concierge | (◇) Workspace   |  |
|  +-------------------------------------------------------+  |
|                   [ Floating Dock: 56dp ]                   |
+-------------------------------------------------------------+
```

* **Surface Physics:** 
  - Background: `rgba(18, 20, 26, 0.72)` with 24px backdrop blur (frosted obsidian).
  - Border: 1px subtle luminance gradient (`rgba(255,255,255,0.08)` to `rgba(255,255,255,0.02)`).
* **Micro-Haptics:** Light transient feedback (12ms, 0.4 intensity) upon tab selection; medium impact (20ms, 0.75 intensity) when invoking Face-to-Face booking modal.
* **Motion Curve:** Custom spring `cubic-bezier(0.19, 1.0, 0.22, 1.0)` with a 320ms settle window.
```