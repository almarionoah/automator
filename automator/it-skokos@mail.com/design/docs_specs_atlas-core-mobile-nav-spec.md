# Atlas Core Mobile Navigation Overhaul Design Specification
**Author:** Onyx Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D1 14:35  
## Summary

Comprehensive UI/UX design specification and information architecture overhaul for Atlas Core mobile viewport, covering hybrid SaaS workflows and Face-to-Face service interactions.

## Deliverable
```
# Design Specification: Atlas Core Mobile Navigation Overhaul (v2.0)
Author: Onyx Okafor, Design
Project: Atlas Core | Status: Ready for Review

## 1. Assumptions
Because baseline design tokens and telemetry were not provided, this spec assumes:
- Viewport Baseline: 390x844px (iOS/Android responsive target 360px-430px).
- Core Business Blend: Users manage digital SaaS analytics and schedule/attend Face-to-Face (F2F) appointments concurrently.
- Token Taxonomy: Standard Atlas design tokens (`--color-surface-nav`, `--space-4`, `--radius-pill`).

## 2. Information Architecture & Navigation Model
Replaced deprecated hamburger-only menu with a persistent 4-tab bottom bar + contextual bottom sheet.

### Primary Destinations (Bottom Bar)
1. Dashboard (`/app`): Hybrid feed (SaaS health + next F2F session).
2. F2F Services (`/services`): Booking calendar, client dispatch, route maps.
3. Workspace (`/workspace`): SaaS pipelines, workflows, active data rooms.
4. More (`[action:sheet]`): Secondary settings, billing, profile, offline sync queue.

## 3. UI Component Specifications
- Bottom Navigation Bar:
  - Container Height: 64px + `env(safe-area-inset-bottom)`
  - Background: `--color-surface-elevated` (Blur 20px / 85% opacity backdrop-filter)
  - Active State: `--color-brand-primary` icon + 4px dot indicator; text 11px Inter SemiBold.
  - Inactive State: `--color-text-subtle`; text 11px Inter Regular.
  - Touch Target: Minimum 48x48px per tab slot.
- Contextual Quick-Action (Center Dock):
  - 44x44px pill button: "+ New Action" (Fast-log F2F consultation or create SaaS pipeline entry).

## 4. Interaction & Accessibility
- Gestures: Bottom sheet drags with velocity-based snapping (threshold: 25% drag distance).
- Screen Readers: `nav[aria-label="Primary Mobile"]`, active item receives `aria-current="page"`.
- Motion: 200ms cubic-bezier(0, 0, 0.2, 1) ease-out for active indicator shifts.
```