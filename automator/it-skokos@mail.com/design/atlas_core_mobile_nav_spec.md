# Mobile Navigation Overhaul Specification - Atlas Core
**Author:** Jax Van Dyk  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 01:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification and tokenized implementation layout for the Atlas Core mobile navigation redesign, integrating brand alignment standards from the Company Document.

## Deliverable
```
# Design Specification: Atlas Core Mobile Navigation Overhaul
Author: Jax Van Dyk (Design)
Status: Ready for Implementation

## 1. Objective & Context
Streamline mobile viewport UX for Atlas Core by replacing the legacy nested hamburger drawer with an accessible, high-performance bottom navigation bar and condensed quick-action sheet. This deliverable directly applies architectural guidelines from the Business Document: 'Company Document' to reconcile hybrid SaaS platform views with Face-to-Face booking workflows.

## 2. Resource Utilization
- **Company Document**: Used to align mobile typography scales, tap-target tolerances (min 48x48dp), and corporate color contrast ratios (WCAG AAA standard for primary navigational items).

## 3. Component Architecture
### 3.1 Persistent Bottom Navigation Bar
- Height: 64px + safe-area-inset-bottom
- Background: var(--surface-primary-elevation-2)
- Tabs (4 core destinations):
  1. Dashboard (`/app/dashboard`)
  2. Services & F2F (`/app/f2f-services`)
  3. Bookings (`/app/schedule`)
  4. Account / More (`/app/profile`)

### 3.2 Quick Action Drawer
- Trigger: Elevated center floating action button (+)
- Sheet Transition: 200ms cubic-bezier(0.16, 1, 0.3, 1)
- Actions: 'New F2F Client Check-in', 'Instant Invoice', 'Book Room'

## 4. Design Tokens
- `--nav-icon-active`: #0F52BA (Atlas Cobalt)
- `--nav-icon-inactive`: #6B7280 (Neutral Slate)
- `--nav-badge-bg`: #EF4444 (Alert Red)
- `--nav-font-size-label`: 11px / 1.2 line-height

## 5. Handoff Notes
- Zero layout shifts during routing transitions.
- Tested across iOS (WebKit) and Android (Chrome) viewports (360px - 428px width).
```