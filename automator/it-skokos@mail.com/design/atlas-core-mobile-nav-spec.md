# Atlas Core: Mobile Navigation Overhaul Design Specification
**Author:** Prism Bishop  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 18:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete design specification and architecture documentation for the Atlas Core mobile navigation overhaul, incorporating account hierarchy and face-to-face service standards.

## Deliverable
```
# Atlas Core — Mobile Navigation Overhaul (v2.0)
**Author:** Prism Bishop (Design) | **Project:** Atlas Core

## 1. Governance & Strategic Alignment
As part of our documentation-first methodology, this overhaul establishes a standardized mobile navigation pattern across SaaS tooling and Face-to-Face service modules.
- **Referenced Resource:** `Business Document: Company Document` was utilized to map tiered account permission matrices and align mobile user flows with our omnichannel service level agreements.

## 2. Navigation Architecture
Replaced legacy drawer navigation with a persistent 4-tab bottom bar and contextual quick-action sheet:
- `Tab 1: Overview` (`/m/overview`) — SaaS analytics and real-time platform telemetry.
- `Tab 2: Services & F2F` (`/m/services`) — On-site dispatch tracking, face-to-face appointment management.
- `Tab 3: Feeds` (`/m/activity`) — System alerts, notifications, audit logs.
- `Tab 4: Settings/Org` (`/m/org`) — Organization profile, docs, switch context.

## 3. Design Tokens & Ergonomics
- **Container Height:** `64px` + `env(safe-area-inset-bottom)`
- **Touch Target:** `48x48px` minimum bounding area per tab
- **Iconography:** 24px stroke geometry (`1.75px` default, `2.0px` active fill)
- **Tokens:**
  - Surface: `var(--nav-bg-glass: rgba(15, 23, 42, 0.88))`
  - Active: `var(--nav-item-active: #0EA5E9)`
  - Inactive: `var(--nav-item-idle: #64748B)`
  - Elevation: `0 -1px 3px 0 rgba(0, 0, 0, 0.1)`

## 4. Accessibility & Interaction Specs
- **Haptics:** Selection feedback via `UIImpactFeedbackGenerator(light)` on tab switch.
- **Accessibility (WCAG 2.1 AA):** Dynamic type scaling up to 200%; `aria-label` and `aria-current="page"` declared on all navigation items.
- **Handoff:** Tokens and component state maps exported directly to the Atlas Core Design System repo.
```