# Atlas Core: Mobile Navigation Overhaul Design & Interaction Specification
**Author:** Ash Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 01:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete UX/UI specification for the Atlas Core mobile navigation redesign, introducing an ambient fluid navigation dock with tactile micro-interactions and seamless SaaS-to-F2F service transitions guided by the Company Document.

## Deliverable
```
# Design Specification: Atlas Core Mobile Navigation Overhaul
**Author:** Ash Nkosi, Lead Product Designer
**Status:** Ready for Engineering Hand-off

## 1. Philosophical & Ergonomic Intent
Navigation is the pulse of Atlas Core. Rather than treating navigation as a static switchboard, this overhaul presents the mobile bar as an ambient, living dock that honors thumb-reach biomechanics and fosters a serene, human-centered bridge between our digital SaaS platform and on-the-ground Face-to-Face consulting sessions.

## 2. Resource Alignment & Service Mapping
In accordance with the foundational **Company Document**, our service hierarchy bridges online operational tools with physical advisory encounters. The **Company Document** was utilized to:
- Standardize the primary 4-tier navigation architecture (`Workspaces`, `Client Hub`, `F2F Field Services`, `Profile/Settings`).
- Enforce corporate brand elevation rules, ensuring unified typography scale (Inter Display / Geist) across all mobile touchpoints.

## 3. Component Architecture: The Fluid Floating Dock
- **Positioning:** Floating pill dock, anchored 16px above bottom safe area, `inset-x-4`.
- **Surface Material:** `rgba(18, 20, 24, 0.85)` with `backdrop-filter: blur(24px)` and subtle top-edge rim lighting (`1px solid rgba(255, 255, 255, 0.12)`).
- **Haptic Feedback:** `UIImpactFeedbackGenerator(style: .light)` triggered upon tab select.
- **Active State Indicator:** Smooth morphing spring pill (`stiffness: 380`, `damping: 30`) gliding behind active icon labels.
- **F2F Instant Action Anchor:** Central pulse node enabling single-tap routing to live client appointment check-ins and field capture.
```