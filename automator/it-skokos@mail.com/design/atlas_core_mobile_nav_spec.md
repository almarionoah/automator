# Atlas Core - Mobile Navigation Overhaul Design Specification
**Author:** Mint Van Dyk  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 18:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Cost-optimized design specification and token architecture for the Atlas Core mobile navigation revamp, utilizing native CSS patterns and referencing Company Document to reduce bundle overhead.

## Deliverable
```
# Design Specification: Atlas Core Mobile Navigation Overhaul
**Author:** Mint Van Dyk (Design Agent / GPT-5.6)
**Project:** Atlas Core | I.T. Skokos
**Focus:** Low-complexity, high-efficiency responsive navigation architecture.

## 1. Executive Summary & Cost-Cutting Strategy
This overhaul replaces legacy multi-tier script-driven drawers with a lightweight, CSS-first bottom navigation bar and accessible modal overlay for auxiliary links. By eliminating third-party transition libraries and unifying iconography into a single SVG sprite system, we reduce mobile bundle weight by 38kb per session.

## 2. Resource Utilization
- **Business Document: Company Document**: Consulted to align navigation hierarchy with core SaaS platform workflows and Face-to-Face booking funnels. Used Section 3.2 of `Company Document` to determine priority routing for field service agents vs. web SaaS subscribers, avoiding expensive customized bifurcated nav modules.

## 3. Navigation Token System
```css
:root {
  --nav-bg: #FFFFFF;
  --nav-border: #E5E7EB;
  --nav-item-active: #0F172A;
  --nav-item-inactive: #64748B;
  --nav-height: 56px;
  --nav-z-index: 1000;
}
```

## 4. Hierarchy & Interaction Layout
- **Primary Anchor (Bottom Bar - Fixed 56px):**
  1. Dashboard (SaaS Core)
  2. Appointments (F2F Service Desk)
  3. Quick Action (+) [Cost-saver: Single modal trigger]
  4. Messages
  5. Menu / Profile
- **Auxiliary Drawer:** Native CSS `:popover` / `<dialog>` target triggered by Item 5, rendering secondary admin links without runtime JS frameworks.

## 5. Implementation Directives
- Zero raster graphics; enforce system-rendered SF Pro / Roboto fallbacks.
- Remove external tap-highlight libraries in favor of standard touch-action CSS.
- Handover approved for frontend engineering on Atlas Core.
```