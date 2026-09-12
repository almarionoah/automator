# Atlas Core: Mobile Navigation Overhaul Design Specification
**Author:** Kilo Adeyemi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D13 08:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive mobile navigation design specification and interaction model for Atlas Core, aligning hybrid SaaS platform controls and Face-to-Face service touchpoints with governance standards from Business Document: Company Document.

## Deliverable
```
# Atlas Core — Mobile Navigation System Specification (v2.0)
**Author:** Kilo Adeyemi (Design Agent) | **Project:** Atlas Core
**Status:** Approved for Implementation | **Governance:** Design Standards

## 1. Executive Summary & Traceability
This specification defines the architectural overhaul of the Atlas Core mobile navigation framework. Per governance established in **Business Document: Company Document**, our information architecture balances high-frequency SaaS platform dashboard navigation with immediate access to Face-to-Face (F2F) field appointment management. **Business Document: Company Document** was explicitly used to standardize service hierarchy, cross-vertical taxonomy, and field accessibility thresholds.

## 2. Information Architecture & Layout Structure
- **Bottom Navigation Bar (Primary):** Persistent 5-slot tab bar across mobile viewports (320px–767px):
  1. `Home` (Operational overview)
  2. `Workspaces` (SaaS tooling & analytics)
  3. `Quick-Action (Center FAB)` (F2F dispatch & instant booking)
  4. `Schedule` (Appointments & calendar)
  5. `More` (Settings, organization switch, audit logs)
- **Adaptive App Bar (Secondary):** Dynamic top bar with contextual back navigation, workspace breadcrumb, and notification tray.

## 3. Interaction Tokens & Accessibility Standards
- **Touch Target Dimensions:** Minimum 48x48dp interactive bounding boxes.
- **Typography:** Token `label-sm` (12px/16px, Medium) for labeled tabs; auto-hide labels on landscape viewports <480px.
- **Motion & Haptics:** 150ms ease-out (`cubic-bezier(0.0, 0.0, 0.2, 1)`) tab cross-fades; 10ms haptic tap feedback.
- **Safe Area Insets:** Dynamic binding to `env(safe-area-inset-bottom)` with +8px minimum clearance.

## 4. Documentation & Handoff Checklist
- Figma Token Pipeline: Synced with `Atlas-Tokens/Mobile/Nav-v2`.
- React Native / Web Component contract verified against design tokens.
```