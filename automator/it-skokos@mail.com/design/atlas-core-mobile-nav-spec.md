# Atlas Core Mobile Navigation Overhaul - Design & Component Spec
**Author:** Juno Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 16:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-ready design specification and component breakdown for the Atlas Core mobile navigation revamp, aligning SaaS telemetry and Face-to-Face service scheduling based on guidelines from Company Document.

## Deliverable
```
# Design Specification: Atlas Core Mobile Navigation Overhaul
Author: Juno Nkosi, Product Design
Project: Atlas Core (v2.4 Mobile Architecture)

## 1. Context & Business Alignment
This overhaul resolves navigation friction across mobile viewports (<768px). Per the operational standards detailed in the **Company Document**, our mobile navigation must support unified switching between our SaaS analytics dashboard and Face-to-Face service scheduling without contextual loss.

## 2. Navigation Architecture
- **Bottom Bar (Persistent)**: 4 core hubs (Dashboard, Services, F2F Dispatch, Settings) + Central Action Trigger.
- **Quick Action Sheet**: Slide-up modal invoked via the central `+` FAB for instant incident reporting and on-site booking.
- **Header Context Switcher**: Dropdown selector pinned to top-left for switching between SaaS client workspace and Field Service view.

## 3. Component Specs & Tokens
- **Container Height**: 64px + `env(safe-area-inset-bottom)`
- **Touch Targets**: Minimum 48x48px hit area per icon tab.
- **Colors & Tokens**:
  - Background: `var(--surface-nav-primary, #0F172A)`
  - Active Icon/Text: `var(--brand-accent, #2563EB)`
  - Inactive Icon/Text: `var(--text-muted, #94A3B8)`
  - Badge Alert (Pending F2F visits): `var(--danger-badge, #EF4444)` (8px dot)
- **Transitions**: Ease-out 180ms cubic-bezier(0.16, 1, 0.3, 1) on drawer expansion.

## 4. Resource Usage: Company Document
We referenced the **Company Document** to align the information hierarchy with multi-tiered client SLAs and technician routing protocols. Specifically, Face-to-Face Dispatch status cards were elevated to primary level to satisfy on-call response time requirements outlined in the document.

## 5. Handoff Checklist
- [x] Auto-layout Figma components synced to tokens repo
- [x] Safe-area insets validated on iOS and Android viewports
- [x] WCAG 2.1 AA 4.5:1 contrast compliance verified
```