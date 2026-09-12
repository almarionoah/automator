# Design Specification: Atlas Core Mobile Navigation Overhaul
**Author:** Zed Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 13:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-ready design specification and token configuration for the Atlas Core mobile navigation redesign, integrating SaaS dashboards and Face-to-Face booking pathways.

## Deliverable
```
# Design Spec: Atlas Core Mobile Navigation Overhaul (v2.4)
**Author:** Zed Fontaine (Design)
**Project:** Atlas Core | I.T. Skokos
**Status:** Ready for Implementation

## 1. Context & Business Alignment
This overhaul replaces the legacy hamburger menu with a bottom-docked navigation bar paired with a progressive disclosure tray. We referenced the **Company Document** to align the primary navigation tiers with our dual SaaS platform and Face-to-Face (F2F) service delivery models, ensuring zero-friction access to instant booking and active SaaS workspace monitors.

## 2. Navigation Architecture
- **Primary Bottom Bar (4 items):**
  1. `Workspace` (SaaS Metrics / Core Dashboard)
  2. `Services` (Hybrid Hub: SaaS Tools + F2F Service Appointments)
  3. `Quick Action [Center Fabricated FAB]` (Instant F2F Dispatch / New Query)
  4. `Activity` (Live Alerts & Session Timelines)
  5. `More` (Trigger for secondary menu & settings)

## 3. Component Specs & Layout Tokens
```json
{
  "mobileNav": {
    "height": "64px",
    "safeAreaBottom": "env(safe-area-inset-bottom, 16px)",
    "background": "rgba(18, 22, 28, 0.94)",
    "blur": "12px",
    "borderTop": "1px solid rgba(255, 255, 255, 0.08)",
    "tapTarget": {
      "minWidth": "48px",
      "minHeight": "48px"
    },
    "fab": {
      "diameter": "56px",
      "offsetY": "-18px",
      "accent": "#00E599",
      "icon": "plus-calendar"
    }
  }
}
```

## 4. Interaction Specs
- **Micro-interactions:** Haptic feedback on bottom-bar tab switch (`UIFeedbackType.selection`).
- **Drawer Transition:** Spring physics (`stiffness: 380, damping: 30`) on secondary 'More' sheet.
- **Breakpoints:** Active on viewport widths `<= 768px`; gracefully shifts to responsive rail at `769px+`.
```